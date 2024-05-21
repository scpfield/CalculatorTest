# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: Extensions (experimental)

from __future__ import annotations
import enum
import typing
from dataclasses import dataclass
from .util import event_class, T_JSON_DICT


def load_unpacked(
        path: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,str]:
    '''
    Installs an unpacked extension from the filesystem similar to
    --load-extension CLI flags. Returns extension ID once the extension
    has been installed.

    :param path: Absolute file path.
    :returns: Extension id.
    '''
    params: T_JSON_DICT = dict()
    params['path'] = path
    cmd_dict: T_JSON_DICT = {
        'method': 'Extensions.loadUnpacked',
        'params': params,
    }
    json = yield cmd_dict
    return str(json['id'])
