import os.path as path

import matplotlib.pyplot as plt

#####
# Communication types

haptic_forms = [4, 10, 11, 14]
haptic_activities = [2, 4]

intellect_forms = [1, 2, 6, 7, 8, 14]
intellect_activities = [1, 3]

visual_forms = [1, 5, 6, 7, 10, 13]
visual_activities = [3]

auditive_forms = [3, 4, 5]
auditive_activities = [1]


def categorize(df):
    cats = {k: 0 for k in ['h', 'i', 'v', 'a']}

    # count forms
    for d in df['1'].dropna():
        for i in d.split(','):
            i = i.strip()
            if not i.isdigit():
                continue
            i = int(i)
            if i in haptic_forms:
                cats['h'] += 1
            if i in intellect_forms:
                cats['i'] += 1
            if i in visual_forms:
                cats['v'] += 1
            if i in auditive_forms:
                cats['a'] += 1

    # count activities
    for d in df['4'].dropna():
        for i in d.split(','):
            i = i.strip()
            if not i.isdigit():
                continue
            i = int(i)
            if i in haptic_activities:
                cats['h'] += 1
            if i in intellect_activities:
                cats['i'] += 1
            if i in visual_activities:
                cats['v'] += 1
            if i in auditive_activities:
                cats['a'] += 1

    return cats


def pct(v, a):
    return 100 * float(v)/float(a)


def do(res, small, txt, img, formats, rfb, rfb_sm):

    old = res[res['12'] < 2006]

    cats = {
        'all': categorize(res),
        'small':  categorize(small),
        'modern': categorize(rfb),
        'modern_small': categorize(rfb_sm),
        'old': categorize(old)
    }

    # Museums present objects and that is a visual form which is not covered in
    # the questionnaire which we here count in.
    cats['all']['v'] += len(res)
    cats['small']['v'] += len(small)
    cats['modern']['v'] += len(rfb)
    cats['modern_small']['v'] += len(rfb_sm)
    cats['old']['v'] += len(old)

    ftxt = path.join(txt, 'graf9.txt')
    with open(ftxt, 'w') as f:
        print("Komunikacni typy v muzeich", file=f)
        print("--------------------------", file=f)
        print("", file=f)
        for k, c in cats.items():
            print(k, file=f)
            print("-----------", file=f)
            for t, v in c.items():
                print("%s : %0.1f%%" % (t, pct(v, sum(c.values()))), file=f)
            print("", file=f)

    labels = [
        'Haptic-social',
        'Intellectual',
        'Visual',
        'Auditive',
    ]

    sizes = cats['all'].values()

    colors = ['gold', 'royalblue', 'orangered', 'forestgreen']
    explode = (0.1, 0.1, 0.1, 0.1)  # explode 1st slice

    fig = plt.figure()
    plt.title(
        'Chart 2: Representation of preferred communication types in museums'
    )
    plt.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=15)
    plt.axis('equal')
    for fm in formats:
        fimg = path.join(img, 'chart2.' + fm)
        fig.savefig(fimg)
    plt.close(fig)
