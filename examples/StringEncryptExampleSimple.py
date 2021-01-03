#!/usr/bin/env python

###############################################################################
#
# String Encrypt WebApi interface usage example.
#
# In this example we will encrypt sample string with default options.
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
# encrypt a string using all the default options
#
result = myStringEncrypt.encrypt_string("Hello, world!", "label_encrypted")

#
# result[] array holds the encryption results as well as other information
#
# result["error"] (int) - error code
# result["source"] (string) - decryptor source code
# result["expired"] (boolean) - expiration flag
# result["credits_left"] (int) - number of credits left
# result["credits_total"] (int) - initial number of credits

if result and "error" in result:

    # display source code of the decryption code
    if result["error"] == StringEncrypt.ErrorCodes.ERROR_SUCCESS:
        print(result["source"])
    else:
        print(f'An error occurred, error code: {result["error"]} ({result["error_string"]})')

else:
    print("Something unexpected happen while trying to encrypt the string.")
