import redis

from .group_chat_manager import GroupChatManager


redis_cache = redis.Redis(connection_pool=redis.ConnectionPool())


class GroupChatManagerRedis(GroupChatManager):
    """Redis implementation for the group chat manager,
    use manager.prefix as the redis key,
    also uses manager.duration for redis expire time."""

    def get_redis_key(self, group_id) -> str:
        return '{}:{}:{}'.format(self.prefix, group_id, self.get_current_period())

    def add_chat(self, group_id: int) -> int:
        redis_cache.set(self.get_redis_key(group_id), 0, ex=self.duration, nx=True)
        return redis_cache.incr(self.get_redis_key(group_id), 1)

    def get_chat_count(self, group_id: int) -> int:
        return int(redis_cache.get(self.get_redis_key(group_id)) or 0)
