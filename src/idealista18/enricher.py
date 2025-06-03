"""
    Eriches original data with census codes

"""
import idealista18.loader as loader
import geopandas as gpd

def load_enriched_data(city_name="Madrid", deduplicate_by_adid=False, enrich_census_code=True, enrich_idealista_areas=True):
    """
    Load and enrich Idealista data with census codes and Idealista zones.
    
    Parameters:
        city_name (str): The name of the city for which to load and enrich the data. Default is "Madrid".
        enrich_census_code (bool): Whether to enrich the data with census codes. Default is True.
        use_geopandas (bool): Whether to return a GeoDataFrame or a regular DataFrame. Default is True.
    Returns:
        DataFrame or GeoDataFrame: A DataFrame or GeoDataFrame containing the enriched Idealista data.
    """
    city_name = city_name.capitalize()  # Ensure the city name is capitalized
    # Load data and remove outliers (spatial)
    df = loader.load_data(city_name=city_name)
    df = loader.remove_geo_outliers(df, zscore=5)

    if deduplicate_by_adid:
        df = deduplicate_dataset(df, field="ASSETID", keep="first")
        if "PERIOD" in df.columns:
            df = df.drop(columns=["PERIOD"])

    gdf_ads = loader.convert_ads_to_geopandas(df, longitude_col='LONGITUDE', latitude_col='LATITUDE')
    gdf_idealista_areas = loader.load_geo_idealista_zones(city_name="Madrid", use_geopandas=True)
    gdf_census_areas = loader.load_geo_census_areas(city_name="Madrid", use_geopandas=True)

    # Añadimos los codigos censales (CUSEC)
    gdf_join = gpd.sjoin(gdf_ads, gdf_census_areas, how="inner")
    gdf_join = gdf_join.drop(columns=['index_right'])

    # Ahora las zonas idealista (LOCATIONID, LOCATIONNAME)
    gdf_join = gpd.sjoin(gdf_join, gdf_idealista_areas, how="inner")

    # Remove geometry column for DataFrame output (get only one record per ASSETID)
    df_area_codes = gdf_join[['ASSETID', 'LOCATIONID', 'LOCATIONNAME', 'CUSEC']]
    df_area_codes = df_area_codes.drop_duplicates(subset='ASSETID', keep='first')
    
    
    # Now create a final dataset that
    # Join df with df_area_codes by ASSETID (left join)
    df_enriched = df.merge(df_area_codes, on='ASSETID', how='left')

        # Left join with mean_price_idealista by LOCATIONID and LOCATIONNAME
    if enrich_census_code:
        mean_price_cusec = gdf_join.groupby(['CUSEC']).agg({
                                      'PRICE': ['median', 'mean','std'],
                                      'UNITPRICE': ['median', 'mean', 'count','std']}).reset_index()

        # Rename columns
        mean_price_cusec.columns = [
            'CUSEC',
            'CUSEC_PRICE_median',
            'CUSEC_PRICE_mean',
            'CUSEC_PRICE_std',
            'CUSEC_UNITPRICE_median',
            'CUSEC_UNITPRICE_mean',
            'CUSEC_UNITPRICE_count',
            'CUSEC_UNITPRICE_std'
        ]

        df_enriched = df_enriched.merge(mean_price_cusec, on=['CUSEC'], how='left')
    
    if enrich_idealista_areas:
        mean_price_idealista = gdf_join.groupby(['LOCATIONID','LOCATIONNAME']).agg({
            'PRICE': ['median', 'mean', 'std'],
            'UNITPRICE': ['median', 'mean', 'count', 'std']
        }).reset_index()

        # Rename columns
        mean_price_idealista.columns = [
            'LOCATIONID',
            'LOCATIONNAME',
            'ID_PRICE_median',
            'ID_PRICE_mean',
            'ID_PRICE_std',
            'ID_UNITPRICE_median',
            'ID_UNITPRICE_mean',
            'ID_UNITPRICE_count',
            'ID_UNITPRICE_std'
        ]
        # Convert to GeoDataFrame
        df_enriched = df_enriched.merge(mean_price_idealista, on=['LOCATIONID', 'LOCATIONNAME'], how='left')
    
    return df_enriched

def deduplicate_dataset(ads_dataset, field="ASSETID", keep="first"):
    """
    Remove duplicates from the dataset based on a specified field.
    This function drops duplicate rows in the dataset based on a specified field, keeping the first occurrence by default.              
    """
    ads_dataset_dedup = ads_dataset.drop_duplicates(subset=field, keep=keep)
    return ads_dataset_dedup

