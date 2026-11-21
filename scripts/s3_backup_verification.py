
import boto3
import csv
import os
from datetime import datetime

REGION = "ap-south-1"

# Add your existing S3 bucket name here when available
BUCKET_NAME = ""

# Expected backup file name
BACKUP_FILE = "backups/database_backup.zip"


def verify_backup():
    s3 = boto3.client("s3", region_name=REGION)

    results = []

    if not BUCKET_NAME:
        print("WARNING: No S3 bucket configured.")

        results.append({
            "Bucket Name": "Not Configured",
            "Backup File": BACKUP_FILE,
            "Verification Status": "Not Checked",
            "Details": "No S3 bucket name provided"
        })

        return results

    try:
        s3.head_bucket(Bucket=BUCKET_NAME)

        try:
            s3.head_object(
                Bucket=BUCKET_NAME,
                Key=BACKUP_FILE
            )

            status = "Verified"
            details = "Backup file exists in S3 bucket"

        except s3.exceptions.ClientError as error:
            error_code = error.response["Error"]["Code"]

            if error_code in ["404", "NoSuchKey", "NotFound"]:
                status = "Missing"
                details = "Backup file not found"
            else:
                raise

        results.append({
            "Bucket Name": BUCKET_NAME,
            "Backup File": BACKUP_FILE,
            "Verification Status": status,
            "Details": details
        })

    except Exception as error:
        results.append({
            "Bucket Name": BUCKET_NAME,
            "Backup File": BACKUP_FILE,
            "Verification Status": "Error",
            "Details": str(error)
        })

    return results


def save_report(results):
    os.makedirs("reports", exist_ok=True)

    filename = (
        "reports/s3_backup_verification_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".csv"
    )

    fieldnames = [
        "Bucket Name",
        "Backup File",
        "Verification Status",
        "Details"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nReport saved: {filename}")


if __name__ == "__main__":
    print("Starting S3 Backup Verification Automation...")

    verification_results = verify_backup()

    for result in verification_results:
        print(result)

    save_report(verification_results)

    print("\nS3 Backup Verification Automation Completed!")
