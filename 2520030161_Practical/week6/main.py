"""Week 6: Golden question set baseline evaluation with local Ollama."""
import csv
import json
from datetime import datetime
from pathlib import Path

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"
INPUT_FILE = "golden_set.json"
OUTPUT_FILE = "baseline_results.csv"
RELEASE = "v0.1"
TIMEOUT_SECONDS = 120


def load_golden_set(path=INPUT_FILE):
    """Load and minimally validate the golden question JSON."""
    with open(path, "r", encoding="utf-8") as file:
        items = json.load(file)
    if not isinstance(items, list) or not items:
        raise ValueError("Golden set must be a non-empty JSON list.")
    required = {"id", "question", "expected_answer", "keywords", "source"}
    for index, item in enumerate(items, start=1):
        missing = required - item.keys()
        if missing:
            raise ValueError(f"Question {index} is missing fields: {sorted(missing)}")
        if not isinstance(item["keywords"], list):
            raise ValueError(f"Question {item['id']} keywords must be a list.")
    return items


def get_llm_answer(question):
    payload = {
        "model": MODEL_NAME,
        "prompt": question,
        "stream": False,
        "options": {"temperature": 0},
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    result = response.json()
    return result.get("response", "").strip()


def calculate_score(answer, expected_keywords):
    """Return keyword coverage percentage and matched/missing keyword lists."""
    answer_lower = answer.lower()
    matched = [word for word in expected_keywords if word.lower() in answer_lower]
    missing = [word for word in expected_keywords if word.lower() not in answer_lower]
    score = (len(matched) / len(expected_keywords) * 100) if expected_keywords else 0
    return round(score, 2), matched, missing


def evaluate(golden_questions):
    results = []
    total_score = 0.0
    successful_questions = 0

    print("\\n======================================")
    print("BASELINE RUN STARTED")
    print("======================================")

    for index, item in enumerate(golden_questions, start=1):
        qid = item["id"]
        question = item["question"]
        keywords = item["keywords"]
        print(f"\\nQuestion {index}: {qid}")
        print("Question:", question)

        try:
            answer = get_llm_answer(question)
            score, matched, missing = calculate_score(answer, keywords)
            status = "PASS" if score >= 60 else "REVIEW"
            total_score += score
            successful_questions += 1
            print("\\nLLM Answer:\\n", answer)
            print("\\nExpected Answer:\\n", item["expected_answer"])
            print("Matched Keywords:", matched)
            print("Missing Keywords:", missing)
            print("Score:", score, "%")
            print("Status:", status)
            results.append({
                "Question_ID": qid,
                "Question": question,
                "Expected_Answer": item["expected_answer"],
                "LLM_Answer": answer,
                "Matched_Keywords": ", ".join(matched),
                "Missing_Keywords": ", ".join(missing),
                "Score": score,
                "Status": status,
                "Source": item["source"],
                "Model": MODEL_NAME,
                "Release": RELEASE,
            })
        except (requests.RequestException, ValueError, KeyError) as error:
            print("Error:", error)
            results.append({
                "Question_ID": qid,
                "Question": question,
                "Expected_Answer": item["expected_answer"],
                "LLM_Answer": "",
                "Matched_Keywords": "",
                "Missing_Keywords": ", ".join(keywords),
                "Score": 0,
                "Status": "ERROR",
                "Source": item["source"],
                "Model": MODEL_NAME,
                "Release": RELEASE,
            })

    return results, total_score, successful_questions


def save_results(results, path=OUTPUT_FILE):
    fieldnames = [
        "Question_ID", "Question", "Expected_Answer", "LLM_Answer",
        "Matched_Keywords", "Missing_Keywords", "Score", "Status",
        "Source", "Model", "Release",
    ]
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def print_summary(golden_questions, results, total_score, successful_questions):
    average_score = total_score / successful_questions if successful_questions else 0
    passed = sum(row["Status"] == "PASS" for row in results)
    review = sum(row["Status"] == "REVIEW" for row in results)
    errors = sum(row["Status"] == "ERROR" for row in results)

    print("\\n======================================")
    print("BASELINE EVALUATION SUMMARY")
    print("======================================")
    print("Release Version:", RELEASE)
    print("Model:", MODEL_NAME)
    print("Total Questions:", len(golden_questions))
    print("Successful Responses:", successful_questions)
    print("Passed Questions:", passed)
    print("Questions for Review:", review)
    print("Failed Requests:", errors)
    print("Average Keyword Coverage:", round(average_score, 2), "%")
    print("Evaluation Date:", datetime.now().isoformat(timespec="seconds"))
    print("\\nResults saved to:", OUTPUT_FILE)
    print("\\nBASELINE RUN COMPLETED!")
    print(f"Release {RELEASE} created successfully.")


def main():
    try:
        golden_questions = load_golden_set()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"Could not load {INPUT_FILE}: {error}")

    print("\\n======================================")
    print("GOLDEN QUESTION SET")
    print("======================================")
    print("Total Questions:", len(golden_questions))
    print("Model:", MODEL_NAME)

    results, total_score, successful_questions = evaluate(golden_questions)
    save_results(results)
    print_summary(golden_questions, results, total_score, successful_questions)


if __name__ == "__main__":
    main()
