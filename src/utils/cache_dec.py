from functools import wraps
import hashlib
import inspect
import json
from src.init import redis_manager


def cache_dec(exp: int = 10):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            f_name = func.__name__
            k_name = hashlib.md5(f"{f_name}:{args}:{kwargs}".encode()).hexdigest()

            key_data = await redis_manager.get(f"fastapi_{f_name}_{k_name}")
            if key_data:
                return json.loads(key_data)
            if inspect.iscoroutinefunction(func):
                res = await func(*args, **kwargs)
            else:
                res = func(*args, **kwargs)
            if isinstance(res, list):
                redis_data = [n.model_dump() for n in res]
                redis_data = json.dumps(redis_data)
            else:
                print(res)
                redis_data = json.dumps(res)
            await redis_manager.set(f"fastapi_{f_name}_{k_name}", redis_data, exp)

            res = await func(*args, **kwargs)
            return res

        return wrapper

    return decorator
