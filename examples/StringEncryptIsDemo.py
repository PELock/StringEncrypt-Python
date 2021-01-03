#!/usr/bin/env python

###############################################################################
#
# StringEncrypt WebApi interface usage example.
#
# In this example we will verify our activation code status.
#
# Version        : v1.0
# Language       : Python
# Author         : Bartosz Wójcik
# Project page   : https://www.stringencrypt.com
# Web page       : https://www.pelock.com
#
###############################################################################

#
# include StringEncrypt module
#
from stringencrypt import StringEncrypt

#
# if you don't want to use Python module, you can import it directly from the file
#
#from stringencrypt.stringencrypt import StringEncrypt

#
# create StringEncrypt class instance (we are using our activation code)
#
myStringEncrypt = StringEncrypt("ABCD-ABCD-ABCD-ABCD")

#
# login to the service
#
result = myStringEncrypt.is_demo()

#
# result[] array holds the information about the license
#
# result["demo"] (boolean) - demo mode flag
# result["label_limit"] (int) - label limit length
# result["string_limit"] (int) - string limit length
# result["bytes_limit"] (int) - bytes/file limit length
# result["credits_left"] (int) - number of credits left
# result["credits_total"] (int) - initial number of credits
# result["cmd_min"] (int) - minimum number of encryption commands
# result["cmd_max"] (int) - maximum number of encryption commands
#
if result:

	print(f'Demo version status - {"True" if result["demo"] else "False"}')

	print(f'Label length limit - {result["label_limit"]}')
	print(f'String length limit - {result["string_limit"]}')

	print(f'File bytes limit - {result["bytes_limit"]}')

	print(f'Usage credits left - {result["credits_left"]}')
	print(f'Total usage credits - {result["credits_total"]}')

	print(f'Min. number of encryption commands - {result["cmd_min"]}')
	print(f'Max. number of encryption commands - {result["cmd_max"]}')

else:
	print("Something unexpected happen while trying to login to the service.")
