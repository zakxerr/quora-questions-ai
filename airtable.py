import os
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv('.env')
api_key = os.environ.get("API_KEY")
base_id = os.environ.get('BASE_ID')







