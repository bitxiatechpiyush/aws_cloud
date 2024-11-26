from django.http import JsonResponse
from django.shortcuts import render
from .db_connections import dynamodb, mongo_collection
import boto3
from django.conf import settings

# AWS SNS and SES clients
sns_client = boto3.client(
    'sns',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)
ses_client = boto3.client(
    'ses',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

def add_item(request):
    if request.method == "POST":
        data = request.POST
        item_name = data.get("item_name")
        item_description = data.get("item_description")

        if not item_name or not item_description:
            return JsonResponse({"error": "Both item_name and item_description are required."}, status=400)

        # Add to DynamoDB
        table = dynamodb.Table('YourDynamoDBTableName')
        table.put_item(
            Item={'item_name': item_name, 'item_description': item_description}
        )

        # Add to MongoDB
        mongo_collection.insert_one({'item_name': item_name, 'item_description': item_description})

        # Trigger AWS SNS
        sns_client.publish(
            PhoneNumber='+1234567890',  # Replace with your phone number
            Message=f"New item added: {item_name} - {item_description}"
        )

        # Trigger AWS SES
        ses_client.send_email(
            Source='your-email@example.com',
            Destination={'ToAddresses': ['recipient@example.com']},
            Message={
                'Subject': {'Data': 'New Item Added'},
                'Body': {'Text': {'Data': f"Item: {item_name}\nDescription: {item_description}"}}
            }
        )

        return JsonResponse({"message": "Item added successfully and notifications sent."})
    return render(request, 'add_item.html')
