import boto3


def test_aws_region_configured():
    session = boto3.Session()
    assert session.region_name == "ap-south-1"
