import base64
import boto3
import json
import os

from email.message import EmailMessage
from passgen import generate_password

env_file = open("temp_env.txt")
target_env = env_file.read()
target_env = target_env.replace("\n","")

user_file = open("temp_user.txt")
target_user = user_file.read()
target_user = target_user.strip()
target_user = target_user.replace("\n","")

iam_client = boto3.client('iam')
response = ""

try:
	response = iam_client.get_user(UserName=target_user)
except Exception as e:
	if "cannot be found" in str(e) or "invalid" in str(e):
		print(f'\nERROR: User account {target_user} is invalid\n')


if response:
	tag_response = iam_client.list_user_tags(UserName=target_user)
	target_email = ""

	if len(tag_response['Tags']) == 0:
		print(f'\nERROR: User account {target_user} does not have tags or has incorrectly formatted tags\n')
	else:
		for tag in tag_response['Tags']:
			if tag['Key']=="email":
				target_email = tag['Value']

	if target_email:
		pwd = generate_password()
		response = iam_client.update_login_profile(UserName=target_user,Password=pwd,PasswordResetRequired=True)
		print(f'\nPassword for user account {target_user} in {target_env} has been reset and an email containing a temporary password has been sent\n')

		pwd_subject = f'pwrd - {target_environment} AWS'
		pwd_message = pwd

		email = EmailMessage()
		email["From"] = "cloudnoreply@deltek.com"
		email["To"] = target_email
		email["Subject"] = pwd_subject
		email.set_content(pwd_message, subtype="html")

		smtp = smtplib.SMTP("smtp.gss.mydeltek.local")
		smtp.sendmail("cloudnoreply@deltek.com", target_email, email.as_string())
	else:
		print(f'\nERROR: User account {target_user} does not have an email tag or has an incorrectly formatted email tag\n')