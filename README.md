I couldn’t find a feature in Alibaba to ensure we didn’t miss open buckets, so I created this script to identify all open buckets and email the results. It can be set to run on a schedule to find them in real time.

Features
  Checks the public access status of OSS buckets.
  Sends email notifications with the results.
  Supports multiple environments with different credentials.
  Excludes specified buckets from the check.

Installation
1. Clone the repo
2. Install the required libraries:
   pip3 install oss2 requests
   Aliyun and ossutil
4. Update the necessary fields (credentials, excluded_buckets should you have any you want to exclude, and email address settings.
   Note: The credentialed accounts require to have AliyunOSSReadOnlyAccess to the buckets in that environment. The script uses Access Keys for authentication.
         You can create a custom policy that only allows access from the IP of your resource to further lock down access and avoid unauthorized usage. 
5. Run the script: python check_buckets.py

Auto-execute/scheduling
You can run this on maxcompute or on a schedule task on any servers you have.

License
This project is licensed under the MIT License.

Feel free to customize this template to better fit your project!
