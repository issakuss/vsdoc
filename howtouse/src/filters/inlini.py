import re
from configparser import ConfigParser
from pathlib import Path

import pandas as pd
from pandocfilters import toJSONFilter, Str


dire = Path(__file__).resolve().parent
pattern = re.compile('%\{(.*?)\}')
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


def int2spell(var):
    spells = ('one', 'two', 'three', 'four', 'five',
              'six', 'seven', 'eight', 'nine', 'ten',
              'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
              'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty')
    return spells[int(var) - 1]


def int2Spell(var):
    return int2spell(var).capitalize()


def inline(key, value, *_):
    def split_args(match):
        splited = match.split('!!')
        if len(splited) > 1:
            match, code = splited
        else:
            code = None
        return re.split('[:.]', match) + [code]

    def extract_from_file(posit, field, key, code):
        loaded = parsers[posit]
        if isinstance(loaded, pd.DataFrame):
            var = loaded.iloc[int(key) - 1, _alpha2num(field) - 1]
        else:
            var = dict(loaded.items(field))[key]
        return eval(code) if code else var

    if key != 'Str':
        return
    matches = re.findall(pattern, value)
    if len(matches) == 0:
        return
    frame = re.sub(pattern, '{}', value)

    argset = [split_args(match) for match in matches]
    embeds = [extract_from_file(*args) for args in argset]
    return Str(frame.format(*embeds))


if __name__ == '__main__':
    if False: # Test code
        values = [
            '%{result:pearson.p1!!pval(var,0.001)})',
            '%{result:pearson.p2!!dround(var,2)})',
            '(%{result:mean.ci_low}--%{result:mean.ci_high}).',
            '%{table:C.3!!pval(var,0.001)}))']
        for value in values:
            inline('Str', value)
    toJSONFilter(inline)