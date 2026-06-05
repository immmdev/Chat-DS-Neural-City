"""
FastAPI Application — Road Safety Analytics Backend.
Entry point for the server. Loads data, initializes all services,
and mounts API routes.
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routes.query_routes import router as query_router
from backend.schemas.response_schema import HealthResponse
from backend.services.llm_service import LLMService
from backend.services.pandas_engine import PandasEngine
from backend.services.answer_service import AnswerService
from backend.services.validation_service import ValidationService
from backend.utils.metadata import DatasetMetadata

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ── Environment ──────────────────────────────────────────────────────────────
load_dotenv()

DATA_PATH = os.getenv(
    "DATASET_PATH",
    str(Path(__file__).parent / "data" / "accidents.csv"),
)
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")


# ── Lifespan (startup / shutdown) ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize all services at startup."""
    logger.info("🚀  Starting Road Safety Analytics Backend...")

    # ── Load dataset ─────────────────────────────────────────────────────
    # Try configured path first, fall back to sibling CSV
    data_path = DATA_PATH
    if not os.path.exists(data_path):
        # Check if the CSV is alongside app.py
        alt_path = str(Path(__file__).parent / "indian_roads_dataset.csv")
        if os.path.exists(alt_path):
            data_path = alt_path
        else:
            logger.error(f"Dataset not found at {data_path} or {alt_path}")
            raise FileNotFoundError(f"Dataset not found. Check DATASET_PATH env var.")

    logger.info(f"📂  Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns.")

    # ── Build metadata ───────────────────────────────────────────────────
    metadata = DatasetMetadata(df)
    logger.info(f"📊  Metadata built — Cities: {metadata.cities}")

    # ── Initialize services ──────────────────────────────────────────────
    if not GEMINI_API_KEY:
        logger.warning("⚠️  GOOGLE_API_KEY not set. LLM calls will fail.")

    app.state.llm_service = LLMService(GEMINI_API_KEY, metadata)
    app.state.validation_service = ValidationService(metadata)
    app.state.pandas_engine = PandasEngine(df)
    app.state.answer_service = AnswerService()
    app.state.metadata = metadata
    app.state.df = df
    app.state.audit_log = []

    logger.info("✅  All services initialized successfully!")

    yield  # Application runs here

    logger.info("🛑  Shutting down Road Safety Analytics Backend...")


# ── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="Road Safety Analytics API",
    description=(
        "AI-powered analytics backend for querying Indian road accident data. "
        "Uses Gemini 2.5 Flash to interpret natural language questions and "
        "produces structured analytics with charts."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS Middleware ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routes ──────────────────────────────────────────────────────────
app.include_router(query_router)


# ── Health Check ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint — API info."""
    return {
        "service": "Road Safety Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check with dataset stats."""
    metadata = app.state.metadata
    return HealthResponse(
        status="healthy",
        total_records=metadata.metadata["total_records"],
        columns=metadata.columns,
        date_range=metadata.metadata["date_range"],
    )


@app.get("/api/metadata", tags=["Metadata"])
async def get_metadata():
    """Return full dataset metadata."""
    return app.state.metadata.metadata


@app.get("/api/audit-log", tags=["Audit"])
async def get_audit_log():
    """Return audit log of all queries processed."""
    return {
        "total_queries": len(app.state.audit_log),
        "logs": app.state.audit_log[-50:],  # Last 50 entries
    }
