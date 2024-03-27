# STEP 3(1): Resize images

import glob
import os
from data_utils import minify

datadir = "/root/database/objects_centercrop"
destdir = "/root/database/objects_downsize"
factors = []
resolutions = [256, 256]

source_list = sorted(glob.glob(os.path.join(datadir, '*')))

for _, source_dir in enumerate(source_list):
    object_name = source_dir.split('/')[-1]
    target_dir = os.path.join(destdir, object_name)

    minify(os.path.join(source_dir, 'images'), os.path.join(target_dir, 'images'),
           factors=factors, resolutions=[resolutions], extend='png')
