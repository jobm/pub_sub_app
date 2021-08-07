import redis

redis_conn = redis.Redis(host="redis", charset="utf-8", decode_responses=True)
