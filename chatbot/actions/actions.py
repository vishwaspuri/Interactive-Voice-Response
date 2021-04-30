# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ActionPaymentStatus(Action):

    def name(self) -> Text:
        return "action_payment_status"

    def run(self,   dispatcher, tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict[Text, Any]]:
        if random.uniform(0, 1) > 0.5:
            dispatcher.utter_message("The payment is complete")
        else:
            dispatcher.utter_message("The payment is not complete")

        return []