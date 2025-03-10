import subprocess
import pytest
from group_management.redis import RedisConnection
from redis.client import Redis

def stop_redis_container():
    # Redisコンテナを停止する
    subprocess.run(["docker", "stop", "redis"], check=True)

def test_init_redis(app):
    """Test init_redis function"""
    
    # Test case 18: Test redis type is redis
    with app.app_context():
        app.config["CACHE_TYPE"] = "redis"
        obj = RedisConnection()
        assert obj.redis_type == "redis"
    
    # Test case 19: Test redis type is sentinel
    with app.app_context():
        app.config["CACHE_TYPE"] = "sentinel"
        obj = RedisConnection()
        assert obj.redis_type == "sentinel"
        
def test_connection(app):
    """Test connection function"""
    
    # Test case 20: Test redis type is redis
    with app.app_context():
        app.config["CACHE_TYPE"] = "redis"
        obj = RedisConnection()
        store = obj.connection(0)
        assert store is not None
        assert type(store) == Redis
    
    # Test case 21: Test redis type is sentinel
    with app.app_context():
        app.config["CACHE_TYPE"] = "sentinel"
        obj = RedisConnection()
        store = obj.connection(0)
        assert store is not None
        assert type(store) == Redis
        
    # Test case 22: Test redis type is invalid
    with app.app_context():
        app.config["CACHE_TYPE"] = "test"
        obj = RedisConnection()
        store = obj.connection(0)
        assert store is None

    # Test case 23: Test redis DB is 16
    with app.app_context():
        app.config["CACHE_TYPE"] = "redis"
        obj = RedisConnection()
        store = obj.connection(16)
        assert store is not None
        assert type(store) == Redis

def test_redis_connection(app):
    """Test redis_connection function"""
    
    # Test case 24: connection is 0
    with app.app_context():
        app.config["CACHE_TYPE"] = "redis"
        obj = RedisConnection()
        store = obj.redis_connection(0)
        assert store is not None
        assert type(store) == Redis
    
    # Test case 25: connection is 16
    with app.app_context():
        app.config["CACHE_TYPE"] = "redis"
        obj = RedisConnection()
        store = obj.redis_connection(16)
        assert store is not None
        assert type(store) == Redis

    # Test case 26: Redis is not running
    with app.app_context():
        app.config["CACHE_TYPE"] = "redis"
        obj = RedisConnection()
        store = obj.redis_connection(0)
        assert store is not None
        assert type(store) == Redis
        
    # Test case 27: Redis enviroment is sentinel
    with app.app_context():
        app.config["CACHE_TYPE"] = "sentinel"
        obj = RedisConnection()
        store = obj.redis_connection(0)
        assert store is not None
        assert type(store) == Redis

    # Test case 28: REDIS_URL is invalid
    with app.app_context():
        app.config["REDIS_URL"] = "test"
        app.config["CACHE_TYPE"] = "redis"
        with pytest.raises(ValueError) as e:
            obj = RedisConnection()
            store = obj.redis_connection(0)
        assert str(e.value) == "Redis URL must specify one of the following schemes (redis://, rediss://, unix://)"
        
def test_sentinel_connection(app):
    """Test sentinel_connection function"""
    
    # Test case 29: connection is 0
    with app.app_context():
        app.config["CACHE_TYPE"] = "sentinel"
        obj = RedisConnection()
        store = obj.sentinel_connection(0)
        assert store is not None
        assert type(store) == Redis
    
    # Test case 30: connection is 16
    with app.app_context():
        app.config["CACHE_TYPE"] = "sentinel"
        obj = RedisConnection()
        store = obj.sentinel_connection(16)
        assert store is not None
        assert type(store) == Redis
															
    # Test case 31: Redis Sentinel is not running
    # note: stop all redis containers before running this test
    with app.app_context():
        app.config["CACHE_TYPE"] = "sentinel"
        obj = RedisConnection()
        store = obj.sentinel_connection(0)
        assert store is not None
        assert type(store) == Redis

    # Test case 32: Redis enviroment is redis
    with app.app_context():
        app.config["CACHE_TYPE"] = "redis"
        obj = RedisConnection()
        store = obj.sentinel_connection(0)
        assert store is not None
        assert type(store) == Redis
    
    # Test case 33: REDIS_SENTINELS is invalid
    with app.app_context():
        app.config["REDIS_SENTINELS"] = [("invalid-sentinel-service.re","2637")]
        app.config["CACHE_TYPE"] = "sentinel"
        obj = RedisConnection()
        store = obj.sentinel_connection(0)
        assert store is not None
        assert type(store) == Redis
