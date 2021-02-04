#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 15:20:59 2020

@author: jmr
"""
import subprocess as sub

### cisco_vpn class
class cisco_vpn:
    def __init__(self, check_for_eduroam = True):
        self.check_eduroam = check_for_eduroam
        if check_for_eduroam:
            self.is_eduroam = "eduroam" in str(sub.check_output("nmcli -t -f active,ssid dev wifi | egrep '^yes' | cut -d\: -f2", shell = True))
        else:
            self.is_eduroam = None
    ## log in 
    def cisco_connect(self, username = None, pswrd = None, account_domain = "my_domain.de", host = "vpn.xkz.my_domain.de"):
        ## check if connected to eduroam, if yes no need to connect to vpn
        if not self.is_eduroam:    
            print(f'> Connecting user {username} to {account_domain}')
            # prepare the command for connecting
            cmd = "printf '{account}\n{pswrd}\ny' | /opt/cisco/anyconnect/bin/vpn -s connect {vpn_host}".format(account = f'{username}@{account_domain}', 
                                                                                                            pswrd = pswrd,
                                                                                                            vpn_host = host)
            ## run the command
            sub.call(cmd, shell = True)
        else:
            if self.check_eduroam:
                print("currently connected to eduroam. Not connecting to the vpn.")
    ## disconnect
    def cisco_disconnect(self):
        print(f'> Disconnecting from cisco anyconnect')
        sub.call("/opt/cisco/anyconnect/bin/vpn disconnect", shell = True)
    ## check the status
    def cisco_status(self):
        out = sub.check_output("/opt/cisco/anyconnect/bin/vpn state", shell = True)
        return list(set([l.replace("\\n\\r", "").strip() for l in str(out).split(">>") if "state:" in l]))[0]
    