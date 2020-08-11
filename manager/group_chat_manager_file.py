import os
import pickle

from .group_chat_manager import GroupChatManager

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class GroupChatManagerFile(GroupChatManager):
    """File implementation for the chat manager,
    use manager.prefix as the data file name."""
    SAVE_TO = "{}/{}.data"
    DUMP_EVERY = 1000

    def add_chat(self, group_id):
        count = super(GroupChatManagerFile, self).add_chat(group_id)
        if count > GroupChatManagerFile.DUMP_EVERY:
            self.dump()
        return count

    def dump(self):
        with open(GroupChatManagerFile.SAVE_TO.format(CURRENT_DIR, self.prefix), 'wb') as f:
            pickle.dump(self.chats, f)

    def load(self):
        with open(GroupChatManagerFile.SAVE_TO.format(CURRENT_DIR, self.prefix), 'rb') as f:
            self.chats = pickle.load(f)
