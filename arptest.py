#encoding:utf-8

import os
import sys
import subprocess
import time
import codecs
import re

TargetMac = ur'20-cf-30-69-1b-79'
TargetMacList = [ur'20-cf-30-69-1b-79',ur'20:CF:30:69:1B:79']

def nmap_done(filename = 'nmaptest.txt'):
    with codecs.open(filename,'r','GBK') as fin:
        for tline in fin:
            if 'Nmap done:' in tline:
                return True
    return False

def count_lines_in_file(filename = 'nmaptest.txt'):
    ret = 0
    with codecs.open(filename,'r','GBK') as fin:
        for ret,tline in enumerate(fin):
            pass
    return ret + 1
    
def search_in_nmap_result(textname = 'nmaptest.txt'):
    IPpattern = re.compile(r'([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})')
    Macpattern = re.compile(r'([0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2})')
    # result
    IPMacTurple = []
    with codecs.open(textname,'r','GBK') as fin:
        curIP = ''
        curMac = ''
        for tline in fin:
            if tline.startswith('Nmap scan report for'):
                res = IPpattern.search(tline)
                curIP = res.group(0)
            if tline.startswith('MAC Address:'):
                res = Macpattern.search(tline)
                curMac = res.group(0)
                if curMac in TargetMacList:
                    print 'server IP-Mac:'
                    print 'IP ({}) -- Mac ({})'.format(curIP,curMac)
                    # add to result
                    IPMacTurple.append((curIP,curMac))
                
    return IPMacTurple
    
def wait_until_nmap_finishes():
    count = 1
    while nmap_done() == False:
        print 'waiting for nmap to finish... count({})'.format(count)
        count+=1
        time.sleep(15)
def nmaptest():
    # Use Nmap to find server IPs
    #
    # nmap ping scan:
    print 'Starting nmap ping scan...'
    with codecs.open('nmaptest.txt','w','utf-8') as fout:
        nmap_ret = subprocess.Popen('nmap -sP 166.111.65.1/22',stdout = fout)
    # wait
    wait_until_nmap_finishes()
    # proc to find servers
    search_in_nmap_result()

def arptest():
    # nmap ping scan:
    print 'Starting nmap ping scan...'
    with codecs.open('nmaptest.txt','w','utf-8') as fout:
        nmap_ret = subprocess.Popen('nmap -sP 166.111.65.1/22',stdout = fout)
    # wait
    wait_until_nmap_finishes()

    ret = subprocess.Popen('arp -a',stdout = subprocess.PIPE)
    print '-'*30
    text = ret.communicate()
    arpres = text[0].decode('GBK')
    # output to text
    with codecs.open('arptest.txt','w','utf-8') as fout:
        fout.write(arpres)
    ipmaclist = arpres.split(os.linesep)
    print 'Total number in list:{}'.format(len(ipmaclist))
    print 'Target sv0 IP:'
    print '-'*50
    for ipmac in ipmaclist:
        if TargetMac in ipmac:
            print ipmac

    # input to continue
    a = raw_input("input sth to terminate:")



if __name__ == "__main__":
    nmaptest()

