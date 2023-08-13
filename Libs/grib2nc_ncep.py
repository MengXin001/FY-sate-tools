import numpy as np
import netCDF4 as nc
import os
import xarray

#2nc
tdata = xarray.open_dataset('gfs.t00z.pgrb2.0p25.anl', engine='cfgrib',backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 2}})
wdata = xarray.open_dataset('gfs.t00z.pgrb2.0p25.anl', engine='cfgrib',backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround', 'level': 10}})
mdata = xarray.open_dataset('gfs.t00z.pgrb2.0p25.anl', engine='cfgrib',backend_kwargs={'filter_by_keys': {'typeOfLevel': 'meanSea'}})
gfs_upper_grib = xarray.open_dataset('gfs.t00z.pgrb2.0p25.anl', engine='cfgrib',backend_kwargs={'filter_by_keys': {'typeOfLevel': 'isobaricInhPa'}})
gfs_upper_grib.to_netcdf('input_upper_gfs.nc')

#2npy
#surface
surface_data = np.zeros((4, 721, 1440), dtype=np.float32)
surface_data[0] = mdata.mslet.astype(np.float32)
surface_data[1] = wdata.u10.astype(np.float32)
surface_data[2] = wdata.v10.astype(np.float32)
surface_data[3] = tdata.t2m.astype(np.float32)
np.save(os.path.join('input_surface.npy'), surface_data)

#upperair
upper_data = np.zeros((5, 13, 721, 1440), dtype=np.float32)
with nc.Dataset(os.path.join('input_upper_gfs.nc')) as nc_file:
    upper_data[0] = (nc_file.variables['gh'][:]).astype(np.float32)
    upper_data[1] = nc_file.variables['q'][:].astype(np.float32)
    upper_data[2] = nc_file.variables['t'][:].astype(np.float32)
    upper_data[3] = nc_file.variables['u'][:].astype(np.float32)
    upper_data[4] = nc_file.variables['v'][:].astype(np.float32)
np.save(os.path.join('input_upper.npy'), upper_data)
