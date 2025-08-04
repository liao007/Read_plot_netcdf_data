import pandas as pd 
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


#################################################### 
# 读取 NetCDF 格式的气候数据, 以及简单的绘图展示
####################################################

# nc文件路径，示例
nc_file_path = './TEMP/temp_CMFD_V0200_B-01_03hr_010deg_197501.nc'
# domain file, 研究区域文件
domain_file_path = './domain.nc'

# read NetCDF file using xarray 
ds = xr.open_dataset(nc_file_path)

# Print dataset information
print(ds)

# Extract latitude and longitude, 数据的坐标
lats = ds['lat'].values
lons = ds['lon'].values


domain = xr.open_dataset(domain_file_path)
mask = domain['mask']

# 研究区域的经纬度坐标
mask_lat = domain['lat'].values
mask_lon = domain['lon'].values

# Extract variable data (temp)
variable_temp = ds['temp']
print("Variable 'temp' data shape:", variable_temp.shape)

# 对数据变量进行时间维度的平均，并进行空间分布展示
variable_temp.mean(dim='time').plot(cmap='coolwarm')
plt.show()

# 对数据变量进行空间范围的平均，并进行时间动态展示
variable_temp.mean(dim=['lat', 'lon']).plot()
plt.show()

# 掩膜所在的研究区域
# Interpolate spatially to VIC grid, 空间插值，以达到相同的坐标
ds_interp = ds.interp(lat=mask_lat, lon=mask_lon, method='linear')
variable_temp_interp = ds_interp['temp']
ds_mask = variable_temp_interp.where(mask)

# 对数据变量进行时间维度的平均，并进行空间分布展示
variable_temp_interp.mean(dim='time').plot(cmap='coolwarm')
plt.title('Temperature in the domain region')
plt.show()

# 对数据变量进行空间范围的平均，并进行时间动态展示
variable_temp_interp.mean(dim=['lat', 'lon']).plot()
plt.title('Temperature dynamics in the domain region')
plt.show()


