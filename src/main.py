# main.py
import argparse, os, glob
import numpy as np
from PIL import Image

import utils as ul
from lambertian import LambertianVectorized
    

def read_image_to_numpy(file) -> np.ndarray:
    greyscale = Image.open(file).convert("L")
    return np.array(greyscale)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images_folder", "-i", required=True)
    parser.add_argument("--light_directions", "-l", required=True)
    parser.add_argument("--outprefix", "-o", required=True)

    args = parser.parse_args()

    # load images from folder to matrix representation
    im_files = sorted(glob.glob(os.path.join(args.images_folder, "*.png"))) # likely a better way to load files
    
    im_matrices = map(read_image_to_numpy, im_files)
    first_image = next(im_matrices)
    
    im_maxrow, im_maxcol = first_image.shape
    images_matrix = np.zeros([im_maxrow, im_maxcol, len(im_files)])
    images_matrix[:, :, 0] = first_image

    for k, im in enumerate(im_matrices, start=1):
        images_matrix[:, :, k] = im

    # load light directions matrix directly from file
    lights_matrix = np.loadtxt(args.light_directions, delimiter=",")

    if ul.check_arguments(images_matrix, lights_matrix):
        estimates = LambertianVectorized(images_matrix, lights_matrix).least_squares()
        estimates.decompose()
        
        mat = ul.reshape_normals(estimates, as_colors=True)
        ul.save_as_npy(mat, args.outprefix)

if __name__ == "__main__":
    main()
