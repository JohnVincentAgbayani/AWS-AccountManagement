import base64
import boto3
import os

from passgen import generate_password

target_env = "deltekdev"
target_user = "test_reset_user"

def reset_password(target_env, target_user):

	target_user = target_user.strip()

	iam_client = boto3.client('iam')
	response = ""

	#PREPROCESSING
	try:
		response = iam_client.get_user(UserName=target_user)
	except Exception as e:
		if "cannot be found" in str(e) or "invalid" in str(e):
			print("Invalid username")


	if response:
		tag_response = iam_client.list_user_tags(UserName=target_user)
		if len(tag_response['Tags']) == 0:
			print("This user does not have tags")
		else:
			for tag in tag_response['Tags']:
				if tag['Key']=="email":
					target_email = tag['Value']

		if target_email:
			pwd = generate_password()
			response = iam_client.update_login_profile(UserName=target_user,Password=pwd,PasswordResetRequired=True)

			encoding_set = ["ascii", "utf-7", "utf-8"]

			for enc in encoding_set:
				pwd_bytes = pwd.encode(enc)
				pwd = base64.b64encode(pwd_bytes)
				pwd = pwd.decode(enc)
	return pwd


print(reset_password(target_env, target_user))
