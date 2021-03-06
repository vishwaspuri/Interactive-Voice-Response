# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import random
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from mongoengine import connect
from .appointment_queries import CreateNewAppointment, GetAppointment, CancelAppointment
from .employee_queries import GetEmployeeByName
from dotenv import load_dotenv
from dotenv import dotenv_values
import os

load_dotenv()
connect(host=os.getenv('MONGO_ADDR'))

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

class ValidateAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_appointment_form"
    
    def validate_user_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        return {"user_name": slot_value}
    def validate_appointment_with(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        if GetEmployeeByName(slot_value) is None:
            dispatcher.utter_message(text="There is no one who goes by the name  "+slot_value+" here.")
            return {"appointment_with": None}
        else:
            return {"appointment_with": slot_value}
    def validate_time(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        return {"time": slot_value}
        


class ActionCreateMeeting(Action):
    def name(self)  -> Text:
        return "action_create_appointment"
    
    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        # user_name is the name of the person making the appointment
        user_name = tracker.get_slot("user_name")
        # appointment_with is the name of the person with whom the appointment is being made
        appointment_with = tracker.get_slot("appointment_with")
        # appointment_time is the time of the appointment
        appointment_time = tracker.get_slot("time")
        employee = GetEmployeeByName(name=appointment_with)
        if employee is None:
            dispatcher.utter_message(text="We have no employee with the provided name.")
            return []

        try:
            appointment = CreateNewAppointment(employee=employee, customer_name=user_name, appointment_time=appointment_time)
            dispatcher.utter_message(template="utter_appointment_confirmed", User_name=user_name, Appointment_with=appointment_with, Appointment_time=appointment_time)
            return [SlotSet("appointment_with", None), SlotSet("time", None)]
        except:
            dispatcher.utter_message(text="We could not create an appointment due to an unkown problem. Please try again later.")

class ValidateCancelAppointment(FormValidationAction):
    def name(self) -> Text:
        return "validate_cancel_appointment_form"
    
    def validate_user_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        return {"user_name": slot_value}
    def validate_appointed_with(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        if GetEmployeeByName(slot_value) is None:
            dispatcher.utter_message(text="There is no one who goes by the name  "+slot_value+" here.")
            return {"appointed_with": None}
        else:
            return {"appointed_with": slot_value}
    def validate_time(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        emp = GetEmployeeByName(name = tracker.get_slot('appointment_with'))
        if GetAppointment(employee=emp, customer_name=tracker.get_slot('user_name'), appointment_time= tracker.get_slot('time')) is not None:
            dispatcher.utter_message(text="You already have an appointment with us at the said time. Please provide a different time and company employee.")
            return {
                'time': None,
                'appointed_with': None,
            }
        else:    
            return {"time": slot_value}

#--------------------------------------------------------------------------------------------
#   Action for cancelling slot
#--------------------------------------------------------------------------------------------
class CancelAppointmentAction(Action):
    def name(self)  -> Text:
        return "action_cancel_appointment"
    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        # user_name is the name of the person making the appointment
        user_name = tracker.get_slot("user_name")
        # appointment_with is the name of the person with whom the appointment is being made
        appointment_with = tracker.get_slot("appointed_with")
        # appointment_time is the time of the appointment
        appointment_time = tracker.get_slot("time")
        employee = GetEmployeeByName(name=appointment_with)
        if employee is None:
            dispatcher.utter_message(text="We have no employee with the provided name.")
            return [SlotSet("appointed_with", None), SlotSet("time", None)]
        appointment = GetAppointment(employee = employee, customer_name=user_name, appointment_time=appointment_time)
        if appointment is None:
            dispatcher.utter_message(text="You have no appointment with "+employee.name+" at "+appointment_time.strftime()+".")
            return [SlotSet("appointed_with", None), SlotSet("time", None)]
        try:
            res = CancelAppointment(employee=employee, customer_name=user_name, appointment_time=appointment_time)
            if res is True:
                dispatcher.utter_message(text="Your appoinment has been cancelled")
                return [SlotSet("appointed_with", None), SlotSet("time", None)]
            else:
                dispatcher.utter_message(text="Your appoinment could not be deleted due to an unknown error")
                return []
        except:
            dispatcher.utter_message(text="Your appoinment could not be deleted due to an unknown error")
            return []

