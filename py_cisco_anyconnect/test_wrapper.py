#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 18:40:17 2020

@author: jmr
"""
from wrapper import *

password = input('Password: ')
print(password)
vpn = cisco_vpn(username = "frvx037", pswrd = password, account_domain = "uni-hamburg.de", host = "vpn.rrz.uni-hamburg.de")
vpn.cisco_connect()
print(vpn.cisco_status())
vpn.cisco_disconnect()
print(vpn.cisco_status())