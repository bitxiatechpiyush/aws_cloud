import boto3
from pymongo import MongoClient
from django.conf import settings

# DynamoDB connection
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

# MongoDB connection
mongo_client = MongoClient(settings.MONGODB_URI)
mongo_db = mongo_client["mydatabase"]
mongo_collection = mongo_db["mycollection"]
