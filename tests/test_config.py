# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2025 Neongecko.com Inc.
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

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from neon_mana_utils.config import get_config_dir, get_messagebus_config, get_event_filters


class TestConfig(unittest.TestCase):
    def test_get_config_dir(self):
        config_dir = get_config_dir()
        self.assertIsInstance(config_dir, str)
        self.assertTrue(os.path.isdir(config_dir))

    def test_get_messagebus_config(self):
        config = get_messagebus_config()
        self.assertEqual(set(config.keys()), {"host", "port", "route", "ssl"})

        config_dir = os.path.join(os.path.dirname(__file__), "config")
        config = get_messagebus_config(config_dir)
        self.assertEqual(set(config.keys()), {"host", "port", "route", "ssl"})
        self.assertEqual(config["host"], "127.0.0.1")
        self.assertEqual(config["port"], 18181)
        self.assertEqual(config["route"], "/test")
        self.assertTrue(config["ssl"])

    def test_get_event_filters(self):
        filters = get_event_filters()
        self.assertEqual(set(filters.keys()), {"include", "exclude"})

        config_dir = os.path.join(os.path.dirname(__file__), "config")
        filters = get_event_filters(config_dir)
        self.assertEqual(set(filters.keys()), {"include", "exclude"})
        self.assertEqual(filters["include"], ["neon."])
        self.assertEqual(filters["exclude"], ["connected"])


if __name__ == '__main__':
    unittest.main()
