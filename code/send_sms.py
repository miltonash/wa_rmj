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
    sid = open('Account_SID.txt', 'r')
    Account_SID = sid.read()
    token = open('Auth_Token.txt', 'r')
    Auth_Token = token.read()
    client = Client(Account_SID,
                    Auth_Token)

    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    # account to send SMS to any phone number
    client.messages.create(to="+18478945670",
                           from_="+18593408786",
                           body="Your Python script is done running!")
