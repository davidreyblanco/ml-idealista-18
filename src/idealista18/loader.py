"""
loader.py - Module for loading data in the idealista18 package.
"""

import pandas as pd
import geopandas as geopandas
from shapely import wkt
from shapely.geometry import Point


def load_data(city_name="Madrid"):
    """
    Load data from the Idealista18 dataset.
    This function retrieves the dataset for a specified city, defaulting to Madrid.
    
    Parameters:
    - city_name (str): The name of the city for which to load the dataset. Default is "Madrid".
    
    Returns:            
    - DataFrame: A pandas DataFrame containing the dataset for the specified city.
    """
    city_name = city_name.capitalize() # Ensure the city name is capitalized
    dataset = pd.read_csv(f'https://raw.githubusercontent.com/davidreyblanco/ml-training/master/data/idealista18/data/assets/es_home_sale_{city_name}_2018.csv.gz', sep=";")    
    return dataset

def convert_ads_to_geopandas(dataset, longitude_col='LONGITUDE', latitude_col='LATITUDE'):
    """
    Convert a DataFrame of ads to a GeoDataFrame.
    This function takes a DataFrame containing longitude and latitude columns and converts it to a GeoDataFrame.
    
    Parameters:
        dataset (DataFrame): The DataFrame containing the ads data.
        longitude_col (str): The name of the column containing longitude values. Default is 'LONGITUDE'.
        latitude_col (str): The name of the column containing latitude values. Default is 'LATITUDE'.
    
    Returns:
        GeoDataFrame: A GeoDataFrame containing the ads data with geometry based on longitude and latitude.
    """
    geometry = [Point(xy) for xy in zip(dataset[longitude_col], dataset[latitude_col])]
    df_prices = dataset.drop([longitude_col, latitude_col], axis=1)
    gdf_ads = geopandas.GeoDataFrame(df_prices, crs="EPSG:4326", geometry=geometry)
    return gdf_ads

def load_osm_data(city_name="Madrid", use_geopandas=True):
    """
    Load OpenStreetMap data for a specified city.
    
    Parameters:
    city_name (str): The name of the city for which to load the OSM data. Default is "Madrid".
    
    Returns:
    DataFrame: A pandas DataFrame containing the OSM data for the specified city.
    """
    city_name = city_name.capitalize() # Ensure the city name is capitalized
    osm_data = pd.read_csv(f'https://raw.githubusercontent.com/davidreyblanco/ml-training/master/data/idealista18/data/osm/osm-pois-{city_name}.csv.gz', sep=";")
    
    if use_geopandas:
        osm_data = convert_ads_to_geopandas(osm_data, longitude_col='LNG', latitude_col='LAT')
    
    return osm_data



def load_geo_idealista_zones(city_name="Madrid", use_geopandas=True):
    """ Load Idealista zone polygons for a specified city.

    Parameters: 
        city_name (str): The name of the city for which to load the Idealista zone polygons. Default is "Madrid".
        use_geopandas (bool): Whether to return a GeoDataFrame or a regular DataFrame. Default is True.
    Returns:
        DataFrame or GeoDataFrame: A DataFrame or GeoDataFrame containing the Idealista zone polygons for the specified city. 
    """
    city_name = city_name.capitalize() # Ensure the city name is capitalized
    city_polygons = pd.read_csv(f'https://raw.githubusercontent.com/davidreyblanco/ml-training/master/data/idealista18/data/polygons/{city_name}_polygons.csv.gz', sep=";")
    
    if use_geopandas:
        city_polygons['geometry'] = city_polygons['WKT'].apply(wkt.loads)
        gdf_polygons = geopandas.GeoDataFrame(city_polygons['geometry'], crs='epsg:4326')
        gdf_polygons['LOCATIONID'] = city_polygons['LOCATIONID']
        gdf_polygons['LOCATIONNAME'] = city_polygons['LOCATIONNAME']
        return gdf_polygons
    else:
        return city_polygons


def load_geo_census_areas(city_name="Madrid", use_geopandas=True):
    """ Load census area polygons for a specified city.

    Parameters:
        city_name (str): The name of the city for which to load the census area polygons. Default is "Madrid".
        use_geopandas (bool): Whether to return a GeoDataFrame or a regular DataFrame. Default is True.
    
    Returns:
        DataFrame or GeoDataFrame: A DataFrame or GeoDataFrame containing the census area polygons for the specified city.
    """
    city_name = city_name.capitalize() # Ensure the city name is capitalized
    city_polygons_census = pd.read_csv(f'https://raw.githubusercontent.com/davidreyblanco/ml-training/master/data/idealista18/data/ine/ine-censal-polygon-boundaries-2011-{city_name}.csv.gz', sep=";")

    if use_geopandas:    

        city_polygons_census['geometry'] = city_polygons_census['WKT'].apply(wkt.loads)
        gdf_polygons_census = geopandas.GeoDataFrame(city_polygons_census['geometry'], crs='epsg:4326')

        # Añadimos el código de sección censal
        gdf_polygons_census['CUSEC'] = city_polygons_census['CUSEC']

        city_polygons_census = gdf_polygons_census
    
    return city_polygons_census


def remove_geo_outliers(dataset, zscore=3):
    """
    Remove geographical outliers based on latitude and longitude.
    
    Parameters:
    df (DataFrame): The DataFrame containing the data.
    zscore (float): The SD times used to remove instances.
    
    Returns:
    DataFrame: The DataFrame with outliers removed.
    """
    lat_mean = dataset['LATITUDE'].median()
    #lat_std = (dataset['LATITUDE'] - lat_mean).abs().median()
    lat_std = dataset['LATITUDE'].std()
    lon_mean = dataset['LONGITUDE'].median()
    #lon_std = (dataset['LONGITUDE'] - lon_mean).abs().median()
    lon_std = dataset['LONGITUDE'].std()

    dataset = dataset[
            (dataset['LATITUDE'] >= lat_mean - zscore * lat_std) & (dataset['LATITUDE'] <= lat_mean + zscore * lat_std) &
            (dataset['LONGITUDE'] >= lon_mean - zscore * lon_std) & (dataset['LONGITUDE'] <= lon_mean + zscore * lon_std)
    ]

    return dataset
