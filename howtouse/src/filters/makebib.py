import string
from pathlib import Path

import numpy as np
from unidecode import unidecode
from pyzotero.zotero import Zotero
from pandocfilters import toJSONFilter


LIBRARY_ID ='6416427'
LIBRARY_TYPE = 'user'
API_KEY = 'RhqIy8pwvm6pDXChBinh3asN'
COLLECTION_ID = 'WE5Z3DSW'
SAVE_PATH = Path('src/citation.bib')


def extract_year(date: str) -> str:
    date = date.replace(' ', '@').replace('-', '@').replace('/', '@')
    date = date.split('@')
    for d in date:
        if len(d) == 4 and d.isdigit():
            return d
    return ''


def make_citekey(lastname, title, year):
    def convert_lastname(lastname):
        return unidecode(lastname).lower().replace(' ', '')

    def make_shorttitle(title):
        # from [extensions.zotero.translators.better-bibtex.skipWords], zotero.
        skipwords = ('a', 'ab', 'aboard', 'about', 'above', 'across', 'after',
                     'against', 'al', 'along', 'amid', 'among', 'an', 'and',
                     'anti', 'around', 'as', 'at', 'before', 'behind', 'below',
                     'beneath', 'beside', 'besides', 'between', 'beyond',
                     'but', 'by', 'd', 'da', 'das', 'de', 'del', 'dell',
                     'dello', 'dei', 'degli', 'della', 'dell', 'delle', 'dem',
                     'den', 'der', 'des', 'despite', 'die', 'do', 'down', 'du',
                     'during', 'ein', 'eine', 'einem', 'einen', 'einer',
                     'eines', 'el', 'en', 'et', 'except', 'for', 'from', 'gli',
                     'i', 'il', 'in', 'inside', 'into', 'is', 'l', 'la', 'las',
                     'le', 'les', 'like', 'lo', 'los', 'near', 'nor', 'of',
                     'off', 'on', 'onto', 'or', 'over', 'past', 'per', 'plus',
                     'round', 'save', 'since', 'so', 'some', 'sur', 'than',
                     'the', 'through', 'to', 'toward', 'towards', 'un', 'una',
                     'unas', 'under', 'underneath', 'une', 'unlike', 'uno',
                     'unos', 'until', 'up', 'upon', 'versus', 'via', 'von',
                     'while', 'with', 'within', 'without', 'yet', 'zu', 'zum')

        def up(str_):
            if len(str_) < 2:
                return str_.upper()
            if str_[0] == ' ':
                return ' ' + str_[1].upper() + str_[2:]
            return str_[0].upper() + str_[1:]
        
        def strip(title):
            for key in ['/', '‐', '—']: # hyphen and dash, not minus (-).
                title = title.replace(key, ' ')
            title = ' ' + unidecode(title) + ' '
            for key in ['\'s', '\'t', '\'S', '\'T']:
                title = title.replace(key, '')
            title = title.translate(str.maketrans('', '', string.punctuation))
            for key in skipwords:
                key = ' ' + key + ' '
                title = title.replace(key, ' ')
                title = title.replace(key.upper(), ' ').replace(up(key), ' ')
            return title

        while True:
            len_before = len(title.replace(' ', ''))
            title = strip(title)
            if len_before == len(title.replace(' ', '')):
                break

        title = [up(t) for t in title.split(' ') if t]
        if len(title) < 3:
            return ''.join(title)
        return ''.join(title[:3])

    return convert_lastname(lastname) + make_shorttitle(title) + str(year)


def zoteroitem2bbtcitekey(item):
    authors = item['data']['creators'] if 'creators' in item['data'] else None
    lastname = authors[0]['lastName'] if authors else ''
    year = extract_year(item['data']['date'])
    return make_citekey(lastname, item['data']['title'], year)


def search_zotero(to_search):
    zotero = Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    if COLLECTION_ID:
        items = zotero.everything(
            zotero.collection_items(COLLECTION_ID,
                                    itemType='journalArticle || book'))
    else:
        items = zotero.everything(
            zotero.items(itemType='journalArticle || book'))

    citekeys = [zoteroitem2bbtcitekey(item) for item in items]
    are_to_search = np.array(citekeys) == to_search
    if not are_to_search.any():
        return None
    return items[np.where(are_to_search)[0][0]]


def make_bib(citekeys: list):
    def eachkey(item, citekey):
        bib = [f'@article{{{citekey},']
        if item['data']['title']:
            title = item['data']['title']
            bib.append(f'  title = {{{title}}},')

        if item['data']['creators']:
            names = [f'{author["lastName"]}, {author["firstName"]}'
                     for author in item['data']['creators']]
            bib.append(f'  author = {{{" and ".join(names)}}},')

        if item['data']['date']:
            year = extract_year(item['data']['date'])
            bib.append(f'  year = {{{year}}},')

        if item['data']['volume']:
            volume = item['data']['volume']
            bib.append(f'  volume = {{{volume}}},')

        if item['data']['pages']:
            pages = '--'.join(item['data']['pages'].split('-'))
            bib.append(f'  pages = {{{pages}}},')
            pass

        if item['data']['DOI']:
            doi = item['data']['DOI']
            bib.append(f'  doi = {{{doi}}},')            

        if item['data']['publicationTitle']:
            journal = item['data']['publicationTitle']
            bib.append(f'  journal = {{{journal}}},')
        
        bib = '\n'.join(bib)[:-1] + '\n}\n\n'
        SAVE_PATH.touch()
        with SAVE_PATH.open('a') as f:
            f.write(bib)

    for citekey in citekeys:
        zoteroitem = search_zotero(citekey)
        if zoteroitem is None:
            raise ValueError(f'{citekey} is not found in Zotero DB')
        eachkey(zoteroitem, citekey)


def extract_make_bib(key, value, format_, meta):
    def read_exist_citekeys():
        with SAVE_PATH.open('r') as f:
            lines = f.readlines()
        return [line[9:-2] for line in lines
                if line[0] if line.startswith('@')]

    if key != 'Cite':
        return
    SAVE_PATH.touch()
    exist_citekeys = read_exist_citekeys()
    for value_ in value[0]:
        citekey = value_['citationId']
        if citekey in exist_citekeys:
            continue
        make_bib([citekey]) 
        

def _test_citekey_generation(path_bib):
    zotero = Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    items = zotero.everything(zotero.items(itemType='journalArticle || book'))
    generated_citekeys = np.array([zoteroitem2bbtcitekey(item)
                                   for item in items])
    generated_citekeys.sort()
        
    with open(path_bib) as f:
        lines = f.readlines() 
    fetched_citekeys = np.array([line[9:-2] for line
                                 in lines if line.startswith('@')])
    fetched_citekeys.sort()
    set(generated_citekeys) - set(fetched_citekeys)


if __name__ == '__main__':
    if False: # Test
        _test_citekey_generation('howtouse/bibtex.bib')
    toJSONFilter(extract_make_bib)