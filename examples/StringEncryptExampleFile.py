#!/usr/bin/env python

###############################################################################
#
# String Encrypt WebApi interface usage example.
#
# In this example we will encrypt sample file with default options.
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
# encrypt current script file using all the default options
#
result = myStringEncrypt.encrypt_file_contents(__file__, "label_file_encrypted")

#
# result[] array holds the encryption results as well as other information
#
# result["error"] (int) - error code
# result["error_string"] (string) - error code as a string
# result["source"] (string) - decryptor source code
# result["expired"] (boolean) - expiration flag
# result["credits_left"] (int) - number of credits left
# result["credits_total"] (int) - initial number of credits

if result and "error" in result:

    if result["error"] == StringEncrypt.ErrorCodes.ERROR_SUCCESS:

        # display source code of the decryption function
        print(result["source"])

        # we can even exec() it (block of code), to run it and
        # display decrypted label, which contains this script
        # source code
        exec(result["source"])

        # label is declared at this point, display its content
        print(label_file_encrypted)

    else:
        print(f'An error occurred, error code: {result["error"]} ({result["error_string"]})')

else:
    print("Something unexpected happen while trying to encrypt the string.")
