"""Test Reader for the FY-3G PMR L2"""

import os
import glob
import h5py
import numpy as np
from datetime import datetime

def autodecode(string, encoding="gbk"):
    return string.decode(encoding) if isinstance(string, bytes) else string

class PMRReader(object):
    """The base class reading FY-3G PMR L2 data.

    Args:
        fname: PMR data path.
        datafield: Scientific datasets field.
        dataset: Scientific dataset.
        level: The first(0) and second(1) dimensions respectively store the geolocation on the ground and at level of 18km above ground.
    """

    def __init__(self, fname, datafield="SLV", dataset="zFactorCorrectedESurface", level=1):
        self.file = h5py.File(fname, "r")
        self.attrs = {k, autodecode(v) for k, v in self.file.attrs.items()}
        self.datafield = datafield
        self.dataset = dataset
        self.level = level
        try:
            if self.attrs["Satellite Name"] == "FY-3G":
                self._reader()
            else:
                raise Exception(f"Unable to decode data:\n{fname}")
        except Exception as e:
            raise e

    def _reader(self):
        lons, lats = self.file["Geo_Fields"]["Longitude"][:], self.file["Geo_Fields"]["Latitude"][:]
        lons[lons==-9999.9] = np.nan
        lats[lats==-9999.9] = np.nan
        dataset = self.file[self.datafield][self.dataset]
        data = dict()
        data["lons"] = lons[:,:,self.level]
        data["lats"] = lats[:,:,self.level]
        data["dataset"] = dataset
        self.data = data

    def all_available_datasets(self, datafield="SLV"):
        return list(self.file[datafield].keys())

    def all_available_datafields(self):
        return list(self.file.keys())

    @property
    def start_time(self):
        start_time = self.attrs["Observing Beginning Date"] + "T" + self.attrs["Observing Beginning Time"] + "Z"
        try:
            return datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            return datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")

    @property
    def end_time(self):
        end_time = self.attrs["Observing Ending Date"] + "T" + self.attrs["Observing Ending Time"] + "Z"
        try:
            return datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            return datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")

if __name__ == "__main__":
    fname = "C:/Users/Administrator/Desktop/FY3G_PMR--_ORBA_L2_KuR_MLT_NUL_20240528_0026_5000M_V0.HDF"
    io = PMRReader(fname, datafield="SLV", dataset="zFactorCorrectedESurface")
    print(io.all_available_datasets())