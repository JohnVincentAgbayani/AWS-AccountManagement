import smtplib
import boto3
import json
import os

from email.message import EmailMessage
from passgen import generate_password

# username = os.environ["Username"]
# user_email = os.environ["Email"]
# employeeid = os.environ["Employee ID"]
# snow_case = os.environ["ServiceNow Case"]
# user_pwd = generate_password()

# env_file = open("temp_env.txt")
# target_environment = env_file.read()
# target_environment = target_environment.replace("\n","")

# emailref_file = open("email_reference.json")
# emailref_json = json.loads(emailref_file.read())

# def check_user_existence(username):
# 	iam_client = boto3.client('iam')
	
# 	try:
# 		response = iam_client.get_user(UserName=username)
# 	except Exception as e:
# 		if "cannot be found" in str(e) or "invalid" in str(e):
# 			response = ""

# 	return response   

# #main execution
# iam_client = boto3.client('iam')

# user_exists = check_user_existence(username)

# if user_exists:
# 	print(f'ERROR: {username} already exists in {target_environment}, aborting creation')
# else:
# 	iam_create_response = iam_client.create_user(UserName=username,Tags=[{'Key': 'email','Value': user_email},{'Key': 'employeeID','Value': employeeid},{'Key': 'snowcase','Value': snow_case}])
# 	print(f'\n{iam_create_response}\n')

# 	iam_profile_response = iam_client.create_login_profile(UserName=username,Password=user_pwd,PasswordResetRequired=True)
# 	print(f'\n{iam_profile_response}\n')

# 	setup_group = emailref_json[target_environment]['setup']
# 	group_add_response = iam_client.add_user_to_group(GroupName=setup_group, UserName=username)
# 	print(f'\n{group_add_response}\n')

# 	if iam_create_response and iam_profile_response and group_add_response:
# 		print(f'\nUser account {username} has been created in {target_environment} and has been added into {setup_group}\n')


pwd_subject = f'pwrd - test AWS'
message = "<strong>Hello</strong>, <em>world</em>!"

email = EmailMessage()
email["From"] = "cloudnoreply@deltek.com"
email["To"] = "johnvincentagbayani@deltek.com"
email["Subject"] = "test subject"
email.set_content(message, subtype="html")

sender = "cloudnoreply@deltek.com"
recipient = "johnvincentagbayani@deltek.com"

smtp = smtplib.SMTP("smtp.gss.mydeltek.local")
smtp.sendmail(sender, recipient, email.as_string())