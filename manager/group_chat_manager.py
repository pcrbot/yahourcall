import time
from multiprocessing import Lock


class GroupChatManager:
    """Group chat manager, calculates chat count in specified duration(default 3600 seconds)."""
    LOCK = Lock()

    def __init__(self, duration=None, prefix='groupchat'):
        # structure: {group_id: {int(timestamp / duration): count}}
        self.chats = {}
        # statistical period in seconds
        self.duration = duration or 3600
        self.prefix = prefix

        self.begin_at = time.time()

    def get_current_period(self, offset=0) -> int:
        # return int((time.time() - self.begin_at) / self.duration) * self.duration
        return int((time.time() + offset) / self.duration) * self.duration

    def add_chat(self, group_id) -> int:
        """Add a chat and return chat count in current period"""
        period = self.get_current_period()

        with GroupChatManager.LOCK:
            chats = self.chats.get(group_id, {})
            count = chats.get(period, 0)
            count += 1
            chats[period] = count
            self.chats[group_id] = chats
            return count

    def get_chat_count(self, group_id) -> int:
        """Get chat count in current period and evict old counts"""
        if group_id not in self.chats:
            return 0

        period = self.get_current_period(offset=-5)
        chats = self.chats[group_id]
        if len(chats) > 1:
            # evict old chat count
            for key in list(chats):
                if key != period:
                    del chats[key]
        return chats.get(period, 0)

    def dump(self):
        """Dump to somewhere"""
        pass

    def load(self):
        """Load from somewhere"""
        pass
