from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from rasa_sdk.forms import FormAction
from rasa_sdk import Action
from rasa_sdk.events import UserUtteranceReverted

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
import os
from rasa_sdk.events import SlotSet, Restarted
from typing import Any, Dict, List, Text, Union, Optional
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)

address = "http://localhost:9080"


class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        intent = tracker.latest_message["intent"].get("name")
        shown_privacy = tracker.get_slot("shown_privacy")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        if intent == "greet" or (intent == "enter_data" and name_entity):
            if shown_privacy and name_entity and name_entity.lower() != "saarthi":
                dispatcher.utter_template("utter_greet_name", tracker, name=name_entity)
                return []
            else:
                dispatcher.utter_template("utter_greet", tracker)
                dispatcher.utter_template("utter_inform_privacypolicy", tracker)
                dispatcher.utter_template("utter_ask_goal", tracker)
                return [SlotSet("shown_privacy", True)]
        elif intent[:-1] == "get_started_step" and not shown_privacy:
            dispatcher.utter_template("utter_greet", tracker)
            dispatcher.utter_template("utter_inform_privacypolicy", tracker)
            dispatcher.utter_template("utter_" + intent, tracker)
            return [SlotSet("shown_privacy", True), SlotSet("step", intent[-1])]
        elif intent[:-1] == "get_started_step" and shown_privacy:
            dispatcher.utter_template("utter_" + intent, tracker)
            return [SlotSet("step", intent[-1])]
        return []


class intent_recog(Action):

    def name(self):
        return 'action_intent'

    def run(
            self,
            dispatcher,
            tracker,
            domain):
        intent = tracker.latest_message['intent'].get('name')
        print(intent)

        if (intent == 'affirm'):
            response = "yes"
        elif (intent == 'deny'):
            response = "no"
        elif (intent == 'diff_domains'):
            response = "diff_domains"
        elif (intent == 'explain'):
            response = "Please, connect to our customer support 8861512182 for the details"
        elif (intent == 'onboarding_info'):
            response = "onboarding_info_details...."
        elif (intent == 'registration_info'):
            response = "registration_info details"

        dispatcher.utter_message(response)

        return []


class ActionRestart(Action):
    """Restarts conversation"""

    def name(self):
        return "action_restart"

    def __init__(self):
        pass

    def run(
            self,
            dispatcher,
            tracker,
            domain,
    ):
        dispatcher.utter_message("Loading...\nAnd I've been restarted!")
        return [Restarted()]