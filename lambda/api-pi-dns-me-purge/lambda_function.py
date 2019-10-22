import json, uuid, time, boto3, os
from boto3.dynamodb.conditions import Attr

zone = os.environ['Route53_Zone_ID']
table = os.environ['DynamoDB_Table_Names']
iplist = os.environ['DynamoDB_Table_IPList']

timeoutvalue=604800
unblockvalue=3600
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb').Table(iplist)
    scanrequest = dynamodb.scan(FilterExpression=Attr("timetolive").lt(int(time.time()-unblockvalue)))
    for item in scanrequest['Items']:
        dynamodb.delete_item(
            Key={
                'ip': item['ip']
            }
        )
    dynamodb = boto3.resource('dynamodb').Table(table)
    scanrequest = dynamodb.scan(FilterExpression=Attr("timetolive").lt(int(time.time()-timeoutvalue)))
    route53 = boto3.client('route53')
    for item in scanrequest['Items']:
        dynamodb.delete_item(
            Key={
                'name': item['name']
            }
        )
        dnsrequest = route53.change_resource_record_sets(
            HostedZoneId=zone,
            ChangeBatch={
                'Comment': 'updated by api',
                'Changes': [
                    {
                        'Action': 'DELETE',
                        'ResourceRecordSet': {
                            'Name': item['name']+".pi-dns.me.",
                            'Type': 'A',
                            'TTL': 60,
                            'ResourceRecords': [
                        {
                            'Value': item['ip']
                        }
                    ]
                }
            }
        ]
    }
)
