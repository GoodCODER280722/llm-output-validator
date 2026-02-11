import json
import os
from datetime import datetime
from config import FLAG_WORDS, REQUIRED_PHRASES, MAX_CHARS, PASS_THRESHOLD


def analyze(text: str) -> dict:
    raw = text
    cleaned = text.strip()
    lowered = cleaned.lower()

    issues = []
    score = 100

    # Rule: empty
    if not cleaned:
        issues.append({"rule": "empty", "message": "Response is empty."})
        score -= 100

    # Rule: length
    if len(cleaned) > MAX_CHARS:
        issues.append({
            "rule": "max_length",
            "message": f"Response exceeds {MAX_CHARS} characters ({len(cleaned)})."
        })
        score -= 20

    # Rule: flag words
    found_flags = [w for w in FLAG_WORDS if w in lowered]
    if found_flags:
        issues.append({
            "rule": "flag_words",
            "message": f"Found flagged terms: {', '.join(found_flags)}",
            "found": found_flags
        })
        score -= min(10 * len(found_flags), 40)

    # Rule: required phrases
    missing_required = [p for p in REQUIRED_PHRASES if p.lower() not in lowered]
    if missing_required:
        issues.append({
            "rule": "required_phrases",
            "message": f"Missing required phrases: {', '.join(missing_required)}",
            "missing": missing_required
        })
        score -= min(10 * len(missing_required), 30)

    score = max(0, min(100, score))
    passed = score >= PASS_THRESHOLD and not any(i["rule"] == "empty" for i in issues)

    return {
        "passed": passed,
        "score": score,
        "issues": issues,
        "meta": {
            "chars": len(cleaned),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
        "input_preview": raw[:200] + ("..." if len(raw) > 200 else "")
    }


def save_report(report: dict) -> str:
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return filename


def main():
    print("LLM Output Validator (Mock Mode)\n")
    print("Paste an AI response, then press Enter twice:\n")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    text = "\n".join(lines)
    report = analyze(text)

    print("\n--- Results ---")
    print("PASSED:" if report["passed"] else "FAILED:", report["passed"])
    print("SCORE:", report["score"])
    if report["issues"]:
        print("\nIssues:")
        for i, issue in enumerate(report["issues"], start=1):
            print(f"  {i}. [{issue['rule']}] {issue['message']}")
    else:
        print("\nNo issues detected.")

    path = save_report(report)
    print("\nSaved report:", path)


if __name__ == "__main__":
    main()