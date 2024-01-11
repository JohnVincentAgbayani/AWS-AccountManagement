import secrets
import string

def generate_password():
	letters = string.ascii_letters
	digits = string.digits
	special_chars = "!@#$%^&*()_+-=[]{}|'"
	alphabet = letters + digits + special_chars

	pwd = ''
	has_upper = 0
	has_lower = 0
	has_number = 0
	has_special = 0


	while has_upper+has_lower+has_number+has_special<4:

		pwd = ''
		has_upper = 0
		has_lower = 0
		has_number = 0
		has_special = 0

		for char in range(16):
			char = secrets.choice(alphabet)
			pwd += char

			if char.islower():
				has_lower = 1
			elif char.isupper():
				has_upper = 1
			elif char.isnumeric():
				has_number = 1
			elif char in special_chars:
				has_special = 1
	return pwd