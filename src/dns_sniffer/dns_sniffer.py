import pyshark
import psutil
import socket
import subprocess

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

def print_dns_info(pkt):
    try:
        if pkt.dns.qry_name and "xn--" in pkt.dns.qry_name:
            print ('DNS Request from {}: {}'.format(pkt.ip.src, pkt.dns.qry_name))
    except AttributeError as e:
        pass
    try:
        if pkt.dns.resp_name:
            print ('DNS Response from {}: {}'.format(pkt.ip.src, pkt.dns.resp_name))
    except AttributeError as e:
        pass

def initiate_sniffing(interface_name):
    cap = pyshark.LiveCapture(interface=interface_name)
    cap.sniff_continuously()
    cap.apply_on_packets(print_dns_info)