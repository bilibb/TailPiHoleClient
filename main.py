import os
import nmap
import sys
import re
import subprocess
import argparse

network = "192.168.0.0/24"
logfile = "log/pihole.log"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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

    # TODO: Loop
    for key, value in hosts.items():
        print(key, ' : ', value)

    try:
        host_number = int(input("\nNumber of host: "))
    except ValueError:
        sys.exit("Ungueltige Eingabe")

    # https://www.geeksforgeeks.org/extract-ip-address-from-file-using-python/
    return re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})').match(hosts[host_number]).group(1)


def tail_blocked(ip):
    match = [ip, 'query[A]']
    blocked = ['blacklisted', 'blocked']
    f = subprocess.Popen(['tail', '-f', logfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line1 = f.stdout.readline().decode("utf-8")
        if all(c in line1 for c in match):
            line2 = f.stdout.readline().decode("utf-8")
            if any(c in line2 for c in blocked):
                start = 'query[A]'
                end = 'from'
                print(bcolors.FAIL + line1[0:15] + ':' + line1[line1.find(start) + len(start):line1.rfind(
                    end)] + bcolors.ENDC)


def tail_unblocked(ip):
    match = [ip, 'query[A]']
    allowed = ['forwarded', 'cached']
    f = subprocess.Popen(['tail', '-f', logfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line1 = f.stdout.readline().decode("utf-8")
        if all(c in line1 for c in match):
            line2 = f.stdout.readline().decode("utf-8")
            if any(c in line2 for c in allowed):
                start = 'query[A]'
                end = 'from'
                print(bcolors.OKGREEN + line1[0:15] + ':' + line1[line1.find(start) + len(start):line1.rfind(
                    end)] + bcolors.ENDC)


def tail_both(ip):
    match = [ip, 'query[A]']
    allowed = ['forwarded', 'cached']
    blocked = ['blacklisted', 'blocked']
    f = subprocess.Popen(['tail', '-f', logfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line1 = f.stdout.readline().decode("utf-8")
        if all(c in line1 for c in match):
            line2 = f.stdout.readline().decode("utf-8")
            if any(c in line2 for c in blocked):
                start = 'query[A]'
                end = 'from'
                print(bcolors.FAIL + line1[0:15] + ':' + line1[line1.find(start) + len(start):line1.rfind(
                    end)] + bcolors.ENDC)
            if any(c in line2 for c in allowed):
                start = 'query[A]'
                end = 'from'
                print(bcolors.OKGREEN + line1[0:15] + ':' + line1[line1.find(start) + len(start):line1.rfind(
                    end)] + bcolors.ENDC)


def check_access():
    if os.access(logfile, os.R_OK) is False:
        sys.exit("Kann Logfile nicht öffnen!")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='TailPiHoleClient', description='Display requested domains from one '
                                                                             'Pi-Hole user')

    argparser.add_argument("-u", action='store_true', required=False, help="Only allowed domains")
    argparser.add_argument("-b", action='store_true', required=False, help="Only blocked domains")

    args = argparser.parse_args()

    check_access()

    if args.b:
        tail_blocked(ping_sweep())
    elif args.u:
        tail_unblocked(ping_sweep())
    else:
        tail_both(ping_sweep())
