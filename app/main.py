from imapTest import do_env
from dotenv import load_dotenv

load_dotenv()

print("Hello from Docker`s Python container!")
do_env()