#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import base64 as b64
import commands as cm
import string

def main():
    if(len(sys.argv) > 1):
        if(sys.argv[1] == 'isReady'):
            print "OK!"
        elif(sys.argv[1] == 'sysInfo'):
            sysInfo()
        elif(sys.argv[1] == 'cmLaunch'):
            if len(sys.argv) == 3:
                cmLaunch(b64.b64decode(sys.argv[2]))
            else:
                cmLaunch('')
        elif(sys.argv[1] == 'servStatus'):
            if len(sys.argv) == 3:
                servStatus(b64.b64decode(sys.argv[2]))
            else:
                servStatus('')
        elif(sys.argv[1] == 'firewall'):
            if len(sys.argv) == 3:
                firewall(b64.b64decode(sys.argv[2]))
            else:
                firewall('')
        elif(sys.argv[1] == 'logInsp'):
            if len(sys.argv) == 3:
                log(b64.b64decode(sys.argv[2]))
            else:
                log('')
        else:
            print sys.argv[1]
    else:
        print "FAIL!"
    
    return 0

def sysInfo():
    dic = {}

    dic['$date'] = cm.getoutput('date "+%F %X"')

    uname = cm.getoutput("uname -a")
    dic['$uname'] = uname;

    uptime = cm.getoutput("uptime")
    uptime = uptime.replace(', ', ' ')
    uptime = uptime.split(" ");
    dic['$up'] = uptime[2]+' '+uptime[4];
    dic['$user'] = uptime[6]+' '+uptime[7]
    dic['$load'] = uptime[9]+' '+uptime[10]+' '+uptime[11]+' '+uptime[12]+' '+uptime[13]

    memo = oneSpace(cm.getoutput('free -h -t')).split("\n")
    memofis = memo[1].split(' ');
    memoswa = memo[3].split(' ');
    memotot = memo[4].split(' ');

    dic['$memof1'] = memofis[1]
    dic['$memof2'] = memofis[2]
    dic['$memof3'] = memofis[3]
    dic['$memos1'] = memoswa[1]
    dic['$memos2'] = memoswa[2]
    dic['$memos3'] = memoswa[3]
    dic['$memot1'] = memotot[1]
    dic['$memot2'] = memotot[2]
    dic['$memot3'] = memotot[3]

    disc = oneSpace(cm.getoutput('df -h')).split("\n")
    ddisc = ''
    for d in disc:
        if d[0:4] == '/dev':
            tmp = d.split(' ')
            ddisc += '<tr><th>'+tmp[5]+'</th><td>'+tmp[1]+'</td><td>'+tmp[2]+'</td><td>'+tmp[3]+'</td><td>'+tmp[4]+'</td></tr>'
    dic['$disc'] = ddisc

    net = oneSpace(cm.getoutput('ifconfig')).split("\n\n");
    dnet = ''
    for n in net:
        lines = n.split("\n")
        pars = lines[1].split(' ')
        add = ''
        msk = ''
        for p in pars:
            if p[0:4] == 'addr':
                add = p.split(':')[1]
            elif p[0:4] == 'Mask':
                msk = p.split(':')[1]
        dnet += '<tr><th>'+lines[0].split(' ')[0]+'</th><td>'+add+'</td><td>'+msk+'</td></tr>'				
    dic['$net'] = dnet

    gate = oneSpace(cm.getoutput('route')).split("\n")
    dgate = ''
    for g in gate:
        if g[0:7] == 'default':
            dgate = g.split(' ')[1]
    dic['$gateway'] = dgate

    render('/usr/local/nomad/html/sysInfo.html', dic)

def cmLaunch(cmd):
    
    dic = {}
    
    if cmd != '':
        dic['$rcmd'] = cm.getoutput(cmd).replace("\n", "<br />")
    else:
        dic['$rcmd'] = ''
    
    render('/usr/local/nomad/html/cmLaunch.html', dic);

def servStatus(cmd):
    dic = {}
    
    if cmd != '':
        cm.getoutput(cmd)
    
    code = ''
    
    ssh = cm.getoutput('service ssh status')
    apa = cm.getoutput('service apache2 status')
    mys = cm.getoutput('ps -A | grep mysqld')
    ftp = cm.getoutput('service vsftpd status')
    dhc = cm.getoutput('service isc-dhcp-server status')
    dns = cm.getoutput('service bind9 status')
    squ = cm.getoutput('service squid status')
    smb = cm.getoutput('service samba status')
    pos = cm.getoutput('service postfix status')
    
    if 'is running' in ssh:
        code += '<tr><th>SSH</th><td style="color: green;">RUNNING</td></tr>'
    else:
        code += '<tr><th>SSH</th><td style="color: red;">STOP</td></tr>'
        
    if 'is running' in apa:
        code += '<tr><th>APACHE</th><td style="color: green;">RUNNING</td></tr>'
    else:
        code += '<tr><th>APACHE</th><td style="color: red;">STOP</td></tr>'
        
    if mys != '':
        code += '<tr><th>MYSQL</th><td style="color: green;">RUNNING</td></tr>'
    else:
        code += '<tr><th>MYSQL</th><td style="color: red;">STOP</td></tr>'
        
    if 'is running' in ftp:
        code += '<tr><th>FTP</th><td style="color: green;">RUNNING</td></tr>'
    else:
        code += '<tr><th>FTP</th><td style="color: red;">STOP</td></tr>'
        
    if 'is running' in dhc:
        code += '<tr><th>DHCP</th><td style="color: green;">RUNNING</td></tr>'
    else:
        code += '<tr><th>DHCP</th><td style="color: red;">STOP</td></tr>'
        
    if 'is running' in dns:
        code += '<tr><th>DNS</th><td style="color: green;">RUNNING</td></tr>'
    else:
        code += '<tr><th>DNS</th><td style="color: red;">STOP</td></tr>'
        
    if 'is running' in squ:
        code += '<tr><th>SQUID</th><td style="color: green;">RUNNING</td></tr>'
    else:
        code += '<tr><th>SQUID</th><td style="color: red;">STOP</td></tr>'
        
    if 'is running' in smb:
        code += '<tr><th>SAMBA</th><td style="color: green;">RUNNING</td></tr>'
    else:
        code += '<tr><th>SAMBA</th><td style="color: red;">STOP</td></tr>'
        
    if 'is running' in pos:
        code += '<tr><th>POSTFIX</th><td style="color: green;">RUNNING</td></tr>'
    else:
        code += '<tr><th>POSTFIX</th><td style="color: red;">STOP</td></tr>'
    
    dic['$serv'] = code
    
    render('/usr/local/nomad/html/servStatus.html', dic);

def firewall(cmd):
    
    dic = {}
    
    if cmd != '':
        cm.getoutput(cmd)
        
    finp = oneSpace(cm.getoutput('iptables -L INPUT -n --line-number')).split("\n")
    cinp = ''
    if len(finp) > 2:
        finp = finp[2:]
        for f in finp:
            tmp = f.split(' ');
            cinp += '<tr><td>'+tmp[0]+'</td><td>'+tmp[1]+'</td><td>'+tmp[2]+'</td><td>'+tmp[4]+'</td><td>'+tmp[5]+'</td></tr>'
    
    fout = oneSpace(cm.getoutput('iptables -L OUTPUT -n --line-number')).split("\n")
    cout = ''
    if len(fout) > 2:
        fout = fout[2:]
        for f in fout:
            tmp = f.split(' ');
            cout += '<tr><td>'+tmp[0]+'</td><td>'+tmp[1]+'</td><td>'+tmp[2]+'</td><td>'+tmp[4]+'</td><td>'+tmp[5]+'</td></tr>'
    
    ffor = oneSpace(cm.getoutput('iptables -L FORWARD -n --line-number')).split("\n")
    cfor = ''
    if len(ffor) > 2:
        ffor = ffor[2:]
        for f in ffor:
            tmp = f.split(' ');
            cfor += '<tr><td>'+tmp[0]+'</td><td>'+tmp[1]+'</td><td>'+tmp[2]+'</td><td>'+tmp[4]+'</td><td>'+tmp[5]+'</td></tr>'
    
    dic['$finp'] = cinp
    dic['$fout'] = cout
    dic['$ffor'] = cfor
    
    render('/usr/local/nomad/html/firewall.html', dic);

def log(cmd):
    
    dic = {}
    
    clog = ''
    
    if cmd != '':
        cmd = cmd.split("|:|")
        if len(cmd) > 1:
            clog = cm.getoutput('cat '+cmd[0]+'| grep '+cmd[1])
        else:
            clog = cm.getoutput('cat '+cmd[0])
        
        tmp = clog.split("\n")
        clog = ''
        for l in tmp:
            clog += '<tr><td>'+l+'</td></tr>'
        
    
    dic['$log'] = clog
    
    render('/usr/local/nomad/html/logInsp.html', dic);

def render(hFile, dVars):
	arc = open(hFile, 'r')
	code = arc.read()
	arc.close()

	for k in dVars:
		code = code.replace(k, dVars[k])

	print code

def oneSpace(cadena):
	flag = True;
	res = ''
	for c in cadena:
		if c == ' ':
			if flag:
				res += c
				flag = False
		else:
			res += c
			flag = True
	return res


if __name__ == '__main__':
        main()
