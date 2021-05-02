# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import random
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymodm import connect
from .db.queries.appointment import CreateNewAppointment
from .db.queries.employee import GetEmployeeByName

connect('mongodb://127.0.0.1:27017/rasa-chatbot')

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        dispatcher.utter_message(text="Hello World!")

        return []

class ValidatePaymentVerificationForm(Action):
    def name(self) -> Text:
        return "payment_id_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        required_slots = ["payment_id"]

        # Added for loop for the case of having multiple slots
        for slot_name in required_slots:
            if tracker.get_slot(slot_name) is None:
                return [SlotSet("requested_slot", slot_name)]
            
        return [SlotSet("requested_slot"), None]

class ActionPaymentStatus(Action):
    def name(self) -> Text:
        return  "action_payment_status"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        if random.uniform(0, 1) > 0.5:
            dispatcher.utter_message(template="utter_payment_status", Payment_status="done", Payment_id=tracker.get_slot("payment_id"))
            return []
        else:
            dispatcher.utter_message(template="utter_payment_status", Payment_status="not done", Payment_id=tracker.get_slot("payment_id"))
            return []

class ValidateAppointmentForm(Action):
    def name(self) -> Text:
        return "appointment_form"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        required_slots = ["user_name", "appointment_with", "time"]
        for slot_name in required_slots:    
            if tracker.get_slot(slot_name) is None:
                return [SlotSet("requested_slot", slot_name)]
        
        return [SlotSet("requested_slot"), None]

class ActionCreateMeeting(Action):
    def name(self)  -> Text:
        return "action_create_appointment"
    
    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        # user_name is the name of the person making the appointment
        user_name = tracker.get_slot("user_name")
        print(user_name)
        # appointment_with is the name of the person with whom the appointment is being made
        appointment_with = tracker.get_slot("appointment_with")
        print(appointment_with)
        # appointment_time is the time of the appointment
        appointment_time = tracker.get_slot("time")
        print(appointment_time)

        employee = GetEmployeeByName(name=appointment_with)
        if employee is None:
            dispatcher.utter_message(text="We have no employee with the provided name.")
            return []

        try:
            appointment = CreateNewAppointment(employee=employee, customer_name=user_name, appointment_time=appointment_time)
            dispatcher.utter_message(template="utter_appointment_confirmed", User_name=user_name, Appointment_with=appointment_with, Appointment_time=appointment_time)
        except:
            dispatcher.utter_message(text="We could not create an appointment due to an unkown problem. Please try again later.")

        
        

