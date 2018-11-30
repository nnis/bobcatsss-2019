import os
import json

import pandas as pd

import q1, q2


def modern_media(medias):
    count = 0
    for m in medias.split(','):
        if int(m) > 3:
            count += 1
    return count


# Mapovani nipos statistiky na mala, stredni a velka muzea
# podle poctu zamestnancu
# mala: 1 - 10 => 0
# stredni: 11 - 25 => 1
# velka: 26 a vice => 2
def nipos_bucketize(val):
    if val < 11:
        return 0
    if val > 10 and val < 26:
        return 1

    return 2


# Mapovani textove odpovedi na mala, stredni, velka
def res_bucketize(val):
    if val == "1 - 10":
        return 0
    if val == "11 - 25":
        return 1

    return 2


def main():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'src',
        metavar='SRC_DIR',
        type=str,
        nargs='?',
        help='source csv file',
        default=None)
    parser.add_argument(
        '-t',
        '--txt',
        metavar='DIR',
        type=str,
        nargs='?',
        default='results',
        help='output directory for text results')
    parser.add_argument(
        '-i',
        '--img',
        metavar='DIR',
        type=str,
        nargs='?',
        default='figures',
        help='output directory for images')
    parser.add_argument(
        '-f',
        '--formats',
        type=str,
        nargs='*',
        default=['png'],
        help='image file formats')

    args = parser.parse_args()

    os.makedirs(args.txt, exist_ok=True)
    os.makedirs(args.img, exist_ok=True)

    res = pd.read_csv(os.path.join(args.src, 'final.csv'))
    res["modernMediaCount"] = res['1'].map(modern_media)
    res['size'] = res['9'].map(res_bucketize)
    res.drop('9', axis=1, inplace=True)  # dale uz textovou verzi nepotrebujeme
    # mala muzea
    small = res[res['size'] == 0]

    # Muzea, která prodělala změnu za posledních deset let
    rfb = res[res['12'] > 2005]
    # A z toho jsou mala
    rfb_sm = rfb[rfb['size'] == 0]

    # Nipos data
    nipos = pd.read_csv(os.path.join(args.src, 'velikosti.csv'),
                        dtype={'f0301_2': int})
    nipos['size'] = nipos['f0301_2'].map(nipos_bucketize)

    # Seznam forem
    with open(os.path.join(args.src, 'formy.json')) as formy_json:
        form_names = list(json.load(formy_json).values())

    # Rozlozeni muzei dle velikosti
    q1.do(res, small, args.txt, args.img, args.formats, rfb, rfb_sm, nipos)

    # Komunikacni typy (otazka 1 a 4 dohromady)
    q2.do(res, small, args.txt, args.img, args.formats, rfb, rfb_sm)


if __name__ == '__main__':
    main()
