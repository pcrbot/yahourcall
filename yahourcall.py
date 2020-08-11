from datetime import datetime

import nonebot
import pytz
from nonebot import NLPSession, logger, CommandSession

from .hour_call_manager import hour_call_manager

bot = nonebot.get_bot()

""" 对于 hoshino 用户，可以在本行前加一个 # ，并在下方nonebot.scheduler前加一个 # 以便其他插件管理
from hoshino import Service
sv = Service('yahourcall', enable_on_default=True, help_='另一个时报')
@sv.scheduled_job('cron', minute='0')
# """
@nonebot.scheduler.scheduled_job('cron', second='0')
async def hour_call():
    # get now hour
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    msg = hour_call_manager.get_hour_call()[now.hour]
    for group_id in hour_call_manager.enabled_groups:
        # skip default group(0) and sometimes None
        if not group_id:
            continue

        logger.info('<yahourcall> checking {}'.format(group_id))
        try:
            # group don't disturb
            if hour_call_manager.do_not_disturb(group_id, now.hour):
                logger.debug('<yahourcall> skipped since do not disturb')
                continue

            # group not active
            if hour_call_manager.should_not_call(group_id):
                logger.debug('<yahourcall> skipped since active {}'
                             .format(hour_call_manager.group_chat_manager.get_chat_count(group_id)))
                continue

            await bot.send_group_msg(group_id=group_id, message=msg)
        except Exception as e:
            logger.exception('<yahourcall> error', exc_info=e)


@nonebot.on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    user_id = session.event.user_id
    # ignore some user
    if hour_call_manager.should_ignore_user(user_id):
        return

    group_id = session.event.group_id
    group_ids = hour_call_manager.enabled_groups

    # this is a group chat with group id
    if group_id is not None:
        # record new group not in config and use default config
        if group_id not in group_ids and 0 in group_ids:
            group_ids.append(group_id)

        # record chat
        if group_id in group_ids:
            hour_call_manager.group_chat_manager.add_chat(group_id)
            logger.debug('<yahourcall> active {} is {}'
                         .format(group_id, hour_call_manager.group_chat_manager.get_chat_count(group_id)))


@nonebot.scheduler.scheduled_job('cron', minute='*/10')
async def dump_data():
    # useless call for memory and redis manager
    hour_call_manager.group_chat_manager.dump()


@nonebot.on_command('yahourcall')
async def reload_config(session: CommandSession):
    hour_call_manager.reload_config()
    logger.info('<yahourcall> admin {} reloaded config'.format(session.event.user_id))
    await bot.send_private_msg(user_id=session.event.user_id,
                               message='reloaded, enabled groups: {}'.format(hour_call_manager.enabled_groups))
