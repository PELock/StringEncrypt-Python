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
#  * Go - https://www.stringencrypt.com/go-encryption/
#  * Rust - https://www.stringencrypt.com/rust-encryption/
#  * Swift - https://www.stringencrypt.com/swift-encryption/
#  * Kotlin - https://www.stringencrypt.com/kotlin-encryption/
#  * Lua - https://www.stringencrypt.com/lua-encryption/
#  * Dart - https://www.stringencrypt.com/dart-encryption/
#  * PHP - https://www.stringencrypt.com/php-encryption/
#  * Objective-C - https://www.stringencrypt.com/objective-c-encryption/
#  * NASM - https://www.stringencrypt.com/nasm-encryption/
#
# Version      : StringEncrypt v1.0.1
# Python       : Python v3
# Dependencies : requests (https://pypi.python.org/pypi/requests/)
# Author       : Bartosz Wójcik (support@pelock.com)
# Project page : https://www.stringencrypt.com
# Web page     : https://www.pelock.com
#
###############################################################################

import base64
import json
import zlib
from enum import Enum, IntEnum
from pathlib import Path
from typing import Any, Dict, Optional, Union

import requests


class StringEncrypt:
    """StringEncrypt Python 3 WebAPI client."""

    API_URL = "https://www.stringencrypt.com/api.php"

    _activationCode: str

    enableCompression = True
    useUnicode = True

    class LangLocaleEncodings(Enum):
        """Input string default locale (only those listed below are supported currently)"""

        def __str__(self) -> str:
            return str(self.value)

        LANG_US = "en_US.utf8"
        LANG_GB = "en_GB.utf8"
        LANG_DE = "de_DE.utf8"
        LANG_ES = "es_ES.utf8"
        LANG_BE = "fr_BE.utf8"
        LANG_FR = "fr_FR.utf8"
        LANG_PL = "pl_PL.utf8"

    langLocaleEncoding = LangLocaleEncodings.LANG_US

    class NewLinesEncodings(Enum):
        """How to encode new lines, available values:

        "lf" - Unix style
        "crlf" - Windows style
        "cr" - Mac style"""

        def __str__(self) -> str:
            return str(self.value)

        UNIX_STYLE_LF = "lf"
        WINDOWS_STYLE_CRLF = "crlf"
        MAC_STYLE_CR = "cr"

    newLinesEncoding = NewLinesEncodings.UNIX_STYLE_LF

    class AnsiEncodings(Enum):
        """Destination ANSI string encoding (if UNICODE encoding is disabled)
        only those listed below are supported"""

        def __str__(self) -> str:
            return str(self.value)

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

    ansiEncoding = AnsiEncodings.WINDOWS_1250

    class OutputProgrammingLanguages(Enum):
        """Output programming language.

        Only those listed below are supported, if you pass
        other name, service will return ERROR_INVALID_LANG"""

        def __str__(self) -> str:
            return str(self.value)

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
        LANG_GO = "go"
        LANG_RUST = "rust"
        LANG_SWIFT = "swift"
        LANG_KOTLIN = "kotlin"
        LANG_LUA = "lua"
        LANG_DART = "dart"
        LANG_PHP = "php"
        LANG_OBJC = "objc"
        LANG_NASM = "nasm"

    outputProgrammingLanguage = OutputProgrammingLanguages.LANG_PYTHON

    minEncryptionCommands = 1
    maxEncryptionCommands = 3

    declareAsLocalVariable = False

    # Mirrors api.php when keys are omitted (PHP filter_var on missing booleans is false).
    includeTags = False
    includeExample = False
    # False = omit (server default); str e.g. "js" / "geshi" for syntax-highlighted HTML.
    highlight: Union[bool, str] = False
    encryptionTemplate: Optional[str] = None
    returnTemplate = False
    includeDebugComments = False

    class ErrorCodes(IntEnum):
        """Possible error codes returned by the StringEncrypt WebAPI service"""

        ERROR_SUCCESS = 0
        ERROR_EMPTY_LABEL = 1
        ERROR_LENGTH_LABEL = 2
        ERROR_EMPTY_STRING = 3
        ERROR_EMPTY_BYTES = 4
        ERROR_EMPTY_INPUT = 5
        ERROR_LENGTH_STRING = 6
        ERROR_INVALID_LANG = 7
        ERROR_INVALID_LOCALE = 8
        ERROR_CMD_MIN = 9
        ERROR_CMD_MAX = 10
        ERROR_LENGTH_BYTES = 11
        ERROR_DEMO = 100

    def __init__(
        self,
        activation_code: Optional[str] = None,
        *,
        timeout: float = 30.0,
        session: Optional[requests.Session] = None,
    ) -> None:
        """Initialize StringEncrypt client.

        :param activation_code: Activation code for the service (empty or None for demo mode).
        :param timeout: HTTP read/connect timeout in seconds (passed to ``requests``).
        :param session: Optional ``requests.Session`` for connection reuse and testing.
        """
        self._activationCode = activation_code or ""
        self._timeout = timeout
        self._session = session if session is not None else requests.Session()

    def info(self) -> Union[Dict[str, Any], bool]:
        """Query server engine version and supported output languages (``command=info``).

        :return: Parsed JSON on success, or ``False`` on transport/parse failure.
        """
        return self.post_request({"command": "info"})

    def is_demo(self) -> Union[Dict[str, Any], bool]:
        """Return activation status and limits for the current activation code.

        :return: Parsed JSON on success, or ``False`` on transport/parse failure.
        """
        return self.post_request({"command": "is_demo"})

    def encrypt_file_contents(
        self, file_path: Union[str, Path], label: str
    ) -> Union[Dict[str, Any], bool]:
        """Encrypt binary file contents.

        :param file_path: Path to a binary file. Demo mode returns ``ERROR_DEMO``.
        :param label: Variable label (demo: max length enforced server-side).
        :return: Parsed JSON on success, or ``False`` on empty file / transport / parse failure.
        """
        path = Path(file_path)
        with path.open("rb") as handle:
            raw = handle.read()

        if not raw:
            return False

        params_array: Dict[str, Any] = {"command": "encrypt", "bytes": raw, "label": label}
        return self.post_request(params_array)

    def encrypt_string(self, string: str, label: str) -> Union[Dict[str, Any], bool]:
        """Encrypt a UTF-8 string into decryptor source for ``outputProgrammingLanguage``.

        When ``enableCompression`` is True, the string is gzip-compressed client-side before
        upload; the wire format is still UTF-8 bytes of the original string (same as prior SDK).

        :return: Parsed JSON on success, or ``False`` on transport/parse failure.
        """
        params_array = {"command": "encrypt", "string": string, "label": label}
        return self.post_request(params_array)

    @staticmethod
    def _error_code_to_string(code: Any) -> str:
        try:
            return StringEncrypt.ErrorCodes(int(code)).name
        except ValueError:
            return "ERROR_UNKNOWN_%s" % (code,)

    def post_request(self, params_array: Dict[str, Any]) -> Union[Dict[str, Any], bool]:
        """POST to the WebAPI. Returns parsed JSON dict or ``False`` on failure."""
        params_array = dict(params_array)
        params_array["code"] = self._activationCode

        command = params_array.get("command")
        if command == "encrypt":
            params_array["unicode"] = 1 if self.useUnicode else 0
            params_array["lang_locale"] = str(self.langLocaleEncoding)
            params_array["ansi_encoding"] = str(self.ansiEncoding)
            params_array["local"] = 1 if self.declareAsLocalVariable else 0
            params_array["new_lines"] = str(self.newLinesEncoding)
            params_array["cmd_min"] = self.minEncryptionCommands
            params_array["cmd_max"] = self.maxEncryptionCommands
            params_array["lang"] = str(self.outputProgrammingLanguage)

            params_array["include_tags"] = 1 if self.includeTags else 0
            params_array["include_example"] = 1 if self.includeExample else 0
            params_array["return_template"] = 1 if self.returnTemplate else 0
            params_array["include_debug_comments"] = 1 if self.includeDebugComments else 0

            if self.encryptionTemplate is not None:
                params_array["template"] = self.encryptionTemplate

            if self.highlight not in (False, None, ""):
                params_array["highlight"] = str(self.highlight)

            if self.enableCompression:
                params_array["compression"] = "1"
                if "string" in params_array and params_array["string"]:
                    compressed_data = zlib.compress(
                        str(params_array["string"]).encode("utf-8"), 9
                    )
                    params_array["string"] = base64.b64encode(compressed_data).decode("ascii")
                elif "bytes" in params_array and params_array["bytes"]:
                    compressed_data = zlib.compress(bytes(params_array["bytes"]), 9)
                    params_array["bytes"] = base64.b64encode(compressed_data).decode("ascii")

        try:
            response = self._session.post(
                self.API_URL, data=params_array, timeout=self._timeout
            )
        except requests.RequestException:
            return False

        if response is None or not response.ok:
            return False

        try:
            result: Dict[str, Any] = response.json()
        except (json.JSONDecodeError, ValueError):
            return False

        if (
            "source" in result
            and self.enableCompression
            and command == "encrypt"
            and int(result.get("error", -1)) == int(self.ErrorCodes.ERROR_SUCCESS)
        ):
            try:
                result["source"] = zlib.decompress(
                    base64.b64decode(result["source"])
                ).decode("utf-8")
            except (zlib.error, TypeError, ValueError):
                return False

        if "error" in result:
            result["error_string"] = self._error_code_to_string(result["error"])

        return result
