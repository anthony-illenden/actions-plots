import xarray as xr
import metpy
import datetime as datetime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from metpy.plots import USCOUNTIES

start_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

url = "https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/NDFD/NWS/CONUS/NOAAPORT/Best"
ds = xr.open_dataset(url, engine='netcdf4')
ds = ds.metpy.parse_cf()
ds_latlon = ds.metpy.assign_latitude_longitude()

hi_temp = ds_latlon['Maximum_temperature_height_above_ground_12_Hour_Maximum'].sel(time1=slice(start_date, None), height_above_ground1=2)

for i in range(0, 9):
    datetime = formatted_date = np.datetime_as_string(hi_temp.time1[i].values, unit='D')
    temp_f = (hi_temp[i,:,:] - 273.15) * 9/5 + 32
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([-86, -82, 41, 45])
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(USCOUNTIES.with_scale('5m'), linewidth=0.25)
    plt.contourf(ds_latlon['longitude'], ds_latlon['latitude'], temp_f, cmap='jet', levels=np.arange(30, 111, 1))
    cbar = plt.colorbar(label='Temperature (F)', fraction=0.046, pad=0.04)
    cbar.set_ticks(np.arange(30, 111, 10))
    cbar.set_ticklabels(['30', '40', '50', '60', '70', '80', '90', '100', '110'])
    contour = plt.contour(ds_latlon['longitude'], ds_latlon['latitude'], temp_f, colors='black', levels=np.arange(30, 111, 5))
    plt.clabel(contour, inline=True, fontsize=12, fmt='%1.0f')
    plt.title('NDFD High Temperature for {}'.format(datetime))
    plt.savefig('plots/high/NDFD_High_Temp_{}.png'.format(i), dpi=450, bbox_inches='tight')

