#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 18:40:17 2020

@author: jmr
"""
from wrapper import *

password = open("/home/jmr/Desktop/cac.txt").read().rstrip()
vpn = cisco_vpn(
        username = ["frvx037", "bar5163"], 
        pswrd = password, 
        account_domain = "@uni-hamburg.de", 
        host = "vpn.rrz.uni-hamburg.de", 
        lastlog_path = '/home/jmr/Desktop/lastlogin_hamb_vpn.txt'
        )

vpn.cisco_connect(multilog_type = "sequential")

vpn.cisco_disconnect()