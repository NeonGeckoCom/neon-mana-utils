# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import unittest

from mycroft_bus_client import Message
from ovos_utils.messagebus import FakeBus

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from neon_mana_utils.bus_api import get_stt, get_tts, get_response


class TestBusApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_bus = FakeBus()

    def test_get_stt(self):
        test_file = os.path.join(os.path.dirname(__file__),
                                 "audio", "stop.wav")
        msg = None

        def handler(message: Message):
            nonlocal msg
            msg = message
            self.test_bus.emit(message.reply(message.context["ident"],
                                             {"success": True}))

        self.test_bus.on("neon.get_stt", handler)
        resp = get_stt(self.test_bus, test_file)
        self.assertIsInstance(msg, Message)
        self.assertIsInstance(resp, Message)

        self.assertEqual(msg.context.pop('source'),
                         resp.context.pop('destination'))
        self.assertEqual(msg.context.pop('destination'),
                         resp.context.pop('source'))
        self.assertEqual(msg.context, resp.context)
        self.assertTrue(resp.data["success"])
        self.assertIsInstance(msg.data["audio_data"], str)

    def test_get_tts(self):
        msg = None

        def handler(message: Message):
            nonlocal msg
            msg = message
            self.test_bus.emit(message.reply(message.context["ident"],
                                             {"success": True}))

        self.test_bus.on("neon.get_tts", handler)
        resp = get_tts(self.test_bus, "test input string")
        self.assertIsInstance(msg, Message)
        self.assertIsInstance(resp, Message)

        self.assertEqual(msg.context.pop('source'),
                         resp.context.pop('destination'))
        self.assertEqual(msg.context.pop('destination'),
                         resp.context.pop('source'))
        self.assertEqual(msg.context, resp.context)
        self.assertTrue(resp.data["success"])
        self.assertEqual(msg.data["text"], "test input string")

    def test_get_response(self):
        msg = None

        def handler(message: Message):
            nonlocal msg
            msg = message
            self.test_bus.emit(message.reply("klat.response", {"success": True}))

        self.test_bus.on("recognizer_loop:utterance", handler)
        resp = get_response(self.test_bus, "This is a test")
        self.assertIsInstance(msg, Message)
        self.assertIsInstance(resp, Message)
        self.assertTrue(resp.data["success"])
        self.assertIn("klat_data", msg.context)
        self.assertEqual(msg.data["utterances"], ["This is a test"])


if __name__ == '__main__':
    unittest.main()
