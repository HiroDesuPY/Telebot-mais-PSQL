from dotenv import load_dotenv
import os


load_dotenv()
TELETOKEN = os.getenv("TELETOKEN")
ENGINESQL = os.getenv('ENGINE')


print(ENGINESQL)