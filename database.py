import motor.motor_asyncio

from config import MONGO_URL

mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db = mongo.zaid_ai

conversations = db.conversations
stats = db.stats
