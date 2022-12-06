# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU GPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: speedtest
# Description: Tests your internet speed via speedtest.net
# Author: iamnalinor
# Commands:
# .speedtest
# ---------------------------------------------------------------------------------


# Tests your internet speed via speedtest.net
# Copyright © 2022 https://t.me/nalinor

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# meta developer: @nalinormods
# requires: speedtest-cli

# Modified by Penggrin, Morri
# All credits goes to the original author

from typing import Tuple

from telethon import TelegramClient
from telethon.tl.custom import Message
from telethon.tl.functions.channels import JoinChannelRequest

import speedtest  # pylint: disable=import-self

from .. import loader, utils


# noinspection PyCallingNonCallable,PyAttributeOutsideInit
# pylint: disable=not-callable,attribute-defined-outside-init,invalid-name
@loader.tds
class SpeedtestMod(loader.Module):
    """Tests your internet speed via speedtest.net"""

    strings = {
        "name": "Speedtest",
        "author": "@nalinormods",
        "running": "<emoji document_id=5327790373865530387>🫥</emoji> <b>Speed Test on</b> <b>speedtest.net ...</b>",
        "result": (
            "<emoji document_id=5213239047710843061>⬆️</emoji><code> Speedtest® Connections:</code>\n\n"
            "<emoji document_id=5783105032350076195>📶</emoji><b> Speed: <code>{download}</code> МБ/с</b> | <code>{upload}</code> МБ/с</b>\n"
            "<emoji document_id=5974081491901091242>🕒</emoji><b> Ping: <code>{ping}</code> мс</b>"
        ),
    }

    strings_ru = {
        "_cls_doc": "Проверяет скорость интернета на вашем сервере",
        "_cmd_doc_speedtest": "Проверить скорость интернета",
        "running": "<emoji document_id=5327790373865530387>🫥</emoji> <b>Тест скорости на</b> <b>speedtest.net ...</b>",
        "result": (
            "<emoji document_id=5213239047710843061>⬆️</emoji><code> Speedtest® Connections:</code>\n\n"
            "<emoji document_id=5783105032350076195>📶</emoji><b> Скорость: <code>{download}</code> МБ/с</b> | <code>{upload}</code> МБ/с</b>\n"
            "<emoji document_id=5974081491901091242>🕒</emoji><b> Пинг: <code>{ping}</code> мс</b>"
        ),
    }

    async def client_ready(self, client: TelegramClient, _):
        """client_ready hook"""
        await client(JoinChannelRequest(channel=self.strings("author")))

    async def speedtestcmd(self, message: Message):
        """Run speedtest"""
        m = await utils.answer(message, self.strings("running"))
        results = await utils.run_sync(self.run_speedtest)
        await utils.answer(
            m,
            self.strings("result").format(
                download=round(results[0] / 1024 / 1024),
                upload=round(results[1] / 1024 / 1024),
                ping=round(results[2], 3),
            ),
        )

    @staticmethod
    def run_speedtest() -> Tuple[float, float, float]:
        """Speedtest using `speedtest` library"""
        s = speedtest.Speedtest()  # pylint: disable=no-member
        s.get_servers()
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
        return res["download"], res["upload"], res["ping"]