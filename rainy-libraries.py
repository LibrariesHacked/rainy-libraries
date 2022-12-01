import pandas
import netCDF4 as nc
import numpy as np

from pyproj import CRS, Transformer

BNG = CRS.from_proj4(
    "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +towgs84=370,-108,434,0,0,0,0 +units=m +no_defs +type=crs")
WGS84 = CRS.from_proj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

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

    transformer = Transformer.from_crs(BNG, WGS84)
    lng, lat = transformer.transform(x, y)
    indexy, indexx = get_closest_grid_index(
        latitude_values, longitude_values, lng, lat)
    rainfall_value = rainfall_data.variables['rainfall'][0, indexy, indexx]

    return float(rainfall_value.flatten()[0])


def get_rainiest_library():
    """
    Get the rainiest library in the UK
    """

    postcode_col_names = ['postcode', 'positional_quality', 'easting', 'northing', 'country_code',
                          'nhs_regional_ha_code', 'nhs_ha_code', 'admin_county_code', 'admin_district_code', 'admin_ward_code']
    postcode_data = pandas.read_csv(
        "code_point_open.csv", header=None, names=postcode_col_names)
    postcode_data["postcode"] = postcode_data["postcode"].str.replace(" ", "")

    libraries_col_names = ['service', 'library_name', 'postcode']
    libraries_data = pandas.read_csv(
        "libraries.csv", header=None, names=libraries_col_names)
    libraries_data["postcode"] = libraries_data["postcode"].str.replace(
        " ", "")
    libraries_data["postcode"] = libraries_data["postcode"].str.upper()
    libraries_data["postcode"] = libraries_data["postcode"].str.strip()
    libraries_data = libraries_data.merge(
        postcode_data, left_on="postcode", right_on="postcode", how="left")
    libraries_data["rainfall"] = libraries_data.apply(
        lambda row: get_rainfall_value(row["easting"], row["northing"]), axis=1)

    header = ["service", "library_name", "rainfall"]
    libraries_data.sort_values(by=["rainfall"], inplace=True)
    libraries_data.to_csv(
        'rainy_library_results.csv', columns=header, index=False)


get_rainiest_library()
