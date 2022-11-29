import pandas
import pyproj
import netCDF4 as nc
import numpy as np

BNG = pyproj.Proj(
    "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +towgs84=370,-108,434,0,0,0,0 +units=m +no_defs +type=crs")
WGS84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

rainfall_data = nc.Dataset("rainfall_hadukgrid_uk_1km_ann_202101-202112.nc")
latitude_values = rainfall_data.variables['latitude'][:]
longitude_values = rainfall_data.variables['longitude'][:]


def get_closest_grid_index(lat_pts, lng_pts, longitude, latitude):
    """
    Find the index of the point closest to the given lat/lon
    """

    distances = np.sqrt((lat_pts - latitude)**2 + (lng_pts - longitude)**2)
    index = np.argmin(distances)
    return np.unravel_index(index, distances.shape)


def get_rainfall_value(x, y):
    """
    Get the rainfall value for the given x/y value
    """

    lng, lat = pyproj.transform(BNG, WGS84, x, y)
    indexy, indexx = get_closest_grid_index(
        latitude_values, longitude_values, lng, lat)
    rainfall_value = rainfall_data.variables['rainfall'][0, indexy, indexx]

    return float(rainfall_value.flatten()[0])


def get_rainiest_library():
    """
    Get the rainiest library in the UK
    """

    postcode_data = pandas.read_csv("code_point_open.csv", header=None)
    postcode_data[0] = postcode_data[0].str.replace(" ", "")

    libraries_data = pandas.read_csv("libraries.csv", header=None)
    libraries_data[2] = libraries_data[2].str.replace(" ", "")
    libraries_data[2] = libraries_data[2].str.upper()
    libraries_data[2] = libraries_data[2].str.strip()
    libraries_data = libraries_data.merge(
        postcode_data, left_on=2, right_on=0, how="left")
    libraries_data['rainfall'] = libraries_data.apply(
        lambda row: get_rainfall_value(row["2_y"], row[3]), axis=1)

    header = ["1_x", "0_x", 2, "rainfall"]
    libraries_data.sort_values(by=['rainfall'], inplace=True)
    libraries_data.to_csv(
        'libraries_output.csv', columns=header)


get_rainiest_library()
