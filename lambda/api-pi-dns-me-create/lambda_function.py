import json, uuid, time, boto3, os

zone = os.environ['Route53_Zone_ID']
table = os.environ['DynamoDB_Table_Names']
iplist = os.environ['DynamoDB_Table_IPList']

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    if ((event['name'] == "api") or (event['name'] == "*") or (event['name'] == "www") or (event['name'] == "")):
        return {
        "statusCode": 403,
        "response": "Forbidden"
        }

    getrequest = dynamodb.get_item(TableName=iplist, Key={'ip':{'S':event['sourceIP']}})
    if 'Item' in getrequest.keys():
        return {
        "statusCode": 429,
        "response": "Too many requests"
        }

    getrequest = dynamodb.get_item(TableName=table, Key={'name':{'S':event['name']}})
    if 'Item' in getrequest.keys():
        message = "Already Taken"
        statusCode = 409
    else:
        guid = str(uuid.uuid4())
        putrequest = dynamodb.put_item(TableName=table, Item= {'name': {'S': event['name']},'ip': {'S':event['sourceIP']},'timetolive':{'N':str(time.time())},'key':{'S':guid}})
        putrequest = dynamodb.put_item(TableName=iplist, Item= {'ip': {'S':event['sourceIP']},'timetolive':{'N':str(time.time())}})
        statusCode = 201
        message = guid

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

    return {
        "statusCode": statusCode,
        "response": message
    }
