#!/usr/bin/env python

###############################################################################
#
# String Encryption and File Encryption for programmers & developers
#
# String Encrypt can help you hide the things that shouldn't be visible at
# first glance in your source code to anyone with a hex-editor.
#
# Supported programming languages code generation:
#
#  * C/C++ - https://www.stringencrypt.com/c-cpp-encryption/
#  * C# - https://www.stringencrypt.com/c-sharp-encryption/
#  * Visual Basic .NET - https://www.stringencrypt.com/visual-basic-net-vb-net-encryption/
#  * Delphi/Pascal - https://www.stringencrypt.com/delphi-pascal-encryption/
#  * Java - https://www.stringencrypt.com/java-encryption/
#  * JavaScript - https://www.stringencrypt.com/javascript-encryption/
#  * Python - https://www.stringencrypt.com/python-encryption/
#  * Ruby - https://www.stringencrypt.com/ruby-encryption/
#  * AutoIt - https://www.stringencrypt.com/autoit-encryption/
#  * PowerShell - https://www.stringencrypt.com/powershell-encryption/
#  * Haskell - https://www.stringencrypt.com/haskell-encryption/
#  * MASM - https://www.stringencrypt.com/masm-encryption/
#  * FASM - https://www.stringencrypt.com/fasm-encryption/
#
# Version      : StringEncrypt v1.0
# Python       : Python v3
# Dependencies : requests (https://pypi.python.org/pypi/requests/)
# Author       : Bartosz Wójcik (support@pelock.com)
# Project page : https://www.stringencrypt.com
# Web page     : https://www.pelock.com
#
###############################################################################

import zlib
import base64
from enum import *

# required external package - install with "pip install requests"
import requests


class StringEncrypt(object):
    """StringEncrypt Python 3 module"""

    # 
    # @var string default StringEncrypt WebApi endpoint
    # 
    API_URL = "https://www.stringencrypt.com/api.php"

    # 
    # @var string WebApi key for the service
    # 
    _activationCode = ""

    #
    # @var bool input string / raw bytes compression enabled (enabled by default)
    #
    # if you set it to true, you need to compress input string / raw bytes eg.
    #
    # compressed = @base64_encode(@gzcompress(string, 9)
    #
    # and after encryption you need to decompress encrypted data
    #
    # decompressed = @gzuncompress(@base64_decode(source));
    #
    # options["compression"] = true/false
    enableCompression = True

    #
    # @var bool treat input string as a UNICODE string (ANSI otherwise)
    #
    # options["unicode"] = true/false
    useUnicode = True

    class LangLocaleEncodings(Enum):
        """Input string default locale (only those listed below are supported currently)"""

        def __str__(self):
            return self.value

        LANG_US = "en_US.utf8"
        LANG_GB = "en_GB.utf8"
        LANG_DE = "de_DE.utf8"
        LANG_ES = "es_ES.utf8"
        LANG_BE = "fr_BE.utf8"
        LANG_FR = "fr_FR.utf8"
        LANG_PL = "pl_PL.utf8"

    #
    # @var string input string locate for UTF-8 encoded strings (en_US encoding is used by default )
    #
    langLocaleEncoding = LangLocaleEncodings.LANG_US

    class NewLinesEncodings(Enum):
        """How to encode new lines, available values:

        "lf" - Unix style
        "crlf" - Windows style
        "cr" - Mac style"""

        def __str__(self):
            return self.value

        UNIX_STYLE_LF = "lf"
        WINDOWS_STYLE_CRLF = "crlf"
        MAC_STYLE_CR = "cr"

    #
    # @var string How to encode new lines (Unix LF is used by default)
    #
    newLinesEncoding = NewLinesEncodings.UNIX_STYLE_LF

    class AnsiEncodings(Enum):
        """Destination ANSI string encoding (if UNICODE encoding is disabled)
        only those listed below are supported"""

        def __str__(self):
            return self.value

        WINDOWS_1250 = "WINDOWS-1250"
        WINDOWS_1251 = "WINDOWS-1251"
        WINDOWS_1252 = "WINDOWS-1252"
        WINDOWS_1253 = "WINDOWS-1253"
        WINDOWS_1254 = "WINDOWS-1254"
        WINDOWS_1255 = "WINDOWS-1255"
        WINDOWS_1256 = "WINDOWS-1256"
        WINDOWS_1257 = "WINDOWS-1257"
        WINDOWS_1258 = "WINDOWS-1258"
        ISO_8859_1 = "ISO-8859-1"
        ISO_8859_2 = "ISO-8859-2"
        ISO_8859_3 = "ISO-8859-3"
        ISO_8859_9 = "ISO-8859-9"
        ISO_8859_10 = "ISO-8859-10"
        ISO_8859_14 = "ISO-8859-14"
        ISO_8859_15 = "ISO-8859-15"
        ISO_8859_16 = "ISO-8859-16"

    #
    # @var string ANSI encoding if UNICODE mode is disabled (WINDOWS-1250 encoding is used by default)
    #
    ansiEncoding = AnsiEncodings.WINDOWS_1250

    class OutputProgrammingLanguages(Enum):
        """Output programming language.

        Only those listed below are supported, if you pass
        other name, service will return ERROR_INVALID_LANG"""

        def __str__(self):
            return self.value

        LANG_CPP = "cpp"
        LANG_CSHARP = "csharp"
        LANG_VBNET = "vbnet"
        LANG_DELPHI = "delphi"
        LANG_JAVA = "java"
        LANG_JS = "js"
        LANG_PYTHON = "python"
        LANG_RUBY = "ruby"
        LANG_AUTOIT = "autoit"
        LANG_POWERSHELL = "powershell"
        LANG_HASKELL = "haskell"
        LANG_MASM = "masm"
        LANG_FASM = "fasm"

    #
    # @var string Generate output source code in selected programming language (Python is selected by default)
    #
    outputProgrammingLanguage = OutputProgrammingLanguages.LANG_PYTHON

    #
    # @var integer minimum number of encryption commands
    #
    # Demo mode supports only up to 3 commands (50 in full version),
    # if you pass more than this number, service will return
    # ERROR_CMD_MIN
    #
    # options["cmd_min"] = 1
    minEncryptionCommands = 1

    #
    # @var integer maximum number of encryption commands
    #
    # demo mode supports only up to 3 commands (50 in full version),
    # if you pass more than this number, service will return
    # ERROR_CMD_MAX
    #
    # options["cmd_max"] = 50
    maxEncryptionCommands = 3

    #
    # @var bool store encrypted string as a local variable (if supported
    # by the programming language), otherwise it's stored as
    # a global variable
    #
    # options["local"] = true/false
    declareAsLocalVariable = False

    class ErrorCodes(IntEnum):
        """Possible error codes returned by the StringEncrypt WebAPI service"""

        # @var integer success
        ERROR_SUCCESS = 0

        # @var integer label parameter is missing
        ERROR_EMPTY_LABEL = 1

        # @var integer label length is too long
        ERROR_LENGTH_LABEL = 2

        # @var integer input string is missing
        ERROR_EMPTY_STRING = 3

        # @var integer input file is missing
        ERROR_EMPTY_BYTES = 4

        # @var integer input string/file is missing
        ERROR_EMPTY_INPUT = 5

        # @var integer string length is too long
        ERROR_LENGTH_STRING = 6

        # @var integer bytes length is too long
        ERROR_LENGTH_BYTES = 11

        # @var integer programming language not supported
        ERROR_INVALID_LANG = 7

        # @var integer invalid locale defined
        ERROR_INVALID_LOCALE = 8

        # @var integer min. number of encryption commands error
        ERROR_CMD_MIN = 9

        # @var integer max. number of encryption commands error
        ERROR_CMD_MAX = 10

        # @var integer you need a valid code to use full version features
        ERROR_DEMO = 100

    def __init__(self, activation_code=None):
        """Initialize StringEncrypt class

        :param api_key: Activation code for the service (it can be empty for demo mode)
        """

        self._activationCode = activation_code

    def is_demo(self):
        """Login to the service using previously provided activation code and get the
         information about the current license limits

        :return: An array with the results or False on error
        :rtype: bool,dict
        """

        # parameters
        params = {"command": "is_demo"}

        return self.post_request(params)

    def encrypt_file_contents(self, file_path, label):
        """Encrypt binary file contents

        :param file_path: A path to any binary file. Demo mode doesn't support
        this parameter and the service will return ERROR_DEMO

        :param label: A label name. Demo mode supports up to 10 chars only
        (64 in full version), if you pass more than this number, service
        will return ERROR_LENGTH_LABEL

        :return: An array with the results or False on error
        :rtype: bool,dict
        """

        source_file = open(file_path, 'rb')
        bytes = source_file.read()
        source_file.close()
    
        if not bytes:
            return False
    
        # additional parameters
        params_array = {"command": "encrypt", "bytes": bytes, "label": label}

        return self.post_request(params_array)

    def encrypt_string(self, string, label):
        """Encrypt a string into an encrypted source code in selected programming language

        :param string: An input string in UTF-8 or ANSI format (by default UTF-8 is used)
        demo mode supports up to 10 chars only, if you pass more
        than that, service will return ERROR_LENGTH_STRING

        :param label: label name. Demo mode supports up to 10 chars only
        (64 in full version), if you pass more than this number, service
        will return ERROR_LENGTH_LABEL

        :return: An array with the results or False on error
        :rtype: bool,dict
        """

        # additional parameters
        params_array = {"command": "encrypt", "string": string, "label": label}

        return self.post_request(params_array)

    def post_request(self, params_array):
        """Send a POST request to the server

        :param params_array: An array with the parameters
        :return: An array with the results or false on error
        :rtype: bool,dict
        """

        # add activation code to the parameters array
        params_array["code"] = self._activationCode

        # setup parameters for the "encrypt" command ("is_demo" doesn't require it)
        if params_array["command"] == "encrypt":

            params_array["unicode"] = 1 if self.useUnicode else 0
            params_array["lang_locale"] = self.langLocaleEncoding
            params_array["ansi_encoding"] = self.ansiEncoding

            params_array["local"] = 1 if self.declareAsLocalVariable else 0

            params_array["new_lines"] = self.newLinesEncoding

            # number of encryption commands
            params_array["cmd_min"] = self.minEncryptionCommands
            params_array["cmd_max"] = self.maxEncryptionCommands

            params_array["lang"] = self.outputProgrammingLanguage

            #
            # check if compression is enabled
            #
            if self.enableCompression:

                params_array["compression"] = "1"

                if "string" in params_array and params_array["string"]:

                    compressed_data = zlib.compress(bytes(params_array["string"], 'utf-8'), 9)
                    base64_encoded_data = base64.b64encode(compressed_data).decode()
                    params_array["string"] = base64_encoded_data

                elif "bytes" in params_array and params_array["bytes"]:

                    compressed_data = zlib.compress(bytes(params_array["bytes"]), 9)
                    base64_encoded_data = base64.b64encode(compressed_data).decode()
                    params_array["bytes"] = base64_encoded_data

        response = requests.post(self.API_URL, data=params_array)

        # no response at all or an invalid response code
        if not response or not response.ok:
            return False

        # decode to json array
        result = response.json()

        # depack output code back into the string
        if "source" in result and self.enableCompression and result["error"] == self.ErrorCodes.ERROR_SUCCESS:
            result["source"] = str(zlib.decompress(base64.b64decode(result["source"])), "utf-8")

        # append error code in string format
        if "error" in result:
            result["error_string"] = self.ErrorCodes(result["error"]).name

        # return original JSON response code
        return result
