
import boto3
import csv
import os
from datetime import datetime

REGION = "ap-south-1"


def get_ec2_inventory():
    ec2 = boto3.client("ec2", region_name=REGION)

    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            name = "Not-Tagged"

            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]

            instances.append({
                "Instance ID": instance["InstanceId"],
                "Name": name,
                "State": instance["State"]["Name"],
                "Instance Type": instance["InstanceType"],
                "Availability Zone": instance["Placement"]["AvailabilityZone"]
            })

    return instances


def save_to_csv(instances):
    os.makedirs("reports", exist_ok=True)

    filename = (
        "reports/ec2_inventory_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".csv"
    )

    fieldnames = [
        "Instance ID",
        "Name",
        "State",
        "Instance Type",
        "Availability Zone"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(instances)

    print(f"\nReport saved: {filename}")


if __name__ == "__main__":
    print("Starting AWS EC2 Inventory Automation...")

    inventory = get_ec2_inventory()

    print(f"Total EC2 instances found: {len(inventory)}")

    for instance in inventory:
        print(instance)

    save_to_csv(inventory)

    print("\nEC2 Inventory Automation Completed!")

