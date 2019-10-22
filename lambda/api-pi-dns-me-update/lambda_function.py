import json, uuid, time, boto3, os

zone = os.environ['Route53_Zone_ID']
table = os.environ['DynamoDB_Table_Names']
iplist = os.environ['DynamoDB_Table_IPList']

def lambda_handler(event, context):
    if ((event['name'] == "api") or (event['name'] == "www") or (event['name'] == "")):
        return {
        "statusCode": 403,
        "response": "Forbidden"
        }

    dynamodb = boto3.client('dynamodb')
    getrequest = dynamodb.get_item(TableName=table, Key={'name':{'S':event['name']}})
    if 'Item' in getrequest.keys():
        if getrequest['Item']['key']['S']==event['secret']:
            putrequest = dynamodb.update_item(TableName=table,Key={'name': {'S':event['name']}},UpdateExpression="set ip = :i, timetolive=:t",ExpressionAttributeValues={':i': {'S': event['sourceIP']},':t': {'N': str(time.time())}})
            route53 = boto3.client('route53')
            dnsrequest = route53.change_resource_record_sets(
            HostedZoneId=zone,
            ChangeBatch={
                'Comment': 'updated by api',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': event['name']+".pi-dns.me.",
                            'Type': 'A',
                            'TTL': 60,
                            'ResourceRecords': [
                                {
                                    'Value': event['sourceIP']
                                    },
                                ]
                            }
                        },
                    ]
                }
            )
            message = "Updated"
            statusCode = 200
        else:
            message = "Not Authorised"
            statusCode = 401
    else:
        statusCode = 404
        message = "Not Found"
    return {
        "statusCode": statusCode,
        "response": message
    }
