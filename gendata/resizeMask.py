
import argparse
import glob
import os
import sys
from data_utils import resizemask


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', type=str, help='source data path')
    parser.add_argument('--destdir', type=str, help='target data path')
    parser.add_argument('--factors', type=int, help='resize factor for target image')
    parser.add_argument('--resolutions', nargs='+', type=int, help='resolution for target image')
    args = parser.parse_args()

    if len(args.factors) == 0 and len(args.resolutions) == 0:
        print("ERROR: Either 'factors' or 'resolutions' should be given. Aborting.")
        sys.exit()
    else:
        return args


if __name__ == '__main__':
    args = get_args()

    args.datadir = "/root/database/objects_centercrop/079_polaroid_film/masks"
    args.destdir = "/root/database/objects_downsize/079_polaroid_film/masks"
    args.factors = []
    args.resolutions = [256, 256]

    resizemask(args.datadir, args.destdir, args.factors, [args.resolutions])
