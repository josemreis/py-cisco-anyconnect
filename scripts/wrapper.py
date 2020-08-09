#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 15:20:59 2020

@author: jmr
"""
import subprocess as sub
from random import choice
import os

### cisco_vpn class
class cisco_vpn():
    def __init__(self, username = None, pswrd_path = None, account_domain = "@uni-hamburg.de", host = "vpn.rrz.uni-hamburg.de", lastlog_path = None):
        self.account_domain = account_domain
        self.host = host
        self.lastlog_path = lastlog_path
        self.username_all = username
        self.pswrd = open(pswrd_path).read().rstrip("\n")
        self.is_eduroam = "eduroam" in str(sub.check_output("nmcli -t -f active,ssid dev wifi | egrep '^yes' | cut -d\: -f2", shell = True))
    ## log in 
    def cisco_connect(self, sequential_log = True):
        ## check if connected to eduroam, if yes no need to connect to vpn
        if not self.is_eduroam:
            ## if accounts > 1, retrieve last log and chose random account
            ## which is not the previous used one
            # get the next log account     
            if len(self.username_all) > 1 and sequential_log:
                if not os.path.isfile(self.lastlog_path):
                    raise ValueError("path to lastlog text file missing!")
                lastlog = open(self.lastlog_path).read().rstrip("\n")
                next_log = choice([x for x in self.username_all if x != lastlog])
                ## replace the last log in file
                with open(self.lastlog_path) as f:
                    lines = f.readlines()
                lines[0] = next_log
                with open(self.lastlog_path, "w") as f:
                    f.writelines(lines)
            else:
                next_log = self.username_all[0]
            # prepare the command for connecting
            cmd = "printf '{account}\n{pswrd}\ny' | /opt/cisco/anyconnect/bin/vpn -s connect {vpn_host}".format(account = next_log + self.account_domain, 
                                                                                                            pswrd = self.pswrd,
                                                                                                            vpn_host = self.host)
            ## run the command
            sub.call(cmd, shell = True)
        else:
            print("currently connected to eduroam. Not connecting to the vpn.")
    ## disconnect
    def cisco_disconnect():
        sub.call("/opt/cisco/anyconnect/bin/vpn disconnect", shell = True)
    ## check the status
    def cisco_status():
        out = sub.check_output("/opt/cisco/anyconnect/bin/vpn state", shell = True)
        return list(set([l.replace("\\n\\r", "").strip() for l in str(out).split(">>") if "state:" in l]))[0]