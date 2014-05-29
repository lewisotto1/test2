#!/usr/bin/python

import os
from subprocess import call
my_in = "/etc/nginx/sites-available"
my_in_name = input('enter server name: ')
try:
    file1 = open(my_in+my_in_name, 'r+')
except IOError:
    str('cannot open file.')
    exit()
s = 'file'+repr(my_in)+'opened'
print(s)
my_in_port = "80"
myRoot = "/usr/share/nginx/html/"
myRoot += my_in_name
my_in_php = input('do you want php? [yes/no]: ')
if not os.path.exists(myRoot):
    os.makedirs(myRoot)
my_in_type = input('import files form github or rsync? [rsync/git]: ')
if my_in_type == 'rsync':
    my_in_ip = input('ip, user and directory to import from: ')
    call(["rsync", "-azv", my_in_ip, myRoot])
elif my_in_type == 'git':
    my_in_files = input('git url: ')
    call(["git", "clone", my_in_files, myRoot])
else:
    str('Invalid input, continuing...')
asdf = my_in_files.rsplit('/')[4]
asdf = asdf[:-4]
myRoot2 = myRoot + asdf
server_cfg = "server {\nlitsen "+my_in_port+"\nserver_name "+my_in_name+" www."+my_in_name+"\n\nlocation / "
server_cfg += "{\n root "+myRoot2+"\n Index   index.php index.html index.htm\n}\n\n"
if my_in_php == 'yes':
    server_cfg += "location ~ \.php$ {\n include /etc/nginx/fastcgi_params;\n"
    server_cfg += " fastcgi_pass unix:/tmp/php5-fpm.sock;\n fastcgi_index index.php\n"
    server_cfg += " fastcgi_param SCRIPT_FILENAME "+myRoot2+"$fast_cgi_scriptname;\n}\n"

server_cfg += "}\n"
file1.write(server_cfg)
file1.close()
link = input('ln to enabled?[yes/no]: ')
if link == 'yes':
    call(["ln", "-s", "/etc/nginx/sites-available/"+my_in_name, "/etc/nginx/sites-enabled"+my_in_name])
call(["chmod", "755", "-R", myRoot])
call(["service", "nginx", "reload"])
str('exiting')
exit()