import json
import os
from datetime import datetime
from typing import Dict, List

import pytz
import yaml

from .manager.group_chat_manager import GroupChatManager

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class HourCallGroupConfig:
    """Stores group config of hour call"""
    DEFAULT_CONFIG = {'group_id': 0, 'enabled': True, 'smart_call': 1, 'do_not_disturb': [1, 5]}

    def __init__(self, group_config=None, default_config=None):
        if group_config is None:
            group_config = HourCallGroupConfig.DEFAULT_CONFIG
        self.group_id = group_config.get('group_id', default_config and default_config.group_id)
        self.enabled = group_config.get('enabled', default_config and default_config.enabled)
        self.smart_call = group_config.get('smart_call', default_config and default_config.smart_call)
        self.do_not_disturb = group_config.get('do_not_disturb', default_config and default_config.do_not_disturb)


class HourCallManager:
    """Manager of group hour call"""

    def __init__(self):
        # config files
        self.config = {}
        self.hour_call = {}

        # configs
        self.data_driver: str = 'MEMORY'
        self.super_user: List[int] = []
        self.block_user: List[int] = []
        self.groups: Dict[int, HourCallGroupConfig] = {}

        # cache data
        self.enabled_groups: List[int] = []

        # data manager
        self.group_chat_manager: GroupChatManager = GroupChatManager()

    def reload_config(self):
        """reload settings and hour call config, and build chat coutn manager
        """
        with open(CURRENT_DIR + '/constant.yml', encoding='utf-8') as fp:
            # support PyYAML before 5.1
            if hasattr(yaml, 'FullLoader'):
                self.config = yaml.load(fp, Loader=yaml.FullLoader)
            else:
                self.config = yaml.load(fp)

        with open(CURRENT_DIR + '/config.json', mode='r', encoding='utf-8') as fp:
            self.hour_call = json.load(fp)

        self.data_driver = self.config.get('data_driver', self.data_driver)
        self.super_user = self.config.get('super_user', self.super_user)
        self.block_user = self.config.get('block_user', self.block_user)

        # pick default config
        default_config = HourCallGroupConfig()
        for group in self.config.get('groups'):
            if group.get('group_id', None) == 0:
                default_config = HourCallGroupConfig(group, default_config)
                break

        # build group config map
        if default_config.enabled:
            self.groups[0] = default_config
        for group in self.config.get('groups'):
            group_id = group.get('group_id')
            if group_id and group_id != 0:
                hour_call_group_config = HourCallGroupConfig(group, default_config)
                if hour_call_group_config.enabled:
                    self.groups[group_id] = hour_call_group_config

        # cache enabled groups
        self.enabled_groups = []
        for group_id in self.groups:
            if self.groups[group_id].enabled:
                self.enabled_groups.append(group_id)

        # build chat data manager
        if self.data_driver == 'FILE':
            from .manager.group_chat_manager_file import GroupChatManagerFile
            self.group_chat_manager = GroupChatManagerFile()
            self.group_chat_manager.load()
        elif self.data_driver == 'REDIS':
            from .manager.group_chat_manager_redis import GroupChatManagerRedis
            self.group_chat_manager = GroupChatManagerRedis()

    def get_hour_call(self):
        """pick an hour call from config.json and change everyday"""
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        hc_groups = self.hour_call["HOUR_CALLS"]
        g = hc_groups[now.day % len(hc_groups)]
        return self.hour_call[g]

    @staticmethod
    def is_in_period(period: List[int], now):
        """determines if now is in the period"""
        if period is None:
            return False
        if len(period) == 0:
            return False
        elif len(period) == 1:
            if now > period[0]:
                return True
        else:
            start = period[0]
            end = period[1]
            if start <= now <= end:
                return True
            if start >= end:
                if start <= now <= 24 or 0 <= now <= end:
                    return True
        return False

    def do_not_disturb(self, group_id, now):
        """check if current period should not be distributed"""
        group = self.groups.get(group_id) or self.groups.get(0)
        return HourCallManager.is_in_period(group.do_not_disturb, now)

    def should_not_call(self, group_id):
        """check if current group should not be called"""
        group = self.groups.get(group_id) or self.groups.get(0)
        smart_call = group.smart_call or 0
        return self.group_chat_manager.get_chat_count(group_id) <= smart_call


hour_call_manager = HourCallManager()
hour_call_manager.reload_config()
