import os
import nmap
import sys
import re
import subprocess

network = "192.168.0.0/24"
logfile = "log/pihole.log"

"""
https://serverfault.com/a/665337

nmap -sn 192.168.0.0/24
-sn  No port scan
-n   No DNS resolution  
-T5  Faster execution

Example: nmap -sn -T5 -n --min-parallelism 100 192.168.0.0/24
"""


def ping_sweep():
    hosts = {}
    nm = nmap.PortScanner()
    nm.scan(hosts=network, arguments='-sn -T5')

    zaehler = 1
    for x in nm.all_hosts():
        hosts[zaehler] = x + "   " + nm[x].hostname()
        zaehler += 1

    for key, value in hosts.items():
        print(key, ' : ', value)

    try:
        host_number = int(input("\nNumber of host: "))
    except ValueError:
        sys.exit("Ungueltige Eingabe")

    # https://www.geeksforgeeks.org/extract-ip-address-from-file-using-python/
    return re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})').match(hosts[host_number]).group(1)


def tail(ip):
    ip = "192.168.0.4"
    cmd = "cat {} | grep -B1 {}".format(logfile, ip)
    subprocess.call(cmd, shell=True)


def check_access():
    if os.access(logfile, os.R_OK) is False:
        sys.exit("Kann Logfile nicht öffnen!")


if __name__ == "__main__":
    check_access()
    tail(ping_sweep())
