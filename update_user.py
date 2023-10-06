import boto3
import json
import os

update_method = "replicate"
target_environment = "deltekdev"
source_user = "johnvincentagbayani"
target_user = "test_reset_user"
groups = "AWSAdministrator\nDCO_AWSAcct_Standard_Users\nDCO_IAM_DefaultPolicy\nIAM_IdleAccount_Exception"

emailref_file = open("email_reference.json")
emailref_json = json.loads(emailref_file.read())

#helper functions
def check_user_existence(username):
	iam_client = boto3.client('iam')
	response = ""
	
	try:
		response = iam_client.get_user(UserName=username)
	except Exception as e:
		if "cannot be found" in str(e) or "invalid" in str(e):
			print(f'\n\nINVALID USERNAME: {username}\n\n')
			exit(1)

	return response

def check_mfa_existence(username):
	iam_client = boto3.client('iam')
	response = iam_client.list_mfa_devices(UserName=username)
	has_mfa = 0

	if response['MFADevices']:
		has_mfa = 1

	return has_mfa

def check_group_existence(groupname):
	iam_client = boto3.client('iam')
	response = ""

	try:
		response = iam_client.get_group(GroupName=groupname)
	except Exception as e:
		if "cannot be found" in str(e) or "invalid" in str(e):
			print(f'\n\nINVALID GROUP: {groupname}\n\n')
			exit(1)

	return response


#main execution
iam_client = boto3.client('iam')

check_user_existence(target_user)
mfa_check = check_mfa_existence(target_user)
if mfa_check:

	if update_method == "replicate":

		source_user_response = check_user_existence(source_user)

		if source_user_response:
			source_user_groups = iam_client.list_groups_for_user(UserName=source_user,MaxItems=1000)

			for group in source_user_groups['Groups']:
				group_add_response = iam_client.add_user_to_group(GroupName=group['GroupName'], UserName=target_user)
				print(f'\n{group_add_response}\n')
				print(f'{target_user} has been added to {group["GroupName"]}\n')
				

	elif update_method == "custom groups":

		groups_list = groups.split("\n")
		for group in groups_list:
			check_group_existence(group)
			group_add_response = iam_client.add_user_to_group(GroupName=group,UserName=target_user)
			print(f'\n{group_add_response}\n')
			print(f'{target_user} has been added to {group}\n')

	setup_group = emailref_json[target_environment]['setup']
	setup_removal_response = iam_client.remove_user_from_group(GroupName=setup_group,UserName=target_user)
	print(f'{target_user} has been removed from {setup_group}\n')
else:
	print(f'ERROR: User {target_user} does not have MFA configured, permission update will not proceed')