import os
import nmap
import sys
import re
import subprocess
from subprocess import PIPE, Popen
from collections import deque

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
    """from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html 
    """  
    match = [ ip, 'query[A]' ]     
    f = subprocess.Popen(['tail','-f',logfile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)      
    while True:                                                
        line1 = f.stdout.readline().decode("utf-8") 
        if all(c in line1 for c in match):   
            line2 = f.stdout.readline().decode("utf-8")  
            if 'blocked' in line2:        
                start = 'query[A]'      
                end = 'from'         
                print(bcolors.FAIL + line1[0:15] + ':' + line1[line1.find(start)+len(start):line1.rfind(end)] + bcolors.ENDC)


def check_access():
    if os.access(logfile, os.R_OK) is False:
        sys.exit("Kann Logfile nicht öffnen!")


if __name__ == "__main__":
    check_access()
    ip = ping_sweep()
    tail(ip)
