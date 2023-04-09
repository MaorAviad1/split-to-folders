import os
import struct

# path to the folder with 10000 images
folder_path = 'C:\\split-to-folder'

# list all the images in the folder
images = os.listdir(folder_path)

def get_image_size(file_path):
    width, height = 0, 0  # default values
    with open(file_path, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return width, height
        if file_path.endswith('.png'):
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return width, height
            width, height = struct.unpack('>ii', head[16:24])
        elif file_path.endswith('.gif'):
            width, height = struct.unpack('<HH', head[6:10])
        elif file_path.endswith('.jpeg'):
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return width, height
        else:
            return width, height
    return width, height

# loop through all the images
for image in images:
    # get the first 10 letters of the file
    first_ten_letters = image[:10]
    # get the width and height of the image
    width, height = get_image_size(f'{folder_path}/{image}')
    if width == 0 and height == 0:
        continue
    # create the sub-folder name
    sub_folder = f'{first_ten_letters}-{width}x{height}'
    # create the sub-folder if it doesn't exist
    if not os.path.exists(f'{folder_path}/{sub_folder}'):
        os.makedirs(f'{folder_path}/{sub_folder}')
    # move the image to the sub-folder
    os.rename(f'{folder_path}/{image}', f'{folder_path}/{sub_folder}/{image}')

