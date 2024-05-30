import numpy as np
import xarray as xr

def PolarizationCorrectedTemperature(V_p, H_p, fractions=(1.7, 0.7)):
    res = V_p * fractions[0] - H_p * fractions[1]
    return res

def RGBCompositor(R: np.ndarray, G: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Create an RGB composite"""
    if not (R.shape == G.shape == B.shape):
        raise ValueError("Data shape Error")
    
    dims = ("y", "x", "bands")
    data = np.stack([R, G, B], axis=-1)
    coords = {
        "bands": ["red", "green", "blue"]
    }
    attrs = {
        "mode": "RGB",
        "sensor": "MWRI"
    }
    
    return xr.DataArray(data=data, dims=dims, coords=coords, attrs=attrs)
