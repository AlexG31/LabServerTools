#encoding:utf-8

import os
import sys
import codecs
import re

#curuserhomepath = os.path.abspath('~')
def Update_serverIP(IP_in):
    IPpattern = re.compile(r'([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})')
    # validate IP_in:
    if not IPpattern.search(IP_in):
        raise StandardError('IP_in is not a valid IP address!:{}'.format(IP_in))
    configfilepath = os.path.join('~','.ssh','config')
    configfilepath = os.path.expanduser(configfilepath)
    print 'config path:',configfilepath

    configure_text = ''
    with codecs.open(configfilepath,'r','utf-8') as fin:
        for line in fin:
            # search for IP & replace it
            res = IPpattern.search(line)
            cpline = line
            if res:# found IP
                oldIP = res.group(0)
                cpline = cpline.replace(oldIP,IP_in)
            configure_text += cpline
    with codecs.open(configfilepath,'w','utf-8') as fout:
        fout.write(configure_text)



if __name__ == '__main__':
    IP_in = raw_input('Please input new IP address:')
    Update_serverIP(IP_in)
