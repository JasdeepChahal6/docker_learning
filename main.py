from fastapi import FastAPI
import redis
import os

app = FastAPI()

# connect to Redis using environment variable
redis_client = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379")
)

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello {name}!"}

@app.get("/cache/set/{key}/{value}")
def set_cache(key: str, value: str):
    redis_client.set(key, value, ex=60)  # expires in 60 seconds
    return {"message": f"Stored {key} = {value} for 60 seconds"}

@app.get("/cache/get/{key}")
def get_cache(key: str):
    value = redis_client.get(key)
    if value:
        return {"key": key, "value": value.decode("utf-8"), "source": "cache"}
    return {"key": key, "value": None, "source": "cache miss"}