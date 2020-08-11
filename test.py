import sys
import time
import unittest
from pathlib import Path


class TestHourCallManager(unittest.TestCase):

    def setUp(self) -> None:
        """Simulate 100 groups with 100 messages per second"""
        self.groups = 100
        self.message_per_group = 100

    def run_with_manager(self, group_chat_manager, group_id):
        def fun(manager):
            for i in range(self.message_per_group):
                time.sleep(.01)
                manager.add_chat(group_id)

        from threading import Thread
        procs = [Thread(target=fun, args=(group_chat_manager,)) for _ in range(self.groups)]
        for p in procs:
            p.start()
        for p in procs:
            p.join()

    def testMemory(self):
        begin_at = time.time()
        group_id = 10000

        from manager.group_chat_manager import GroupChatManager
        manager: GroupChatManager = GroupChatManager(5)
        self.run_with_manager(manager, group_id)
        # assert the result is correct
        self.assertEqual(manager.get_chat_count(group_id), self.groups * self.message_per_group)
        print('test memory finished in {:.4f} seconds'.format(time.time() - begin_at))

    def testFile(self):
        begin_at = time.time()
        group_id = 10000

        from manager.group_chat_manager_file import GroupChatManagerFile
        manager = GroupChatManagerFile(30)

        self.run_with_manager(manager, group_id)
        # assert the result is correct
        self.assertEqual(manager.get_chat_count(group_id), self.groups * self.message_per_group)
        print('test file finished in {:.4f} seconds'.format(time.time() - begin_at))
    #
    #     time.sleep(10)
    #     # assert count before is expired
    #     self.assertEqual(manager.get_chat_count(group_id), 0)
    #     self.run_with_manager(manager, group_id)
    #     # assert the result is correct
    #     self.assertEqual(manager.get_chat_count(group_id), self.groups * self.message_per_group)

    def testRedis(self):
        begin_at = time.time()
        group_id = 10000

        from manager.group_chat_manager_redis import GroupChatManagerRedis
        manager = GroupChatManagerRedis(30)

        # assert count before is expired
        self.assertEqual(manager.get_chat_count(group_id), 0)
        self.run_with_manager(manager, group_id)
        # assert the result is correct
        self.assertEqual(manager.get_chat_count(group_id), self.groups * self.message_per_group)
        print('test redis finished in {:.4f} seconds'.format(time.time() - begin_at))


if __name__ == '__main__':
    # trick parent path
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[1]
    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError:  # Already removed
        pass
    __package__ = 'yahourcall'

    # test
    unittest.main()
