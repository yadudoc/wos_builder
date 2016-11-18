#!/bin/bash

### Installation
# sudo pip install jupyter
### Generate sha hash of a password using python
# from notebook.auth import passwd
# passwd() # this will ask for password
### Copy the sha hash into ~/.jupyter/jupyter_notebook_config.py
#
###  Set the following in the same config file
# c.NotebookApp.ip = '*'
#c.NotebookApp.password = u'sha1:bcd259ccf...<your hashed password here>'
#c.NotebookApp.open_browser = False

# It is a good idea to set a known, fixed port for server access
#c.NotebookApp.port = 9999


### Create Certificate
# openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mykey.key -out mycert.pem
### Start notebook

jupyter notebook --certfile=mycert.pem --keyfile mykey.key
