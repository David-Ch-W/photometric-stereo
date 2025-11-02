# utils.py
import numpy as np

def check_arguments(images_matrix, lights_file) -> bool:
    maxrow, maxcol, k = images_matrix.shape
    if k != lights_file.shape[0]:
        raise ValueError(
            f"Matrix dimensions are {(maxrow, maxcol, k)}; "
            f"expected {k} light vectors, saw {lights_file.shape[0]}."
        )
    return True

def reshape_normals(estimate, as_colors=False) -> np.ndarray:
    maxrow, maxcol = estimate.single_channel.shape[:2]
    normals_matrix = estimate.normal.T.reshape(maxrow, maxcol, 3)
    if as_colors:
        # for a pixel, each vector component can be mapped to a value that
        # we can use to show the length of the vector's projection onto the 
        # respective axes (x->red, y->green, z->blue)
        color_matrix = ((normals_matrix + 1.) / 2.) * 255
        return color_matrix.astype(int)
    return normals_matrix

def save_as_npy(matrix, prefix):
    np.save(f"{prefix}.npy", matrix)
