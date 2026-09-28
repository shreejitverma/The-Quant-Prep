# set options for certfile, ip, password, and toggle off browser auto-opening
#
# execute the bash script generate_rsa_ssl.sh to generate your certificate files
# replace the following file names (and files used) by your choice/files
c.NotebookApp.certfile = u'/root/mycert.pem'
c.NotebookApp.keyfile = u'/root/mykey.key'

# set ip to '*' to bind on all interfaces (ips) for the public server
c.NotebookApp.ip = '*'

# to generate a password hash, do in Python:
#
# from notebook.auth import passwd
# passwd()
#
# here: 'jupyter' as password
# replace the hash key with the one for your password
c.NotebookApp.password = 'sha1:bb5e01be158a:99465f872e0613a3041ec25b7860175f59847702'

c.NotebookApp.open_browser = False

# it is a good idea to set a known, fixed default port for server access
c.NotebookApp.port = 8888
