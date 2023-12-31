import boto3
import json
import os

#initializing params
method_file = open("temp_method.txt")
update_method = method_file.read()
update_method = update_method.replace("\n","").strip()

env_file = open("temp_env.txt")
target_environment = env_file.read()
target_environment = target_environment.replace("\n","")

target_user_file = open("temp_user.txt")
target_user = target_user_file.read()
target_user = target_user.replace("\n","")

emailref_file = open("email_reference.json")
emailref_json = json.loads(emailref_file.read())

setup_removal = os.environ["Setup Group Removal"]


#helper functions
def check_user_existence(username):
	iam_client = boto3.client('iam')
	response = ""
	
	try:
		response = iam_client.get_user(UserName=username)
	except Exception as e:
		if "cannot be found" in str(e) or "invalid" in str(e):
			response = ""

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

target_user_check = check_user_existence(target_user)

if not target_user_check:
	with open("target_user_errors.txt", 'a') as tuser_error:
		append_message = f'{target_user} does not exist in {target_environment}\n'
		tuser_error.write(append_message)
	print(f'\n========================\nINVALID TARGET USER: {target_user} - SKIPPING {target_environment}\n========================\n')
	exit(0)


mfa_check = check_mfa_existence(target_user)

if mfa_check:

	if update_method == "replicate":
		source_user = os.environ["Source User"]
		source_user_response = check_user_existence(source_user)

		if source_user_response:
			source_user_groups = iam_client.list_groups_for_user(UserName=source_user,MaxItems=1000)

			for group in source_user_groups['Groups']:
				group_add_response = iam_client.add_user_to_group(GroupName=group['GroupName'], UserName=target_user)
				print(f'\n{group_add_response}\n')
				print(f'{target_user} has been added to {group["GroupName"]}\n')
		else:
			with open("source_user_errors.txt", 'a') as suser_error:
				append_message = f'{source_user} does not exist in {target_environment}\n'
				suser_error.write(append_message)
			print(f'\n========================\nINVALID SOURCE USER: {source_user} - SKIPPING {target_environment}\n========================\n')
				
	elif update_method == "custom":
		groups = os.environ["Groups"]
		groups_list = groups.split("\n")

		for group in groups_list:
			check_group_existence(group)
			group_add_response = iam_client.add_user_to_group(GroupName=group,UserName=target_user)
			print(f'\n{group_add_response}\n')
			print(f'{target_user} has been added to {group}\n')

	if "Yes" in setup_removal:
		setup_group = emailref_json[target_environment]['setup']
		setup_removal_response = iam_client.remove_user_from_group(GroupName=setup_group,UserName=target_user)
		print(f'{target_user} has been removed from {setup_group}\n')

else:
	print(f'ERROR: User {target_user} does not have MFA configured, permission update will not proceed')