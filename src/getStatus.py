import json
import boto3
from decimal import Decimal

TABLE_NAME = 'SystemStatus'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

# Convert all Decimals in a dict to float
def convert_decimals(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(v) for v in obj]
    else:
        return obj

def lambda_handler(event, context):
    try:
        response = table.get_item(Key={'id': 'laptop1'})

        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No data found'})
            }

        raw_data = response['Item']['data']
        clean_data = convert_decimals(raw_data)

        return {
            'statusCode': 200,
            'body': json.dumps(clean_data)
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
