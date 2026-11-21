# Python-Based AWS Automation Toolkit

**Author:** Ziaur Rahman

## Overview
Python and Boto3 based AWS automation toolkit for inventory, monitoring, CSV reporting and error logging.

## Technologies
- Python 3.14
- Boto3
- AWS CLI
- EC2, S3, CloudWatch
- Linux Ubuntu
- Pytest
- Git and GitHub

## Features
1. EC2 Instance Inventory
2. S3 Bucket Inventory
3. EC2 Status Checker
4. CloudWatch CPU Metrics
5. S3 Backup Verification (Test Mode)
6. CSV Report Generator
7. Error Logging

## Testing
Automated tests: 3 passed.
Run: python -m pytest tests/ -v

## AWS Configuration
Region: ap-south-1 (Mumbai)

## Important Notes
- No AWS infrastructure resources were created.
- S3 backup verification was executed in test mode.
- Empty inventory reports are expected when no resources exist.
