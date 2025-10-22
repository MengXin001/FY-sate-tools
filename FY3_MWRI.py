"""Test Reader for the FY-3 MWRI L1"""

import os
import glob
import h5py
import numpy as np
from datetime import datetime
from utils import *

MWRI_DATASETS = {
    "S1": ["bt_10v", "bt_10h", "bt_18v", "bt_18h", "bt_23v", "bt_23h", "bt_36v", "bt_36h", "bt_89v", "bt_89h"],
    "S2": ["bt_50v", "bt_50h", "bt_52v", "bt_52h", "bt_53.24v", "bt_53.24h", "bt_53.75v", "bt_53.75h", "bt_118v", "bt_165v", "bt_183v"]
}


def cal_bt(dataset, intercept, slope):
    dataset = dataset * slope + intercept
    return dataset


class MWRIReader(object):

    def __init__(self, fname, dataset="bt_89v"):
        self.file = h5py.File(fname, "r")
        try:
            self.attrs = {k: autodecode(v) for k, v in self.file.attrs.items()}
            if self.attrs["Satellite Name"] == "FY-3D":
                self.available_datasets = MWRI_DATASETS["S1"]
                self._3D_reader(dataset)
            elif self.attrs["Satellite Name"] == "FY-3G":
                self.available_datasets = MWRI_DATASETS["S1"] + MWRI_DATASETS["S2"]
                self._3G_reader(dataset)
            elif self.attrs["Satellite Name"] == "FY-3F":
                self.available_datasets = MWRI_DATASETS["S1"] + MWRI_DATASETS["S2"]
                self._3F_reader(dataset)
            else:
                raise Exception(f"Unable to decode data:\n{fname}")
        except Exception as e:
            raise e

    def _3D_reader(self, dataset):
        datasets = self.file
        flag = "EARTH_OBSERVE_BT_10_to_89GHz"
        index = MWRI_DATASETS["S1"].index(dataset)
        lons, lats = datasets["Geolocation"]["Longitude"][:], datasets["Geolocation"]["Latitude"][:]
        EOB = datasets["Calibration"][flag]
        self.intercept = EOB.attrs["Intercept"]
        self.slope = EOB.attrs["Slope"]
        data = dict()
        data["lons"], data["lats"] = lons, lats
        data["dataset"] = cal_bt(EOB[index], self.intercept, self.slope)
        self.data = data

    def _3G_reader(self, dataset):
        try:
            if dataset in MWRI_DATASETS["S1"]:
                flag = "EARTH_OBSERVE_BT_10_to_89GHz"
                index = MWRI_DATASETS["S1"].index(dataset)
                datasets = self.file["S1"]
            elif dataset in MWRI_DATASETS["S2"]:
                flag = "EARTH_OBSERVE_BT_50_to_183GHz"
                index = MWRI_DATASETS["S2"].index(dataset)
                datasets = self.file["S2"]
            else:
                raise Exception(f"Unavailable dataset: {dataset}")
        except Exception as e:
            raise e
        EOB = datasets["Data"][flag]
        self.intercept = EOB.attrs["Intercept"]
        self.slope = EOB.attrs["Slope"]
        lons, lats = datasets["Geolocation"]["Longitude"][:], datasets["Geolocation"]["Latitude"][:]
        data = dict()
        data["lons"], data["lats"] = lons, lats
        data["datasets"] = cal_bt(EOB[:, :, index], self.intercept, self.slope)
        self.data = data

    def _3F_reader(self, dataset):
        try:
            if dataset in MWRI_DATASETS["S1"]:
                index = MWRI_DATASETS["S1"].index(dataset)
                datasets = self.file["Window Channel"]
            elif dataset in MWRI_DATASETS["S2"]:
                index = MWRI_DATASETS["S2"].index(dataset)
                datasets = self.file["Sounding Channel"]
            else:
                raise Exception(f"Unavailable dataset: {dataset}")
        except Exception as e:
            raise e
        EOB = datasets["Calibration"]["EARTH_OBSERVE_BT"]
        self.intercept = EOB.attrs["Intercept"]
        self.slope = EOB.attrs["Slope"]
        lons, lats = datasets["Geolocation"]["Longitude"][:], datasets["Geolocation"]["Latitude"][:]
        data = dict()
        data["lons"], data["lats"] = lons, lats
        data["datasets"] = cal_bt(EOB[:, :, index], self.intercept, self.slope)
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
    fname = "C:/Users/Administrator/Desktop/FY3D_MWRIA_GBAL_L1_20210504_0514_010KM_MS.HDF"
    io = MWRIReader(fname, dataset="bt_36v")
