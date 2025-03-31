# -*- coding: utf-8 -*-
import asyncio
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
        async def on_ready(self):
                    _log.info(f"robot 「{self.robot.name}」 on_ready!")

        async def on_group_at_message_create(self, message: GroupMessage):
            print(repr(message.content))
            print(message)
            if message.content == " /开灯 " :
                messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0, 
                msg_id=message.id,
                content=f"已开灯")
                _log.info(messageResult)

            if message.content == " /关灯 " :
                messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0, 
                msg_id=message.id,
                content=f"已关灯")
                _log.info(messageResult)

            if message.content == " /打开窗帘 " :
                messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0, 
                msg_id=message.id,
                content=f"已打开窗帘")
                _log.info(messageResult)

            if message.content == " /关闭窗帘 " :
                messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0, 
                msg_id=message.id,
                content=f"已关闭窗帘")
                _log.info(messageResult)

if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
