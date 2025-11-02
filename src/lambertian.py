import numpy as np

class LambertianVectorized:

    def __init__(self, single_channel: np.ndarray, direction_matrix: np.ndarray):
        self.single_channel = single_channel
        self.L = direction_matrix
        self._reflectances = None
        self._normals = None
        self._albedos = None

    def least_squares(self):
        L = self.L
        U = self.single_channel.reshape(-1, L.shape[0])
        self._reflectances = np.linalg.pinv(L) @ U.T
        return self
                
    def decompose(self):
        if self._reflectances is None:
            return
        eps = np.finfo(np.float64).eps
        albedos = np.linalg.norm(self._reflectances, axis=0)
        self._normals = self._reflectances / (albedos + eps)
        self._albedos = albedos

    @property
    def normal(self):
        if self._normals is None:
            raise ValueError
        return self._normals
    
    @property
    def albedo(self):
        if self._albedos is None:
            raise ValueError
        return self._albedos
