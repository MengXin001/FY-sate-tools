"""Preprocess for the GF-4 Imager"""

import rasterio
import numpy as np
from osgeo import gdal

def linear(data):
    data_min, data_max = data.min(), data.max()
    data = (data - data_min) / (data_max - data_min) * 255
    data = np.clip(data, 0, 255)
    return np.uint8(data)

def ortho(input, output, dstSRS="EPSG:4326", dem=None):
    if dem is None:
        print("Ortho without DEM")
        wo = gdal.WarpOptions(srcNodata=0, dstNodata=0, dstSRS=dstSRS, resampleAlg="bilinear", 
                        format="Gtiff",rpc=True, warpOptions=["INIT_DEST=NO_DATA", "INSERT_CENTER_LONG=FALSE"])
    else:
        wo = gdal.WarpOptions(srcNodata=0, dstNodata=0, dstSRS=dstSRS, resampleAlg="bilinear", 
                            format="Gtiff",rpc=True, warpOptions=["INIT_DEST=NO_DATA", "INSERT_CENTER_LONG=FALSE"], 
                            transformerOptions=["RPC_DEM=%s"%(dem), "RPC_DEMINTERPOLATION=bilinear"])   
    wr = gdal.Warp(output, input, options=wo)
    del wr

class GFProcess(object):
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.ortho(self.input, self.output)
        self.gain = ""
        self.bias = ""
        with rasterio.open(output) as src:
            data = [src.read(band) for band in range(1, src.count + 1)]
            self.calibrated_data = [(band * gain) + bias for band in data]
            self.stretch_data =  linear(calibrated_data)

    def save_datasets(self):
        with rasterio.open(self.output, "w", driver="GTiff", 
                        width=self.stretch_data[0].shape[1], 
                        height=self.stretch_data[0].shape[0], 
                        count=len(self.stretch_data), 
                        dtype=self.stretch_data[0].dtype) as dst:
            for i, band_data in enumerate(self.stretch_data, 1):
                dst.write(band_data, i)

if __name__ == "__main__":
    input = ""
    output = ""
    io = GFProcess(input, output)
