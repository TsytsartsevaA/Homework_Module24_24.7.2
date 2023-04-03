import os
from dotenv import load_dotenv

not_valid_email = '12345@mail.com'
not_valid_password = '12345'
not_valid_key = '1'

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')