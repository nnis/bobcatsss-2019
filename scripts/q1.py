import os.path as path

import numpy as np
import matplotlib.pyplot as plt


def barplot_info(bins):
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    return width, center

#####
# Distribution of employee count in museums


def do(res, small, txt, img, formats, rfb, rfb_sm, nipos):

    nipos_hist, nipos_bins = np.histogram(nipos['size'], bins=3)
    res_hist, res_bins = np.histogram(res['size'], bins=3)

    ftxt = path.join(txt, 'chart.txt')
    with open(ftxt, 'w') as f:
        print("Distribution of employee count in museums", file=f)
        print("-----------------------------------------", file=f)
        print("NIPOS", file=f)
        print("-----", file=f)
        print(
            "small (1-10)    : %d (%d%%)" % (nipos_hist[0], nipos_hist[0] /
                                             (len(nipos) / 100)),
            file=f)
        print(
            "medium (11-25): %d (%d%%)" % (nipos_hist[1], nipos_hist[1] /
                                           (len(nipos) / 100)),
            file=f)
        print(
            "large (26+)    : %d (%d%%)" % (nipos_hist[2], nipos_hist[2] /
                                            (len(nipos) / 100)),
            file=f)
        print("", file=f)
        print("Sample", file=f)
        print("------", file=f)
        print(
            "small (1-10)    : %d (%d%%)" % (res_hist[0],
                                             res_hist[0] / (len(res) / 100)),
            file=f)
        print(
            "medium (11-25): %d (%d%%)" % (res_hist[1],
                                           res_hist[1] / (len(res) / 100)),
            file=f)
        print(
            "large (26+)    : %d (%d%%)" % (res_hist[2],
                                            res_hist[2] / (len(res) / 100)),
            file=f)
        print("", file=f)

    width, center = barplot_info(nipos_bins)

    fig = plt.figure()
    plt.title('Distribution of employee count in museums')
    plt.xlabel("Number of employees")
    plt.xlim(0, 2)
    plt.ylabel("Number of museums")
    plt.ylim(0, 350)
    plt.yticks(range(0, 350, 25))
    plt.xticks(center,
               ["1 - 10 (small)", "11 - 25 (medium)", "26 and more (large)"])
    nip_rects = plt.bar(
        center,
        nipos_hist,
        align='center',
        width=width,
        color='lightblue',
        label="NIPOS")
    vz_rects = plt.bar(
        center,
        res_hist,
        align='center',
        width=width,
        color='darkblue',
        label="Sample")
    plt.legend(loc='upper right', frameon=False)

    # Nipos
    nip_labels = [
        '{0:.1f}%'.format(i / (sum(nipos_hist) / 100)).rstrip('0').rstrip('.')
        for i in nipos_hist
    ]
    for r, l in zip(nip_rects, nip_labels):
        height = r.get_height() / 2
        plt.text(
            r.get_x() + r.get_width() / 2,
            height + 5,
            l,
            ha='center',
            va='bottom')
    # Vzorek
    vz_labels = [
        '{0:.1f}%'.format(i / (sum(res_hist) / 100)).rstrip('0').rstrip('.')
        for i in res_hist
    ]
    for r, l in zip(vz_rects, vz_labels):
        height = r.get_height() / 2
        plt.text(
            r.get_x() + r.get_width() / 2,
            height + 5,
            l,
            ha='center',
            va='top',
            color='whitesmoke')

    for fm in formats:
        fimg = path.join(img, 'chart1.' + fm)
        fig.savefig(fimg)
    plt.close(fig)
