import re
from configparser import ConfigParser
from pathlib import Path

from pandocfilters import toJSONFilter, Str


# Input relative paths from the working directory
INI_PATHS = ['method.ini', 'report/result.ini']


def inline(key, value, format_, meta):
    ###
    if value is not None:
        if key=='Cite':
            with open('/mnt/vsdoc/debug.text', 'a') as f:
                f.write(str(value[0]) + '/')
                f.write('#####\n')
    ###

    if key != 'Str':
        return
    m = re.compile('%\{(.*)\}').match(value)
    if m is None:
        return
    field = re.split('[:.]', m.group(1))
    if len(field) != 3:
        return
    var = dict(parsers[field[0]].items(field[1]))[field[2]]
    return Str(value[:m.span()[0]] + var + value[m.span()[1]:]) 


if __name__ == '__main__':
    parsers = dict()
    for path in INI_PATHS:
        parser = ConfigParser()
        parser.read(path)
        parsers[Path(path).stem] = parser

    toJSONFilter(inline)