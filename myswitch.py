#!/usr/bin/env python3

'''
Ethernet learning switch in Python: HW3.

Note that this file currently has the code to implement a "hub"
in it, not a learning switch.  (I.e., it's currently a switch
that doesn't learn.)
'''
from switchyard.lib.address import *
from switchyard.lib.packet import *
from switchyard.lib.common import *

def switchy_main(net):
    my_interfaces = net.interfaces()
    my_addresses = [interface.ethaddr for interface in my_interfaces]
    my_forwarding_table = {}

    while True:
        try:
            port_in, packet = net.recv_packet()
        except NoPackets:
            continue
        except Shutdown:
            return

        log_debug ("In {} received packet {} on {}".format(net.name, packet, port_in))

        source_address = packet[0].src
        destination_address = packet[0].dst

        my_forwarding_table[source_address] = port_in

        if destination_address in my_addresses:
            log_debug ("Packet intended for me")
            #drop for now
        else:
            if packet[0].dst in my_forwarding_table:
                net.send_packet(my_forwarding_table[destination_address], packet)
            else:
                for interface in my_interfaces:
                    if port_in != interface.name:
                        log_debug ("Flooding packet {} to {}".format(packet, interface.name))
                        net.send_packet(interface.name, packet)

    net.shutdown()
