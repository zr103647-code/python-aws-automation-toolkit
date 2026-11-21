import boto3
import csv
import os
from datetime import datetime

REGION = "ap-south-1"


def get_s3_inventory():
    s3 = boto3.client("s3", region_name=REGION)

    response = s3.list_buckets()

    buckets = []

    for bucket in response["Buckets"]:
        buckets.append({
            "Bucket Name": bucket["Name"],
            "Creation Date": bucket["CreationDate"].strftime("%Y-%m-%d %H:%M:%S")
        })

    return buckets


def save_to_csv(buckets):
    os.makedirs("reports", exist_ok=True)

    filename = (
        "reports/s3_inventory_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".csv"
    )

    fieldnames = ["Bucket Name", "Creation Date"]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(buckets)

    print(f"\nReport saved: {filename}")


if __name__ == "__main__":
    print("Starting AWS S3 Bucket Inventory Automation...")

    inventory = get_s3_inventory()

    print(f"Total S3 buckets found: {len(inventory)}")

    for bucket in inventory:
        print(bucket)

    save_to_csv(inventory)

    print("\nS3 Bucket Inventory Automation Completed!")
