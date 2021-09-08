import boto3
from botocore.exceptions import ClientError

def notify(subject, body_text, body_html ):
    SENDER = "Vaccine Availability <vijith.vijayan0512@gmail.com>"

    if "Ernakulam" in subject:
        RECIPIENT = ["vijith.squadz@gmail.com", "sanalsquadz08@gmail.com"]
    else:
         RECIPIENT = ["vijith.squadz@gmail.com"]

    AWS_REGION = "ap-south-1"
    SUBJECT = subject
    BODY_TEXT = body_text
    BODY_HTML = body_html     
    CHARSET = "UTF-8"

    client = boto3.client('ses',aws_access_key_id='AKIAJ2EOOFKNLS3A2STA',
                        aws_secret_access_key= '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',
                        region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENT
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )


    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


