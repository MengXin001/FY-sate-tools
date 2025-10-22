import os
import glob
import h5py
import numpy as np
import xarray as xr
from datetime import datetime
from utils import *

MWHS_DATASETS = {
    "MWHS2": ["bt_89h", "bt_118_0.08v", "bt_118_0.2v", "bt_118_0.3v", "bt_118_0.8v", "bt_118_1.1v", "bt_118_2.5v", "bt_118_3.0v", "bt_118_5.0v", "bt_166h", "bt_183_1.0v", "bt_183_1.8v", "bt_183_3.0v", "bt_183_4.5v", "bt_183_7.0v"],
    "MWHSX": ["bt_89v", "bt_118_0.08v", "bt_118_0.2v", "bt_118_0.3v", "bt_118_0.8v", "bt_118_1.1v", "bt_118_2.5v", "bt_118_3.0v", "bt_118_5.0v", "bt_150v", "bt_183_1.0v", "bt_183_1.8v", "bt_183_3.0v", "bt_183_4.5v", "bt_183_7.0v"]
}
SENSOR_NAMES = ["Advanced Microwave Humidity Sounder", "MicroWave Humidity Sounder-II"]


class MWHSReader():
    def __init__(self, fname, dataset="bt_89v"):
        self.file = h5py.File(fname, "r")
        try:
            self.attrs = {k: autodecode(v) for k, v in self.file.attrs.items()}
            if self.attrs["Sensor Name"] in SENSOR_NAMES:
                if self.attrs["Sensor Name"] == "MicroWave Humidity Sounder-II":
                    self.available_datasets = MWHS_DATASETS["MWHS2"]
                elif self.attrs["Sensor Name"] == "Advanced Microwave Humidity Sounder":
                    self.available_datasets = MWHS_DATASETS["MWHSX"]
                else:
                    raise Exception(f"Not currently supported sensor: {self.attrs['Sensor Name']}")
                if dataset not in self.available_datasets:
                    raise Exception(f"Not found dataset {dataset} in {self.available_datasets}")
                self._MWHS2_reader(dataset)
            else:
                raise Exception(f"Unable to decode data:\n{fname}")
        except Exception as e:
            raise e

    def _MWHS2_reader(self, dataset):
        datasets = self.file
        flag = "Earth_Obs_BT"
        index = self.available_datasets.index(dataset)
        lons, lats = datasets["Geolocation"]["Longitude"][:], datasets["Geolocation"]["Latitude"][:]
        EOB = datasets["Data"][flag]

        dims = ["y", "x"]
        coords = {
            "lon": (dims, lons),
            "lat": (dims, lats)
        }
        attrs = {
            "satellite": self.attrs["Satellite Name"],
            "sensor": self.attrs["Sensor Name"],
            "center_frequency": self.attrs["Chs_Center_Frequency"].split(',')[index],
            "description": "Earth Observation Brightness Temperature"
        }
        data = xr.DataArray(
            data=EOB[index],
            dims=dims,
            coords=coords,
            attrs=attrs,
            name="brightness_temperature"
        )
        '''
        data = dict()
        data["satellite"] = self.attrs["Satellite Name"]
        data["sensor"] = self.attrs["Sensor Name"]
        data["center_frequency"] = self.attrs["Chs_Center_Frequency"].split(',')[index]
        data["lons"], data["lats"] = lons, lats
        data["dataset"] = EOB[index]
        '''
        self.data = data

    @property
    def all_available_datasets(self):
        return self.available_datasets

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
    fname = "FY3F_MWHS-_ORBD_L1_20251022_0036_015KM_V0.HDF"
    io = MWHSReader(fname, dataset="bt_89h")
    print(io.data)
