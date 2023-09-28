import boto3
import json
import time
import os

env_file = open("temp_env.txt")
target_env = env_file.read()

def main(target_env):
	ssm_file = open("ssm_send_reset.json")
	ssm_json = ssm_file.read()

	pwd_file = open("temp_password.txt")
	pwd = pwd_file.read()
	pwd_split = pwd.split(",")
	pwd = pwd_split[0][2:-1]
	email = pwd_split[1][2:-3]

	emailer_instance = "i-0e0ef4b5f42929f4e"

	ssm_doc_name = 'InfraSRE-IAMReset'
	ssm_client = boto3.client('ssm', region_name="us-east-1")

	print("SSM CREATION STEP")
	ssm_create_response = ssm_client.create_document(Content = ssm_json, Name = ssm_doc_name, DocumentType = 'Command', DocumentFormat = 'JSON', TargetType =  "/AWS::EC2::Instance")
	print(ssm_create_response)

	print("\n\nSSM RUN STEP")
	ssm_run_response = ssm_client.send_command(InstanceIds = [emailer_instance], DocumentName=ssm_doc_name, DocumentVersion="$DEFAULT", TimeoutSeconds=120, Parameters={'environment':[target_env], 'password':[pwd], 'email':[email]})
	print(ssm_run_response)

	print("\n\nSSM DELETION STEP")
	ssm_delete_response = ssm_client.delete_document(Name=ssm_doc_name)
	print(ssm_delete_response)

main(target_env)
