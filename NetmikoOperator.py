# -*- coding: utf-8 -*-

from netmiko import ConnectHandler
import clitable

class NetmikoOperator():
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.net_connect = {}


    def open_session(self,ip,username,password,device,hostname):
        # open session to target device
        if hostname in self.net_connect:
            pass
        else:
            # make SSH session to router
            handler = {
                'device_type': device,
                'ip': ip,
                'username': username,
                'password': password,
                }
            self.net_connect[hostname] = ConnectHandler(**handler)
            print("[INFO] Successfully make SSH connection to {}".format(hostname))


    def close_session(self,hostname):
        # close existing session
        self.net_connect[hostname].disconnect()
        del self.net_connect[hostname]
        print("[INFO] Successfully close SSH connection to {}".format(hostname))


    def send_command(self,command,hostname):
        # send command to target device
        out = self.net_connect[hostname].send_command(command)
        print("[INFO] Successfully get output of command<{}> from {}".format(command,hostname))
        print("="*30)
        print(out)
        print("="*30)
        return out


    def check_if_state(self,ifname,hostname):
        # check target interface's state
        # return
        #  True  : if the interface is up
        #  False : if the interface is not up
        command = 'show interface %s' % format(ifname)
        ifstate_ouput = self.send_command(command,hostname)
        cli_table = clitable.CliTable('index', './template')
        attributes = {'Command': 'show interfaces', 'Vendor':'cisco_xr'}
        cli_table.ParseCmd(ifstate_ouput, attributes)
        ifstate_dict =  self.clitable_to_dict(cli_table)
        if ifstate_dict[0]["link_status"] == "up":
            return True
        else:
            return False


    def clitable_to_dict(self,cli_table):
        objs = []
        for row in cli_table:
            temp_dict = {}
            for index, element in enumerate(row):
                temp_dict[cli_table.header[index].lower()] = element
            objs.append(temp_dict)
        return objs


    def commit_configlist(self,config,comment,hostname):
        # commit config to IOS-XR device
        output1 = self.net_connect[hostname].send_config_set(config)
        output2 = self.net_connect[hostname].send_command("show configuration")
        output3 = self.net_connect[hostname].commit(comment=comment)
        output4 = self.net_connect[hostname].exit_config_mode()
        print("[INFO] Successfully change config on {}".format(hostname))
        print("="*30)
        print(output1)
        print(output2)
        print(output3)
        print(output4)
        print("="*30)


    def shutdown_interface(self,ifname,comment,hostname):
        # shutdown interface
        configs = []
        configs.append("interface {}".format(ifname))
        configs.append(' shutdown')
        self.commit_configlist(configs,comment,hostname)
        print("[INFO] Successfully shutdown interface<{}> of {}".format(ifname,hostname))


    def noshutdown_interface(self,ifname,comment,hostname):
        # no shutdown interface
        configs = []
        configs.append("interface {}".format(ifname))
        configs.append(' no shutdown')
        self.commit_configlist(configs,comment,hostname)
        print("[INFO] Successfully unshutdown interface<{}> of {}".format(ifname,hostname))
