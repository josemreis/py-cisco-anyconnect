#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 15:20:59 2020

@author: jmr
"""
import subprocess as sub

### cisco_vpn class
class cisco_vpn():
    def __init__(self, username = None, pswrd = None, account_domain = "uni-hamburg.de", host = "vpn.rrz.uni-hamburg.de", lastlog_path = None):
        self.account_domain = account_domain
        self.host = host
        self.lastlog_path = lastlog_path
        self.username = username
        if isinstance(pswrd, str):
            self.pswrd = pswrd
        else:
            raise ValueError("No password was provided.")
        self.is_eduroam = "eduroam" in str(sub.check_output("nmcli -t -f active,ssid dev wifi | egrep '^yes' | cut -d\: -f2", shell = True))
    ## log in 
    def cisco_connect(self):
        ## check if connected to eduroam, if yes no need to connect to vpn
        if not self.is_eduroam:    
            print(f'> Connecting user {self.username} to {self.account_domain}')
            # prepare the command for connecting
            cmd = "printf '{account}\n{pswrd}\ny' | /opt/cisco/anyconnect/bin/vpn -s connect {vpn_host}".format(account = f'{self.username}@{self.account_domain}', 
                                                                                                            pswrd = self.pswrd,
                                                                                                            vpn_host = self.host)
            ## run the command
            sub.call(cmd, shell = True)
        else:
            print("currently connected to eduroam. Not connecting to the vpn.")
    ## disconnect
    def cisco_disconnect(self):
        print(f'> Disconnecting user {self.username} from {self.account_domain}')
        sub.call("/opt/cisco/anyconnect/bin/vpn disconnect", shell = True)
    ## check the status
    def cisco_status(self):
        out = sub.check_output("/opt/cisco/anyconnect/bin/vpn state", shell = True)
        return list(set([l.replace("\\n\\r", "").strip() for l in str(out).split(">>") if "state:" in l]))[0]
    