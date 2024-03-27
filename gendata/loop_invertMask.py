# STEP 4: Capture foreground and keep white background, save images(.jpg) and masks(.pbm) into same category folder for Cut-Paste-Learn

import glob
import os
import re
import numpy as np
from PIL import Image
from data_utils import invertmask

datadir = "/root/database/objects_downsize"
destdir = "/root/database/objects_bk"

source_list = sorted(glob.glob(os.path.join(datadir, '*')))

for _, source_dir in enumerate(source_list):
    object_name = source_dir.split('/')[-1]
    target_dir = os.path.join(destdir, object_name)
    image_paths = sorted([p for p in glob.glob(os.path.join(source_dir, 'images', '*'))
                          if re.search('/*\.(jpg|jpeg|png|gif|bmp|pbm)', str(p))])
    mask_paths = sorted([p for p in glob.glob(os.path.join(source_dir, 'masks', '*'))
                         if re.search('/*\.(jpg|jpeg|png|gif|bmp|pbm)', str(p))])

    os.makedirs(target_dir, exist_ok=True)
    # os.makedirs(os.path.join(target_dir, 'images'), exist_ok=True)
    # os.makedirs(os.path.join(target_dir, 'masks'), exist_ok=True)

    for _, file_path in enumerate(zip(image_paths, mask_paths)):
        img = np.array(Image.open(file_path[0]))
        mask = np.array(Image.open(file_path[1]))
        base_filename = os.path.splitext(os.path.basename(file_path[0]))[0]

        new_img, new_mask = invertmask(img, mask)
        new_img = Image.fromarray(new_img.astype(np.uint8), mode="RGB")
        new_mask = Image.fromarray(new_mask.astype(np.uint8))

        # new_img.save(os.path.join(target_dir, 'images', base_filename + '.png'))
        # new_mask.save(os.path.join(target_dir, 'masks', base_filename + '.png'))
        
        new_img.save(os.path.join(target_dir, base_filename + '.jpg'))
        new_mask.save(os.path.join(target_dir, base_filename + '.pbm'))

    print('Invert Mask: ' + object_name + ' Done!')
