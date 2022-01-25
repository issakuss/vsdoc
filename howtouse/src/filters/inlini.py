import re
from configparser import ConfigParser
from pathlib import Path

import pandas as pd
from pandocfilters import toJSONFilter, Str


dire = Path(__file__).resolve().parent
pattern = re.compile('%\{(.*)\}')
parser_posit = ConfigParser()
parser_posit.read(dire / 'iniposit.ini')

posits = dict(parser_posit.items('posit'))
parsers = dict()
for key, posit in posits.items():
    if posit.endswith('.ini'):
        parser = ConfigParser()
        parser.read(posit)
        parsers[key] = parser
    if posit.endswith('.csv'):
        parsers[key] = pd.read_csv(posit, header=None)


def _alpha2num(alpha):
    num=0
    for index, item in enumerate(list(alpha)):
        num += pow(26,len(alpha)-index-1)*(ord(item)-ord('A')+1)
    return num


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

    loaded = parsers[field[0]]
    if isinstance(loaded, pd.DataFrame):
        var = loaded.iloc[int(field[2]) - 1, _alpha2num(field[1]) - 1]
    else:
        var = dict(loaded.items(field[1]))[field[2]]
    if code:
        var = eval(code)

    return Str(value[:m.span()[0]] + var + value[m.span()[1]:]) 


if __name__ == '__main__':
    toJSONFilter(inline)