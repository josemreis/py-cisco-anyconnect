#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 18:40:17 2020

@author: jmr
"""
from wrapper import *

password = input('Password: ')
print(password)
username = input('username: ')
print(username)
vpn = cisco_vpn()
vpn.cisco_connect(username = username, pswrd = password, account_domain = "uni-hamburg.de", host = "vpn.rrz.uni-hamburg.de")
print(vpn.cisco_status())
vpn.cisco_disconnect()
print(vpn.cisco_status())