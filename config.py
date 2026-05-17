from dotenv import load_dotenv
import os


load_dotenv()
ENGINESQL = os.environ.get("DATABASE_URL")
TELETOKEN = os.environ.get("TELETOKEN")


print(ENGINESQL)