import boto3
import csv
import os
from datetime import datetime, timedelta, timezone

REGION = "ap-south-1"


def get_cpu_metrics():
    ec2 = boto3.client("ec2", region_name=REGION)
    cloudwatch = boto3.client("cloudwatch", region_name=REGION)

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
                "State": instance["State"]["Name"]
            })

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=1)

    results = []

    for instance in instances:
        metric_response = cloudwatch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": instance["Instance ID"]
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average"]
        )

        datapoints = metric_response["Datapoints"]

        if datapoints:
            latest = max(datapoints, key=lambda point: point["Timestamp"])
            cpu_average = round(latest["Average"], 2)
            metric_time = latest["Timestamp"].strftime("%Y-%m-%d %H:%M:%S UTC")
        else:
            cpu_average = "No recent data"
            metric_time = "Not Available"

        results.append({
            "Instance ID": instance["Instance ID"],
            "Name": instance["Name"],
            "State": instance["State"],
            "CPU Utilization (%)": cpu_average,
            "Metric Timestamp": metric_time
        })

    return results


def save_to_csv(results):
    os.makedirs("reports", exist_ok=True)

    filename = (
        "reports/cloudwatch_cpu_metrics_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".csv"
    )

    fieldnames = [
        "Instance ID",
        "Name",
        "State",
        "CPU Utilization (%)",
        "Metric Timestamp"
    ]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nReport saved: {filename}")


if __name__ == "__main__":
    print("Starting CloudWatch CPU Metrics Automation...")

    metrics = get_cpu_metrics()

    print(f"EC2 instances checked: {len(metrics)}")

    for item in metrics:
        print(item)

    save_to_csv(metrics)

    print("\nCloudWatch CPU Metrics Automation Completed!")
