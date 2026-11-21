
import csv
import os
from datetime import datetime


REPORTS_FOLDER = "reports"


def generate_summary():
    os.makedirs(REPORTS_FOLDER, exist_ok=True)

    summary = []

    for filename in os.listdir(REPORTS_FOLDER):

        if not filename.endswith(".csv"):
            continue

        if filename == "combined_summary.csv":
            continue

        filepath = os.path.join(REPORTS_FOLDER, filename)

        try:
            with open(filepath, "r", newline="") as file:
                reader = csv.DictReader(file)
                rows = list(reader)

                summary.append({
                    "Report Name": filename,
                    "Total Records": len(rows),
                    "Report Status": "Processed"
                })

        except Exception as error:
            summary.append({
                "Report Name": filename,
                "Total Records": 0,
                "Report Status": f"Error: {error}"
            })

    return summary


def save_summary(summary):
    filename = os.path.join(
        REPORTS_FOLDER,
        "combined_summary.csv"
    )

    fieldnames = [
        "Report Name",
        "Total Records",
        "Report Status"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary)

    print(f"\nCombined report saved: {filename}")


if __name__ == "__main__":
    print("Starting CSV Report Generator...")

    summary = generate_summary()

    print(f"Total reports processed: {len(summary)}")

    for report in summary:
        print(report)

    save_summary(summary)

    print("\nCSV Report Generator Completed!")
