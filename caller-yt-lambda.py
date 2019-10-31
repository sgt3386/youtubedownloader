import json
import boto3
import os
import time

LAMBDA_ARN = str(os.environ['yt_lambda'])
client_lambda = boto3.client('lambda')
TIME = str(time.time())

def lambda_tag():
    response = client_lambda.tag_resource(
        Resource=LAMBDA_ARN,
        Tags={
        'LastRan': TIME
        }
    )
    return (response)

def lambda_run(funcJSON):
    response = client_lambda.invoke(
        FunctionName=LAMBDA_ARN,
        InvocationType='RequestResponse',
        Payload = json.JSONEncoder().encode(funcJSON)
    )
    data = response['Payload'].read()
    return (data)

def lambda_handler(event, context):
    # TODO implement
    json_data = event['body']
    parse_json = json_data.split('%3D')
    parse_json_2 = parse_json[1].split('%')
    lambda_tag()
    time.sleep(5)
    status = lambda_run(parse_json_2[0])
    print(parse_json_2[0])
    return {
        'statusCode': 200,
        'body': status.decode('utf')
    }
