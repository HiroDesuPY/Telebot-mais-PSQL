from dotenv import load_dotenv
import os


load_dotenv()
ENGINESQL = os.getenv("ENGINE")
TELETOKEN = os.getenv("TELETOKEN")


print(ENGINESQL)