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

from mycroft_bus_client import Message, MessageBusClient


def get_skills_list(bus: MessageBusClient) -> dict:
    """
    Get a list of skills from the SkillManager
    :param bus: Connected MessageBusClient to query
    :returns: dict of loaded skills
    """
    # TODO: Comp. to `intent.service.skills.get`?
    resp = bus.wait_for_response(
            Message("skillmanager.list",
                    context={"source": ["mana"],
                             "destination": ["skills"]}), "mycroft.skills.list")
    skills = resp.data if resp else None
    return skills


def deactivate_skill(bus: MessageBusClient, skill: str):
    """
    Request deactivation of a skill
    :param bus: Connected MessageBusClient to query
    :param skill: skill ID to deactivate
    """
    bus.emit(Message("intent.service.skills.deactivate", {'skill_id': skill},
                     context={"source": ["mana"],
                              "destination": ["skills"]}))


def activate_skill(bus: MessageBusClient, skill: str):
    """
    Request activation of a skill
    :param bus: Connected MessageBusClient to query
    :param skill: skill ID to activate
    """
    bus.emit(Message("intent.service.skills.activate", {'skill_id': skill},
                     context={"source": ["mana"],
                              "destination": ["skills"]}))


def get_active_skills(bus: MessageBusClient) -> list:
    """
    Get active skills from the intent service
    :param bus: Connected MessageBusClient to query
    :returns: list of active skills
    """
    msg = bus.wait_for_response(Message("intent.service.active_skills.get",
                                        context={"source": ["mana"],
                                                 "destination": ["skills"]}),
                                reply_type="intent.service.active_skills.reply")
    return msg.data.get('skills', list())


def get_adapt_manifest(bus: MessageBusClient, lang: str) -> list:
    """
    Get the manifest of registered Adapt intents
    :param bus: Connected MessageBusClient to query
    :param lang: BCP-47 lang code to get intents for
    """
    msg = bus.wait_for_response(Message("intent.service.adapt.manifest.get",
                                        {"lang": lang},
                                        context={"source": ["mana"],
                                                 "destination": ["skills"]}),
                                reply_type="intent.service.adapt.manifest")
    return msg.data.get('intents', list())


def get_adapt_intent(bus: MessageBusClient, lang: str,
                     utterance: str) -> dict:
    """
    Get an Adapt intent for the input utterance
    :param bus: Connected MessageBusClient to query
    :param lang: language of utterance
    :param utterance: utterance to check
    :returns: dict Padatious intent
    """
    msg = bus.wait_for_response(Message("intent.service.adapt.get",
                                        {'lang': lang,
                                         'utterance': utterance},
                                        {"source": ["mana"],
                                         "destination": ["skills"]}),
                                reply_type="intent.service.adapt.reply",
                                timeout=15)
    return msg.data.get('intent', dict())


def get_padatious_manifest(bus: MessageBusClient, lang: str) -> list:
    """
    Get the manifest of registered Padatious intents
    :param bus: Connected MessageBusClient to query
    :param lang: BCP-47 lang code to get intents for
    """
    msg = bus.wait_for_response(Message("intent.service.padatious.manifest.get",
                                        {"lang": lang},
                                        context={"source": ["mana"],
                                                 "destination": ["skills"]}),
                                reply_type="intent.service.padatious.manifest")
    return msg.data.get('intents', list())


def get_padatious_intent(bus: MessageBusClient, lang: str,
                         utterance: str) -> dict:
    """
    Get a Padatious intent for the input utterance
    :param bus: Connected MessageBusClient to query
    :param lang: language of utterance
    :param utterance: utterance to check
    :returns: dict Padatious intent
    """
    msg = bus.wait_for_response(Message("intent.service.padatious.get",
                                        {'lang': lang,
                                         'utterance': utterance},
                                        {"source": ["mana"],
                                         "destination": ["skills"]}),
                                reply_type="intent.service.padatious.reply",
                                timeout=15)
    return msg.data.get('intent', dict())
