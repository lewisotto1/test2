#!/usr/bin/python3

__author__ = 'lewis'
#usage: script to create nginx server blocks, also automates creation of directories and
#also can download from github or retrieve via rsync

import os
from subprocess import call
my_in = "/etc/nginx/sites-available/"
my_in_name = input('enter server name: ')
try:
    file1 = open(my_in+my_in_name, 'w+')
except IOError:
    print(str('cannot open file.'))
    exit(1)
s = 'file'+repr(my_in_name)+'opened'
print(s)
my_in_port = "80"
myRoot = "/usr/share/nginx/html/"
myRoot += my_in_name
my_in_php = input('do you want php? [yes/no]: ')
my_in_ssl = input('http or SSL [ssl]: ')
my_in_type = input('import files from github, rsync or portable storage? [rsync/git/usb]: ')
if my_in_type == 'rsync':
    my_in_ip = input('ip, user and directory to import from: ')
    call(["rsync", "-azv", my_in_ip, myRoot])
elif my_in_type == 'git':
    my_in_files = input('git url: ')
    call(["git", "clone", my_in_files, myRoot])
elif my_in_type == 'usb':
    my_in_files = input('directory: ')
    call(["rsync", "-azv", my_in_files, myRoot])
else:
    print(str('no files selected, continuing...'))
if not os.path.exists(myRoot):
    os.makedirs(myRoot)
    os.makedirs(myRoot+"/logs")
if my_in_ssl == 'ssl':
    my_in_port = "443 ssl"
server_cfg = "server {\nlisten "+my_in_port+"\nserver_name "+my_in_name+" www."+my_in_name+"\n\nlocation / "
if my_in_ssl == 'ssl':
    server_cfg += "  ssl_certificate "+my_in_name+".crt;\n  ssl_certificate_key "+my_in_name+".key;"
server_cfg += "{\n root "+myRoot+"\n Index   index.php index.html index.htm\n}\n\n"
if my_in_php == 'yes':
    server_cfg += "location ~ \.php$ {\n include /etc/nginx/fastcgi_params;\n"
    server_cfg += " fastcgi_pass 127.0.0.1:9000;\n fastcgi_index index.php;\n"
    #server_cfg += " fastcgi_pass unix:/tmp/php5-fpm.sock;\n fastcgi_index index.php;\n"
    server_cfg += " fastcgi_param SCRIPT_FILENAME "+myRoot+"$fast_cgi_scriptname;\n}\n"
server_cfg += "location ~ /\. {\n  access_log off;\n  log_not_found off;\n  deny all;\n}\n}"
file1.write(server_cfg)
file1.close()
link = input('link to enabled?[yes/no]: ')
if link == 'yes':
    call(["ln", "-s", "/etc/nginx/sites-available/"+my_in_name, "/etc/nginx/sites-enabled/"+my_in_name])
call(["chmod", "755", "-R", myRoot])
call(["service", "nginx", "reload"])
print(str('exiting'))
exit()