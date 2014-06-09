#!/usr/bin/python3

__author__ = 'lewis'
#usage: script to create nginx server blocks, also automates creation of directories and
#also can download from github or retrieve via rsync
#USAGE: server_name, -git(github), -r(rsync), -p(php), -s(ssl), -l(link)

import os
from subprocess import call
import argparse

parser = argparse.ArgumentParser(description="Nginx server block creator")
parser.add_argument('server', help="Server name")
parser.add_argument('-g', "--git", help="Git url for files")
parser.add_argument('-r', "--rsync", help="Rsync for files")
parser.add_argument('-p', "--php", action='store_true', help="Include php block")
parser.add_argument('-s', "--ssl", action='store_true', help="make block SSL")
parser.add_argument('-l', "--ls", action='store_true', help="link files to enabled")
args = parser.parse_args()
try:
    file1 = open("/etc/nginx/sites-available/"+args.server, 'w+')
except IOError:
    print(str('cannot open file.'))
    exit(1)
myRoot = "/usr/share/nginx/html/"
myRoot += args.server
if args.rsync:
    my_in_ip = input('ip, user and directory to import from: ')
    call(["rsync", "-azv", my_in_ip, myRoot])
elif args.git:
    my_in_files = input('git url: ')
    call(["git", "clone", my_in_files, myRoot])
    call(["chmod", "600", myRoot+".git"])
else:
    print(str('no files selected, continuing...'))
if not os.path.exists(myRoot):
    os.makedirs(myRoot)
    os.makedirs(myRoot+"/logs")
if args.ssl:
    server_cfg = "server {{\nlisten 443 ssl;\nserver_name {} www.{};\n\nlocation / {".format(args.server, args.server)
    server_cfg += "\n  ssl_certificate {}.crt;\n ssl_certificate_key {}.key;".format(args.server, args.server)
else:
    server_cfg = "server {{\nlisten 80;\nserver_name {} www.{}\n\nlocation /".format(args.server, args.server)
server_cfg += "\n root {}\n Index   index.php index.html index.htm\n}}\n\n".format(myRoot)
if args.php:
    server_cfg += "location ~ \.php$ {\n include /etc/nginx/fastcgi_params;\n"
    server_cfg += " fastcgi_pass 127.0.0.1:9000;\n fastcgi_index index.php;\n"
    #server_cfg += " fastcgi_pass unix:/tmp/php5-fpm.sock;\n fastcgi_index index.php;\n"
    server_cfg += " fastcgi_param SCRIPT_FILENAME {}$fast_cgi_scriptname;\n}}\n".format(myRoot)
server_cfg += "location ~ /\. {\n  access_log off;\n  log_not_found off;\n  deny all;\n}\n}"
file1.write(server_cfg)
file1.close()
if args.ls:
    call(["ln", "-s", "/etc/nginx/sites-available/"+args.server, "/etc/nginx/sites-enabled/"+args.server])
call(["chmod", "755", "-R", myRoot])
call(["service", "nginx", "reload"])
print(str('exiting'))
exit()
