"""
Evaluation Script for Road Safety Analytics Backend.
Runs the 7 sample questions against the API to verify behavior.
Usage: Start the API server first (`uvicorn backend.app:app --reload`), then run this script.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.9:8000"

QUESTIONS = [
    "Which city recorded the highest number of fatal accidents?",
    "Compare Delhi and Mumbai average risk score.",
    "How does accident severity vary by weather condition?",
    "Top 5 cities by casualties.",
    "Do weekends have more accidents than weekdays?",
    "How do accidents vary during festivals?",
    "What is the average number of vehicles involved per accident?",
]

def check_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def format_terminal_output(q, data):
    print("\n" + "="*80)
    print(f"QUESTION: {q}")
    print("="*80)
    
    if "answer" in data:
        print(f"\nANSWER:\n{data['answer']}")
        
    if "operation_description" in data:
        print(f"\nOPERATION:\n{data['operation_description']}")
        
    if "query_json" in data:
        print("\nSTRUCTURED QUERY:")
        print(json.dumps(data["query_json"], indent=2))
        
    if "chart_path" in data and data["chart_path"]:
        print(f"\nCHART GENERATED AT: {data['chart_path']}")
        
    if "result_table" in data and len(data["result_table"]) > 0:
        print("\nDATA SAMPLE (first 3 rows):")
        for row in data["result_table"][:3]:
            print(row)

def main():
    print("Starting evaluation...")
    if not check_health():
        print(f"Error: API server is not running on {BASE_URL}")
        print("Please run: uvicorn backend.app:app --reload")
        return

    for i, q in enumerate(QUESTIONS, 1):
        print(f"\nProcessing {i}/{len(QUESTIONS)}...")
        try:
            response = requests.post(
                f"{BASE_URL}/api/query",
                json={"question": q},
                timeout=30  # LLM calls might take a moment
            )
            data = response.json()
            format_terminal_output(q, data)
        except Exception as e:
            print(f"Failed to process '{q}': {e}")
            if 'response' in locals():
                print(f"Status Code: {response.status_code}")
                try:
                    print(f"Response: {response.text}")
                except:
                    pass
        
        # Slight pause to avoid hitting rate limits on Gemini Flash
        time.sleep(1)

if __name__ == "__main__":
    main()
