#! /usr/bin/env python

"""
    Name:   VPN Connect
    Author: Ramece Cave
    Email:  rrcave@n00dle.org

    License: BSD

    Copyright (c) 2017 Ramece Cave
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted     
    provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions
    and the following disclaimer. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the documentation and/or other
    materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
    IMPLIED WARRANTIES,INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
    FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
    DAMAGE.
"""

#__version__ = 2.0

import random,os,pycurl,argparse

username = ""
password = ""
defaultRoute = ""

serverList = ['Algeria', 'Argentina', 'Melbourne', 'Perth', 'Sydney', 'Austria', \
				'Bahrain', 'Belgium', 'Brazil', 'Bulgaria', 'Canada', 'Colombia', \
				'Costa Rica', 'Czech Republic', 'Denmark', 'Egypt', 'El Salvador', \
				'Finland', 'France', 'Germany', 'Greece', 'Hong Kong', 'Iceland', \
				'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', \
				'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', \
				'Malaysia', 'Maldives', 'Marshall Islands', 'Mexico', 'Netherlands', \
				'New Zealand', 'Norway', 'Pakistan', 'Panama', 'Philippines', 'Poland',\
				 'Portugal', 'Qatar', 'Romania', 'Russia', 'Saudi Arabia', 'Singapore', \
				 'Slovakia', 'Slovenia', 'South Korea', 'Spain', 'Sweden', 'Switzerland', \
				 'Taiwan', 'Thailand', 'Turkey', 'Ukraine', \
				 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'Vietnam']

usaServerList = ['Austin', 'Chicago', 'Los Angeles', 'Miami', 'New York', 'San Francisco', 'Seattle', 'Washington']

def GetIp():
	from StringIO import StringIO
	import pycurl

	curl = pycurl.Curl()
	site = 'httpbin.org/ip'
	storage = StringIO()

	curl.setopt(curl.URL, site)	
	curl.setopt(curl.USERAGENT, 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; GTB6.4; SLCC2; .NET CLR 2.0.50727; .NET CLR')
	curl.setopt(curl.WRITEFUNCTION, storage.write)
	curl.perform()
	content = storage.getvalue()

	currentAddy = eval(content).get('origin')

	return currentAddy

def ConnectVPN(anyloc=None,foreign=None,domestic=None):
	if anyloc:
		vpnServer = random.choice(serverList + usaServerList)
	elif foreign:
		vpnServer = random.choice(serverList)
	elif domestic:
		vpnServer = random.choice(usaServerList)

	loginStr = "vyprvpn login %s %s" % (username,password) 
	locationStr = "vyprvpn server set %s" % vpnServer
	connStr = "vyprvpn connect"
	delRouteStr = "sudo route del default gw %s" % defaultRoute
	
	#Exec Commands
	b = os.popen(loginStr).read()
	b = os.popen(locationStr).read()
	b = os.popen(connStr).read()
	b = os.popen(delRouteStr).read()

	print "CONNECTED TO:",vpnServer
	print "CURRENT IP:",GetIp()

	return

def DisconnectVPN():
	dissConnStr = "vyprvpn disconnect"
	logoutStr = "vyprvpn logout"
	dfRouteStr = "sudo route add default gw %s" % defaultRoute

	#Exec Commands

	b = os.popen(dissConnStr).read()
	b = os.popen(logoutStr).read()
	b = os.popen(dfRouteStr).read()

	print "DISCONNECTED!"
	print "CURRENT IP:",GetIp()

	return

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--start",help="Start VPN Tunnel",required=False,action='store_true')
	parser.add_argument("--stop",help="End VPN Tunnel", required=False,action='store_true')
	parser.add_argument("--domestic",help="US based VPN Tunnel", required=False,action='store_true')
	parser.add_argument("--foreign",help="None US based VPN Tunnel", required=False,action='store_true')

	args = parser.parse_args()

	if args.start:
		if args.domestic:
			ConnectVPN(domestic=True)
		elif args.foreign:
			ConnectVPN(foreign=True)
		else:
			ConnectVPN(anyloc=True)

	elif args.stop:
		DisconnectVPN()

if __name__=='__main__':
	main()