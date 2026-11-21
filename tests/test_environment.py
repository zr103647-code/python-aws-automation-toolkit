import sys
import boto3


def test_python_version():
    assert sys.version_info >= (3, 10)


def test_boto3_installed():
    assert boto3.__version__ is not None
