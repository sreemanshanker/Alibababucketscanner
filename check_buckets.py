import oss2
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# List of credentials for different environments
credentials = [
    {'access_key_id': '', 'access_key_secret': '', 'endpoint': ''},
    {'access_key_id': '', 'access_key_secret': '', 'endpoint': ''},
    # Add more credentials as needed
]

# List of buckets to exclude from the results
excluded_buckets = ["<bucketname>"]

# Email notification settings
email_recipients = ["<email.address>"]

def send_email(subject, body, to_emails):
    from_email = "<email.address>"
    password = "<email.password>"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        print("Connecting to SMTP server...")
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()
        print("Logging in to SMTP server...")
        server.login(from_email, password)
        text = msg.as_string()
        print("Sending email...")
        server.sendmail(from_email, to_emails, text)
        print("Email sent successfully")
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_public_access(bucket_name, endpoint):
    url = f"https://{bucket_name}.{endpoint}"
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return f"Bucket '{bucket_name}' is PUBLIC."
        else:
            return f"Bucket '{bucket_name}' is NOT PUBLIC (status: {response.status_code})."
    except requests.exceptions.RequestException:
        return f"Error accessing '{bucket_name}'."

def main():
    results = []
    try:
        for cred in credentials:
            access_key_id = cred['access_key_id']
            access_key_secret = cred['access_key_secret']
            endpoint = cred['endpoint']

            auth = oss2.Auth(access_key_id, access_key_secret)
            service = oss2.Service(auth, endpoint)

            print(f"Checking buckets for endpoint: {endpoint}")

            # List all buckets
            for bucket_info in oss2.BucketIterator(service):
                bucket_name = bucket_info.name

                # Skip excluded buckets
                if bucket_name in excluded_buckets:
                    print(f"Skipping excluded bucket: {bucket_name}")
                    continue

                # Create a Bucket object
                bucket = oss2.Bucket(auth, endpoint, bucket_name)
                # Check bucket ACL
                bucket_acl = bucket.get_bucket_acl()
                if bucket_acl.acl == oss2.BUCKET_ACL_PUBLIC_READ or bucket_acl.acl == oss2.BUCKET_ACL_PUBLIC_READ_WRITE:
                    result = f"Bucket {bucket_name} ACL: {bucket_acl.acl} (PUBLIC)"
                    print(result)
                    results.append(result)
                    # Additional check for public access
                    public_access_result = check_public_access(bucket_name, endpoint)
                    print(public_access_result)
                    results.append(public_access_result)
    
    except Exception as e:
        error_message = f"Error: {e}"
        print(error_message)
        results.append(error_message)

    # Send email with the results
    if results:
        email_body = "\n".join(results)
        send_email("Public OSS Bucket found!!", email_body, email_recipients)

if __name__ == "__main__":
    main()
