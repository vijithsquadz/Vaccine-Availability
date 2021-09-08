import boto3
from botocore.exceptions import ClientError
import time

count = 0

while True:
    
    if count >= 5:
        break

    SENDER = "Service Tester <vijith.vijayan0512@gmail.com>"
    RECIPIENT = ["vijith.squadz@gmail.com", "sanalsquadz08@gmail.com"]
    AWS_REGION = "ap-south-1"
    SUBJECT = "Amazon SES Test (SDK for Python) - " + str(count + 1)
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                "This email was sent with Amazon SES using the "
                "AWS SDK for Python (Boto)."
                )
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK for Python)</h1>
    <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """    
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',aws_access_key_id='AKIAJ2EOOFKNLS3A2STA',
                        aws_secret_access_key= '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',
                        region_name=AWS_REGION)

    # Try to send the email.
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
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        count += 1 