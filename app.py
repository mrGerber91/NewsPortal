import redis
import os
import dotenv
from dotenv import load_dotenv

dotenv.load_dotenv()

r = redis.Redis(
    host='redis-13967.c325.us-east-1-4.ec2.cloud.redislabs.com',
    port=13967,
    password=os.getenv('REDIS_PASSWORD'),

)