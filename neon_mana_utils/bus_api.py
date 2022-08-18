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
import base64
import os
from time import time
from typing import Optional
from mycroft_bus_client import MessageBusClient, Message
from neon_utils.file_utils import encode_file_to_base64_string


def get_stt(messagebus_client: MessageBusClient,
            audio_path: Optional[str] = None,
            audio_bytes: Optional[bytes] = None,
            lang: str = "en-us") -> Optional[Message]:
    """
    Send audio to the speech module and return the transcription response
    :param messagebus_client: Running MessageBusClient
    :param audio_path: Path to audio file to transcribe
    :param audio_bytes: Audio bytes to transcribe
    :param lang: language of input audio
    :returns: Response Message from speech module (None if no response)
    """
    ident = str(time())
    audio_data = encode_file_to_base64_string(audio_path) if audio_path else \
        base64.b64encode(audio_bytes).decode("utf-8")
    data = {"audio_data": audio_data,
            "lang": lang}
    context = {"ident": ident,
               "source": ["mana"],
               "destination": ["speech"]}
    resp = messagebus_client.wait_for_response(Message("neon.get_stt",
                                                       data, context),
                                               ident, 15)
    return resp


def get_tts(messagebus_client: MessageBusClient,
            text_to_speak: str = None,
            speaker: Optional[dict] = None):
    """
    Send text to the audio module and return the synthesis response
    :param messagebus_client: Running MessageBusClient
    :param text_to_speak: String to synthesize
    :param speaker: Dict speaker data associated with request
    :returns: Response Message from audio module (None if no response)
    """
    ident = str(time())
    data = {"text": text_to_speak}
    context = {"ident": ident,
               "speaker": speaker,
               "source": ["mana"],
               "destination": ["audio"]}
    resp = messagebus_client.wait_for_response(Message("neon.get_tts",
                                                       data, context),
                                               ident, 15)
    return resp


def audio_input(messagebus_client: MessageBusClient,
                audio_path: Optional[str] = None,
                audio_bytes: Optional[bytes] = None,
                lang: str = "en-us") -> Optional[Message]:
    """
    Send audio to the speech module for skills processing
    :param messagebus_client: Running MessageBusClient
    :param audio_path: Path to audio file to transcribe
    :param audio_bytes: Audio bytes to transcribe
    :param lang: language of input audio
    :returns: Response Message from speech module (None if no response)
    """
    audio_file = os.path.expanduser(audio_path) if audio_path else None
    if audio_file and not os.path.isfile(audio_file):
        raise FileNotFoundError(audio_file)
    if not any((audio_file, audio_bytes)):
        raise ValueError("No file or audio bytes specified")
    ident = str(time())
    audio_data = encode_file_to_base64_string(audio_file) if audio_file else \
        base64.b64encode(audio_bytes).decode("utf-8")
    data = {"audio_data": audio_data,
            "lang": lang}
    context = {"ident": ident,
               "source": ["mana"],
               "destination": ["speech"]
               }
    resp = messagebus_client.wait_for_response(Message("neon.audio_input",
                                                       data, context),
                                               ident, 15)
    return resp


def get_response(messagebus_client: MessageBusClient,
                 utterance: str, lang: str = "en-us") -> Optional[Message]:
    """
    Send text to the skills module and return the response from the audio module
    :param messagebus_client: Running MessageBusClient
    :param utterance: input to pass to Intent Service
    :param lang: language of input audio
    :returns: klat.response Message from audio module (None if no response)
    """
    ident = str(time())
    data = {
        "utterances": [utterance],
        "lang": lang
    }
    context = {
        "client_name": "neon_cli",
        "client": "cli",
        "source": ["mana"],
        "destination": ["skills"],
        "ident": ident,
        "neon_should_respond": True,
        "username": "local",
        "klat_data": {"key": "val"}
    }
    resp = messagebus_client.wait_for_response(
        Message("recognizer_loop:utterance",
                data, context), "klat.response", 10)
    return resp
