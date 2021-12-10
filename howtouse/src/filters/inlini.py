import re
from configparser import ConfigParser
from pathlib import Path

from pandocfilters import toJSONFilter, Str


dire = Path(__file__).resolve().parent
pattern = re.compile('%\{(.*)\}')
parser_posit = ConfigParser()
parser_posit.read(dire / 'iniposit.ini')

posits = dict(parser_posit.items('posit'))
parsers = dict()
for key, posit in posits.items():
    parser = ConfigParser()
    parser.read(posit)
    parsers[key] = parser


def pval(var, mini=-float('inf')):
    if float(var) < mini:
        return '< .001'
    else:
        return '= ' + var[1:]

def dround(var, d):
    return str(round(float(var), 2))


def inline(key, value, *_):
    if key != 'Str':
        return
    m = pattern.match(value)
    if m is None:
        return

    field = re.split('!!', m.group(1))
    if len(field) == 2:
        field, code = field
    else:
        field = field[0]
        code = None
    field = re.split('[:.]', field)

    if len(field) != 3:
        return

    var = dict(parsers[field[0]].items(field[1]))[field[2]]
    if code:
        var = eval(code)

    return Str(value[:m.span()[0]] + var + value[m.span()[1]:]) 


if __name__ == '__main__':
    toJSONFilter(inline)
    if False: # Test code
        replaced = inline('Str', '%{method:stats.test!!pval(var)}', None, None)