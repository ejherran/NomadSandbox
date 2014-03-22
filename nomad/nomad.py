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
        elif(sys.argv[1] == 'filer'):
            if len(sys.argv) == 3:
                filer(b64.b64decode(sys.argv[2]))
            else:
                filer('')
        elif(sys.argv[1] == 'routes'):
            if len(sys.argv) == 3:
                routes(b64.b64decode(sys.argv[2]))
            else:
                routes('')
        elif(sys.argv[1] == 'sshCfg'):
            if len(sys.argv) == 3:
                sshCfg(b64.b64decode(sys.argv[2]))
            else:
                sshCfg('')
        elif(sys.argv[1] == 'mysqlCfg'):
            if len(sys.argv) == 3:
                mysqlCfg(b64.b64decode(sys.argv[2]))
            else:
                mysqlCfg('')
        elif(sys.argv[1] == 'ftpCfg'):
            if len(sys.argv) == 3:
                ftpCfg(b64.b64decode(sys.argv[2]))
            else:
                ftpCfg('')
        elif(sys.argv[1] == 'webCfg'):
            if len(sys.argv) == 3:
                webCfg(b64.b64decode(sys.argv[2]))
            else:
                webCfg('')
        elif(sys.argv[1] == 'mtaCfg'):
            if len(sys.argv) == 3:
                mtaCfg(b64.b64decode(sys.argv[2]))
            else:
                mtaCfg('')
        elif(sys.argv[1] == 'sambaCfg'):
            if len(sys.argv) == 3:
                sambaCfg(b64.b64decode(sys.argv[2]))
            else:
                sambaCfg('')
        elif(sys.argv[1] == 'squidCfg'):
            if len(sys.argv) == 3:
                squidCfg(b64.b64decode(sys.argv[2]))
            else:
                squidCfg('')
        elif(sys.argv[1] == 'dnsCfg'):
            if len(sys.argv) == 3:
                dnsCfg(b64.b64decode(sys.argv[2]))
            else:
                dnsCfg('')
        elif(sys.argv[1] == 'dhcpCfg'):
            if len(sys.argv) == 3:
                dhcpCfg(b64.b64decode(sys.argv[2]))
            else:
                dhcpCfg('')
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
    
    if len(uptime) > 12:
        dic['$up'] = uptime[2]+' '+uptime[3];
        dic['$user'] = uptime[5]+' '+uptime[6]
        dic['$load'] = uptime[8]+' '+uptime[9]+' '+uptime[10]+' '+uptime[11]+' '+uptime[12]

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

def filer(cmd):
    dic = {}
    
    clog = ''
    
    if cmd != '':
        cmd = cmd.split("|:|")
        if len(cmd) > 1:
            arc = open(cmd[0], 'w')
            arc.write(cmd[1])
            arc.close()
    
    render('/usr/local/nomad/html/filer.html', dic);

def routes(cmd):
    dic = {}
    
    if cmd != '':
        arc = open('/usr/local/nomad/cfg/routes.cfg', 'w')
        arc.write(cmd)
        arc.close()
    
    dic = importRoutes('/usr/local/nomad/cfg/routes.cfg')
    render('/usr/local/nomad/html/routes.html', dic);

def sshCfg(cmd):
    
    rou = importRoutes('/usr/local/nomad/cfg/routes.cfg')
    sshf = rou['$ssh_config']+'/sshd_config'
    dic = {}
    
    if cmd != '':
        arc = open(sshf, 'w')
        arc.write(cmd)
        arc.close()
        
    res = {}
    arc = open(sshf, 'r')
    code = arc.read()
    arc.close()
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            if c[0] != '#':
                tmp = c.split(' ')
                if len(tmp) > 1:
                    pic = str(i)+'_'
                    if i < 10:
                        pic = '0'+pic
                    res[pic+tmp[0]] = ' '.join(tmp[1:])
                    i += 1
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        code += '<tr><th>'+tmp[1]+'</th><td><input id="c_'+pic+'" type="text" value=\''+res[r]+'\' /></td></tr>';
    
    dic['$code'] = code
    
    render('/usr/local/nomad/html/ssh.html', dic);

def mysqlCfg(cmd):
    rou = importRoutes('/usr/local/nomad/cfg/routes.cfg')
    mysf = rou['$mysql_config']+'/my.cnf'
    dic = {}
    
    if cmd != '':
        arc = open(mysf, 'w')
        arc.write(cmd)
        arc.close()
        
    res = {}
    arc = open(mysf, 'r')
    code = arc.read()
    arc.close()
    code = code.replace("\t", " ")
    code = oneSpace(code)
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            if c[0] != '#':
                if '=' in c:
                    tmp = c.split('=')
                    if len(tmp) > 1:
                        pic = str(i)+'_'
                        if i < 10:
                            pic = '0'+pic
                        res[pic+tmp[0]] = ' '.join(tmp[1:])
                        i += 1
                elif '[' in c:
                    pic = str(i)+'_'
                    if i < 10:
                        pic = '0'+pic
                    res[pic+c] = ''
                    i += 1
                else:
                    pic = str(i)+'_'
                    if i < 10:
                        pic = '0'+pic
                    res[pic+c] = '*-/-*'
                    i += 1
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        
        if res[r] != '' and res[r] != '*-/-*':
            code += '<tr><th>'+'_'.join(tmp[1:])+'</th><td><input id="c_'+pic+'" type="text" value=\''+res[r]+'\' /></td></tr>';
        elif res[r] == '*-/-*':
            code += '<tr><td colspan="2"><input id="c_'+pic+'" type="text" value=\''+'_'.join(tmp[1:])+'\' /></td></tr>';
        else:
            code += '<tr><th colspan="2">'+'_'.join(tmp[1:])+'</th></tr>';
    
    dic['$code'] = code
    render('/usr/local/nomad/html/mysql.html', dic);

def ftpCfg(cmd):
    rou = importRoutes('/usr/local/nomad/cfg/routes.cfg')
    ftpf = rou['$ftp_config']+'/vsftpd.conf'
    dic = {}
    
    if cmd != '':
        arc = open(ftpf, 'w')
        arc.write(cmd)
        arc.close()
        
    res = {}
    arc = open(ftpf, 'r')
    code = arc.read()
    arc.close()
    code = code.replace("\t", " ")
    code = oneSpace(code)
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            if c[0] != '#':
                if '=' in c:
                    tmp = c.split('=')
                    if len(tmp) > 1:
                        pic = str(i)+'_'
                        if i < 10:
                            pic = '0'+pic
                        res[pic+tmp[0]] = ' '.join(tmp[1:])
                        i += 1
                elif '[' in c:
                    pic = str(i)+'_'
                    if i < 10:
                        pic = '0'+pic
                    res[pic+c] = ''
                    i += 1
                else:
                    pic = str(i)+'_'
                    if i < 10:
                        pic = '0'+pic
                    res[pic+c] = '*-/-*'
                    i += 1
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        
        if res[r] != '' and res[r] != '*-/-*':
            code += '<tr><th>'+'_'.join(tmp[1:])+'</th><td><input id="c_'+pic+'" type="text" value=\''+res[r]+'\' /></td></tr>';
        elif res[r] == '*-/-*':
            code += '<tr><td colspan="2"><input id="c_'+pic+'" type="text" value=\''+'_'.join(tmp[1:])+'\' /></td></tr>';
        else:
            code += '<tr><th colspan="2">'+'_'.join(tmp[1:])+'</th></tr>';
    
    dic['$code'] = code
    render('/usr/local/nomad/html/ftp.html', dic);

def webCfg(cmd):
    rou = importRoutes('/usr/local/nomad/cfg/routes.cfg')
    webf = rou['$apache_config']+'/apache2.conf'
    dic = {}
    
    if cmd != '':
        arc = open(webf, 'w')
        arc.write(cmd)
        arc.close()
        
    res = {}
    arc = open(webf, 'r')
    code = arc.read()
    arc.close()
    code = code.replace("\t", " ")
    code = oneSpace(code)
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            if c[0] != '#':
                pic = str(i)+'_'
                if i < 10:
                    pic = '0'+pic
                res[pic+c] = '*-/-*'
                i += 1
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        
        if res[r] == '*-/-*':
            code += '<tr><td colspan="2"><input id="c_'+pic+'" type="text" value=\''+'_'.join(tmp[1:])+'\' /></td></tr>';
        
    
    dic['$code'] = code
    render('/usr/local/nomad/html/web.html', dic);

def mtaCfg(cmd):
    rou = importRoutes('/usr/local/nomad/cfg/routes.cfg')
    mtaf = rou['$postfix_config']+'/main.cf'
    dic = {}
    
    if cmd != '':
        arc = open(mtaf, 'w')
        arc.write(cmd)
        arc.close()
        
    res = {}
    arc = open(mtaf, 'r')
    code = arc.read()
    arc.close()
    code = code.replace("\t", " ")
    code = oneSpace(code)
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            if c[0] != '#':
                if '=' in c:
                    tmp = c.split('=')
                    if len(tmp) > 1:
                        pic = str(i)+'_'
                        if i < 10:
                            pic = '0'+pic
                        res[pic+tmp[0]] = ' '.join(tmp[1:])
                        i += 1
                
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        
        code += '<tr><th>'+'_'.join(tmp[1:])+'</th><td><input id="c_'+pic+'" type="text" value=\''+res[r]+'\' /></td></tr>';
    
    dic['$code'] = code
    render('/usr/local/nomad/html/mta.html', dic);

def sambaCfg(cmd):
    rou = importRoutes('/usr/local/nomad/cfg/routes.cfg')
    smbf = rou['$samba_config']+'/smb.conf'
    dic = {}
    
    if cmd != '':
        arc = open(smbf, 'w')
        arc.write(cmd)
        arc.close()
        
    res = {}
    arc = open(smbf, 'r')
    code = arc.read()
    arc.close()
    code = code.replace("\t", " ")
    code = oneSpace(code)
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            if c[0] != '#' and c[0] != ';':
                if '=' in c:
                    tmp = c.split('=')
                    if len(tmp) > 1:
                        pic = str(i)+'_'
                        if i < 10:
                            pic = '0'+pic
                        res[pic+tmp[0]] = ' '.join(tmp[1:])
                        i += 1
                elif '[' in c:
                    pic = str(i)+'_'
                    if i < 10:
                        pic = '0'+pic
                    res[pic+c] = ''
                    i += 1
                else:
                    pic = str(i)+'_'
                    if i < 10:
                        pic = '0'+pic
                    res[pic+c] = '*-/-*'
                    i += 1
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        
        if res[r] != '' and res[r] != '*-/-*':
            code += '<tr><th>'+'_'.join(tmp[1:])+'</th><td><input id="c_'+pic+'" type="text" value=\''+res[r]+'\' /></td></tr>';
        elif res[r] == '*-/-*':
            code += '<tr><td colspan="2"><input id="c_'+pic+'" type="text" value=\''+'_'.join(tmp[1:])+'\' /></td></tr>';
        else:
            code += '<tr><th colspan="2">'+'_'.join(tmp[1:])+'</th></tr>';
    
    dic['$code'] = code
    render('/usr/local/nomad/html/samba.html', dic);

def squidCfg(cmd):
    rou = importRoutes('/usr/local/nomad/cfg/routes.cfg')
    squf = rou['$squid_config']+'/squid.conf'
    dic = {}
    
    if cmd != '':
        arc = open(squf, 'w')
        arc.write(cmd)
        arc.close()
        
    res = {}
    arc = open(squf, 'r')
    code = arc.read()
    arc.close()
    code = code.replace("\t", " ")
    code = oneSpace(code)
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            if c[0] != '#':
                pic = str(i)+'_'
                if i < 10:
                    pic = '0'+pic
                res[pic+c] = '*-/-*'
                i += 1
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        
        if res[r] == '*-/-*':
            code += '<tr><td colspan="2"><input id="c_'+pic+'" type="text" value=\''+'_'.join(tmp[1:])+'\' /></td></tr>';
        
    
    dic['$code'] = code
    render('/usr/local/nomad/html/squid.html', dic);

def dnsCfg(cmd):
    rou = importRoutes('/usr/local/nomad/cfg/routes.cfg')
    locf = rou['$dns_config']+'/named.conf.local'
    optf = rou['$dns_config']+'/named.conf.options'
    zonf = rou['$dns_config']+'/named.conf.default-zones'
    dic = {}
    
    if cmd != '':
        cmd = cmd.split('|:|')
        for c in cmd:
            p = c.split('|>|')
            if len(p) == 2:
                arc = ''
                if p[0] == 'local':
                    arc = open(locf, 'w')
                elif p[0] == 'option':
                    arc = open(optf, 'w')
                elif p[0] == 'zone':
                    arc = open(zonf, 'w')
                arc.write(p[1])
                arc.close()
                    
    res = {}
    arc = open(locf, 'r')
    code = arc.read()
    arc.close()
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            c = remInitSpace(c)
            if c[0] != '#' and c[0:2] != '//':
                pic = str(i)+'_'
                if i < 10:
                    pic = '0'+pic
                res[pic+c] = '*-/-*'
                i += 1
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        
        if res[r] == '*-/-*':
            code += '<tr><td colspan="2"><input id="l_'+pic+'" type="text" value=\''+'_'.join(tmp[1:])+'\' /></td></tr>';
    
    dic['$local'] = code
    
    res = {}
    arc = open(optf, 'r')
    code = arc.read()
    arc.close()
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            c = remInitSpace(c)
            if c[0] != '#' and c[0:2] != '//':
                pic = str(i)+'_'
                if i < 10:
                    pic = '0'+pic
                res[pic+c] = '*-/-*'
                i += 1
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        
        if res[r] == '*-/-*':
            code += '<tr><td colspan="2"><input id="o_'+pic+'" type="text" value=\''+'_'.join(tmp[1:])+'\' /></td></tr>';
    dic['$option'] = code
    
    res = {}
    arc = open(zonf, 'r')
    code = arc.read()
    arc.close()
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            c = remInitSpace(c)
            if c[0] != '#' and c[0:2] != '//':
                pic = str(i)+'_'
                if i < 10:
                    pic = '0'+pic
                res[pic+c] = '*-/-*'
                i += 1
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        
        if res[r] == '*-/-*':
            code += '<tr><td colspan="2"><input id="z_'+pic+'" type="text" value=\''+'_'.join(tmp[1:])+'\' /></td></tr>';
    dic['$zone'] = code
    
    
    render('/usr/local/nomad/html/dns.html', dic);

def dhcpCfg(cmd):
    rou = importRoutes('/usr/local/nomad/cfg/routes.cfg')
    dhcf = rou['$dhcp_config']+'/dhcpd.conf'
    dic = {}
    
    if cmd != '':
        arc = open(dhcf, 'w')
        arc.write(cmd)
        arc.close()
        
    res = {}
    arc = open(dhcf, 'r')
    code = arc.read()
    arc.close()
    code = code.replace("\t", " ")
    code = oneSpace(code)
    code = code.split("\n")
    i = 1;
    for c in code:
        if len(c) > 0:
            if c[0] != '#':
                pic = str(i)+'_'
                if i < 10:
                    pic = '0'+pic
                res[pic+c] = '*-/-*'
                i += 1
    code = ''
    for r in sorted(res.keys()):
        tmp = r.split('_')
        pic = str(int(tmp[0]))
        
        if res[r] == '*-/-*':
            code += '<tr><td colspan="2"><input id="c_'+pic+'" type="text" value=\''+'_'.join(tmp[1:])+'\' /></td></tr>';
        
    
    dic['$code'] = code
    render('/usr/local/nomad/html/dhcp.html', dic);

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

def importRoutes(path):
    res = {}
    arc = open(path, 'r')
    code = arc.read()
    arc.close()
    code = code.split("\n")
    for c in code:
        tmp = c.split(": ")
        if len(tmp) == 2:
            res['$'+tmp[0]] = tmp[1]
    
    return res

def remInitSpace(cadena):
    i = 0
    for c in cadena:
        if c == ' ' or c == "\t":
            i += 1
        else:
            break
    return cadena[i:]

if __name__ == '__main__':
        main()
