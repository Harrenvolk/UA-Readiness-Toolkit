import pyshark
import psutil
import socket
import subprocess
import time

dns_Ids_to_look_for=set()

def run_powershell(cmd):
    captured_result = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return captured_result

def run_terminal(cmd_options_list):
    captured_result = subprocess.run([cmd_options_list], capture_output=True, text=True).stdout
    return captured_result

def detect_interfaces():
    return list(psutil.net_if_addrs().keys())

def check_interface(interface):
    nic_address = psutil.net_if_addrs().get(interface) or []
    return socket.AF_INET in [snicaddr.family for snicaddr in nic_address]

def list_active_interfaces():
    active_intefaces = []
    for interface in detect_interfaces():
        if check_interface(interface):
            active_intefaces.append(interface)
    return active_intefaces

def print_dns_info(pkt, f):

    try:
        if pkt.dns.qry_name and "xn--" in pkt.dns.qry_name:
            dns_Ids_to_look_for.add(pkt.dns.id)
            print ('DNS Request from {}: {}: {}'.format(pkt.ip.src, pkt.dns.qry_name, pkt.dns.id), file=f)
    except AttributeError as e:
        pass
    try:
        if pkt.dns.resp_name and pkt.dns.id in dns_Ids_to_look_for:
            print ('DNS Response from {}: {}: {}'.format(pkt.ip.src, pkt.dns.resp_name, pkt.dns.id), file=f)
    except AttributeError as e:
        pass

def initiate_sniffing(interface_name):
    with open("pkt.txt", "w") as f:
        start=time.time()
        cap = pyshark.LiveCapture(interface=interface_name)

        for pkt in cap.sniff_continuously():
            if 30<time.time()-start: break
            print_dns_info(pkt, f)