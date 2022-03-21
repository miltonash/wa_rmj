# ==============================================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name: send_sms.py
# Author: Milton Straw

''' Description.

This script defines a function called 'message()'. message() can be imported into scripts. When a script has finished running in the terminal, sms() will text my phone with a message to tell me that it is done.
'''
# ==============================================================================


def send_sms():
    # we import the Twilio client from the dependency we just installed
    from twilio.rest import Client

    # the following line needs your Twilio Account SID and Auth Token
    client = Client("AC10b7aceaf81589e8cf70ae2697c2ae61",
                    "ca7ead1b352145c39911e3d2ef53cc2f")

    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    # account to send SMS to any phone number
    client.messages.create(to="+18478945670",
                           from_="+18593408786",
                           body="Your Python script is done running!")
