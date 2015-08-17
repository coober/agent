#!/usr/bin/python
#-*- coding:utf-8 -*-

__author__ = 'Coober Liang'

import json
import time
import socket
import commands
import urllib2
import base64

####xxx.com#######
DOMAIN = 'domain name'
PORTS = [8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8091,8092]
PATH = 'l/api/log/operate/write'



def main(DOMAIN, PORTS, PATH):
    timestamp = int(time.time())
    step = 60
    IP = socket.gethostname()
    IPADDR = socket.gethostbyaddr(IP)[2][0]
    metric = "tomcat"
    endpoint = IP
    p = []

    monit_keys = [
        (IP,'GAUGE')
    ]

    SET_HEADER = {
    'Host':DOMAIN,
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'
    }

    for i in PORTS:
        for key,vtype in monit_keys:
            if key == IP:
                try:
                    URL = 'http://%s:%d/%s' % (IPADDR, i, PATH)
                    req = urllib2.Request(URL, headers=SET_HEADER)
                    r = urllib2.urlopen(req)
                    value =  r.code
                except Exception,e:
                    value = 500
        #print value, URL
                i = {
                    'Metric': '%s.%s' % (metric,key),
                    'Endpoint': endpoint,
                    'Timestamp': timestamp,
                    'Step': step,
                    'Value': value,
                    'CounterType': vtype,
                    'TAGS': 'port=%s' % i
                }
                p.append(i)

    print json.dumps(p, sort_keys=True, indent=4)
    method = "POST"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    url = 'http://127.0.0.1:1988/v1/push'
    request = urllib2.Request(url, data=json.dumps(p) )
    request.add_header("Content-Type",'application/json')
    request.get_method = lambda: method
    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e
    if connection.code == 200:
        print connection.read()
    else:
        print '{"err":1,"msg":"%s"}' % connection


if __name__ == '__main__':
	proc = commands.getoutput(''' ps -ef|grep 'check-tomcat-status.py'|grep -v grep|wc -l ''')
	if int(proc) < 5:
		main(DOMAIN, PORTS, PATH)

