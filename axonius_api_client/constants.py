# -*- coding: utf-8 -*-
"""Constants."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import os
import sys

from . import __package__ as PACKAGE_ROOT

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

PY36 = sys.version_info[0:2] >= (3, 6)
""":obj:`bool`: python version is 3.6 or higher"""

PY37 = sys.version_info[0:2] >= (3, 7)
""":obj:`bool`: python version is 3.7 or higher"""

COMPLEX = (dict, list, tuple)
""":obj:`tuple` of :obj:`type`: types that are considered as complex."""

EMPTY = [None, "", [], {}, ()]
""":obj:`list` of :obj:`type`: values that should be considered as empty"""

LIST = (tuple, list)
""":obj:`tuple` of :obj:`type`: types that are considered as lists"""

if PY3:
    STR = (str,)
    INT = (int,)
    TEXT = str
    BYTES = bytes
else:
    STR = (basestring,)  # noqa
    INT = (int, long)  # noqa
    TEXT = unicode  # noqa
    BYTES = str


SIMPLE = tuple(list(STR) + [int, bool, float])
""":obj:`tuple` of :obj:`type`: types that are considered as simple"""

SIMPLE_NONE = tuple(list(SIMPLE) + [None])
""":obj:`tuple` of :obj:`type`: types that are considered as simple or None"""

YES = [True, 1, "1", "true", "t", "yes", "y", "yas"]
""":obj:`list` of :obj:`type`: values that should be considered as truthy"""

NO = [False, 0, "0", "false", "f", "no", "n", "noes"]
""":obj:`list` of :obj:`type`: values that should be considered as falsey"""

MAX_PAGE_SIZE = 2000
""":obj:`int`: maximum page size that REST API allows"""

PAGE_SIZE = MAX_PAGE_SIZE
PAGE_SLEEP = 0
PAGE_CACHE = False

GUI_PAGE_SIZES = [25, 50, 100]
""":obj:`list` of :obj:`int`: valid page sizes for GUI paging"""

LOG_REQUEST_ATTRS_BRIEF = [
    "request to {request.url!r}",
    "method={request.method!r}",
    "size={size}",
]
""":obj:`list` of :obj:`str`: request attributes to log when verbose=False"""

RESPONSE_ATTR_MAP = {
    "url": "{response.url!r}",
    "size": "{response.body_size}",
    "method": "{response.request.method!r}",
    "status": "{response.status_code!r}",
    "reason": "{response.reason!r}",
    "elapsed": "{response.elapsed}",
    "headers": "{response.headers}",
}

REQUEST_ATTR_MAP = {
    "url": "{request.url!r}",
    "size": "{request.body_size}",
    "method": "{request.method!r}",
    "headers": "{request.headers}",
}

TIMEOUT_CONNECT = 5
""":obj:`int`: seconds to wait for connection to API."""

TIMEOUT_RESPONSE = 900
""":obj:`int`: seconds to wait for response from API."""

LOG_FMT_VERBOSE = "%(asctime)s %(levelname)-8s [%(name)s:%(funcName)s()] %(message)s"
LOG_FMT_BRIEF = "%(levelname)-8s [%(name)s] %(message)s"

DEBUG = os.environ.get("AX_DEBUG", "").lower().strip()
DEBUG = any([DEBUG == x for x in YES])

LOG_FMT_CONSOLE = LOG_FMT_VERBOSE if DEBUG else LOG_FMT_BRIEF
""":obj:`str`: default logging format to use for console logs"""

LOG_FMT_FILE = LOG_FMT_VERBOSE
""":obj:`str`: default logging format to use for file logs"""

LOG_DATEFMT_CONSOLE = "%m/%d/%Y %I:%M:%S %p"
""":obj:`str`: default datetime format to use for console logs"""

LOG_DATEFMT_FILE = "%m/%d/%Y %I:%M:%S %p"
""":obj:`str`: default datetime format to use for file logs"""

LOG_LEVEL_CONSOLE = "debug"
""":obj:`str`: default logging level to use for console log handlers"""

LOG_LEVEL_FILE = "debug"
""":obj:`str`: default logging level to use for file log handlers"""

LOG_LEVEL_HTTP = "debug"
""":obj:`str`: default logging level to use for :obj:`axonius_api_client.http.Http`"""

LOG_LEVEL_AUTH = "debug"
""":obj:`str`: default logging level to use for :obj:`axonius_api_client.auth.Mixins`"""

LOG_LEVEL_API = "debug"
""":obj:`str`: default logging level to use for
:obj:`axonius_api_client.api.mixins.Mixins`"""

LOG_LEVEL_PACKAGE = "debug"
""":obj:`str`: default logging level to use for :mod:`axonius_api_client`"""

LOG_LEVELS_STR = ["debug", "info", "warning", "error", "fatal"]
""":obj:`list` of :obj:`str`: valid logging level strs"""

LOG_LEVELS_STR_CSV = ", ".join(LOG_LEVELS_STR)
""":obj:`str`: csv of valid logging level strs"""

LOG_LEVELS_INT = [getattr(logging, x.upper()) for x in LOG_LEVELS_STR]
""":obj:`list` of :obj:`int`: valid logging level ints"""

LOG_LEVELS_INT_CSV = ", ".join([format(x) for x in LOG_LEVELS_INT])
""":obj:`str`: csv of valid logging level ints"""

LOG_FILE_PATH = os.getcwd()
""":obj:`str`: default path to use for log files"""

LOG_FILE_PATH_MODE = 0o700
""":obj:`str`: default permisisons to use when creating directories"""

LOG_FILE_NAME = "{pkg}.log".format(pkg=PACKAGE_ROOT)
""":obj:`str`: default log file name to use"""

LOG_FILE_MAX_MB = 5
""":obj:`int`: default rollover trigger in MB"""

LOG_FILE_MAX_FILES = 5
""":obj:`int`: default max rollovers to keep"""

LOG_NAME_STDERR = "handler_stderr"
""":obj:`str`: default handler name to use for STDERR log"""

LOG_NAME_STDOUT = "handler_stdout"
""":obj:`str`: default handler name to use for STDOUT log"""

LOG_NAME_FILE = "handler_file"
""":obj:`str`: default handler name to use for file log"""

CSV_FIELDS = {
    "device": ["id", "serial", "mac_address", "hostname", "name"],
    "user": ["id", "username", "mail", "name"],
    "sw": ["hostname", "installed_sw_name"],
}
""":obj:`dict`: mapping of csv required columns for csv types"""

SETTING_UNCHANGED = ["unchanged"]
""":obj:`list` of :obj:`str`: ref used by REST API when supplying a password
field that should remain the same as what is already in the database"""

DEFAULT_NODE = "master"
""":obj:`str`: default node name to use"""

CSV_KEYS_META = {
    "file": "file_path",
    "is_users_csv": "is_users",
    "is_installed_sw": "is_installed_sw",
    "id": "user_id",
    "csv_http": "resource_path",
    "csv_share": "resource_path",
    "csv_share_username": "username",
    "csv_share_password": "password",
}
""":obj:`dict`: mapping for csv adapter configuration items"""

CSV_ADAPTER = "csv"
""":obj:`str`: name of csv adapter"""

DEBUG_MATCHES = False
""":obj:`bool`: include log entries regarding match logic"""

DEFAULT_PERM = "ReadOnly"
""":obj:`str`: default user permission to use"""

VALID_PERMS = ["Restricted", "ReadWrite", "ReadOnly"]
""":obj:`list` of :obj:`str`: valid user permissions"""

FIELD_TRIM_LEN = 30000
FIELD_TRIM_STR = "...TRIMMED - {field_len} characters over {trim_len}"
FIELD_JOINER = "\n"
