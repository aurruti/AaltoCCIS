import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

def df_name_cleanup(df, payment_col='EU_Payments'):
    """
    Clean up the names of the dataframe.
    
    Inputs:
    - df: (df) dataframe with the data
    - payment_col: (str) the name of the payment column (default: 'EU_Payments')

    Returns:
    - df: (df) dataframe with the cleaned up names
    """
    df['Region'] = df['Region'].str.replace('Comunidad Valenciana', 'Comunitat Valenciana')
    df['Region'] = df['Region'].str.replace('Centro', 'Centro (PT)')
    df['Region'] = df['Region'].str.replace('Dytiki Ellada', 'Dytiki Elláda')
    df['Region'] = df['Region'].str.replace('Lisboa', 'Área Metropolitana de Lisboa')
    df['Region'] = df['Region'].str.replace('Friesland', 'Friesland (NL)')
    df['Region'] = df['Region'].str.replace('Ciudad Autónoma de Ceuta', 'Ciudad de Ceuta')
    df['Region'] = df['Region'].str.replace('Ciudad Autónoma de Melilla', 'Ciudad de Melilla')
    df['Region'] = df['Region'].str.replace("Provence-Alpes-Côte d'Azur", 'Provence-Alpes-Côte d’Azur')
    df['Region'] = df['Region'].str.replace('Warmińsko-Mazurskie', 'Warmińsko-mazurskie')
    df['Region'] = df['Region'].str.replace('Prov. Limburg', 'Prov. Limburg (BE)')
    df['Region'] = df['Region'].str.replace('Southern and Eastern', 'Southern')
    df['Region'] = df['Region'].str.replace('Sud - Muntenia', 'Sud-Muntenia')
    df['Region'] = df['Region'].str.replace('Prov. Luxembourg', 'Prov. Luxembourg (BE)')
    df['Region'] = df['Region'].str.replace('Kujawsko-Pomorskie', 'Kujawsko-pomorskie')
    df['Region'] = df['Region'].str.replace('Bucureşti - Ilfov', 'Bucureşti-Ilfov')
    df['Region'] = df['Region'].str.replace("Valle d'Aosta/Vallée d'Aoste", 'Valle d’Aosta/Vallée d’Aoste')
    df['Region'] = df['Region'].str.replace('Nord - Pas-de-Calais', 'Nord-Pas de Calais')
    df['Region'] = df['Region'].str.replace('Réunion', 'La Réunion') 
    df['Region'] = df['Region'].str.replace('Centre', 'Centre — Val de Loire') 
    df['Region'] = df['Region'].str.replace('South Western Scotland', 'Southern Scotland') 
    df['Region'] = df['Region'].str.replace('Région de Bruxelles-Capitale / Brussels Hoofdstedelijk Gewest', 'Région de Bruxelles-Capitale/ Brussels Hoofdstedelijk Gewest') 
    df['Region'] = df['Region'].str.replace('Île de France', 'Ile-de-France') 
    df['Region'] = df['Region'].str.replace('Sterea Ellada', 'Sterea Elláda') 
    df['Region'] = df['Region'].str.replace('Anatoliki Makedonia,Thraki', 'Anatoliki Makedonia, Thraki')
    df.loc[df['NUTS2_ID']=='NL42', 'Region'] = 'Limburg (NL)'
    
    # New regions and their data
    paymentPL = float(df[df['NUTS2_ID']=='PL12'][payment_col].iloc[0])
    new_regions_pl = pd.DataFrame({'NUTS2_ID': ['PL91','PL92'], 'Region': ['Warszawski stołeczny', 'Mazowiecki regionalny'], payment_col: [paymentPL, paymentPL]})
    df = pd.concat([df, new_regions_pl], ignore_index=True)
    df = df.drop(df[df['NUTS2_ID']=='PL12'].index)

    paymentHUN = float(df[df['NUTS2_ID']=='HU10'][payment_col].iloc[0])
    new_regions_hun = pd.DataFrame({'NUTS2_ID': ['HU12','HU11'], 'Region': ['Pest', 'Budapest'], payment_col: [paymentHUN, paymentHUN]})
    df = pd.concat([df, new_regions_hun], ignore_index=True)
    df = df.drop(df[df['NUTS2_ID']=='HU10'].index)

    paymentLT = float(df[df['NUTS2_ID']=='LT00'][payment_col].iloc[0])
    new_regions_lt = pd.DataFrame({'NUTS2_ID': ['LT01','LT02'], 'Region': ['Sostinės regionas','Vidurio ir vakarų Lietuvos regionas'], payment_col: [paymentLT, paymentLT]})
    df = pd.concat([df, new_regions_lt], ignore_index=True)
    df = df.drop(df[df['NUTS2_ID']=='LT00'].index)

    paymentsHR04 = float(df[df['NUTS2_ID']=='HR04'][payment_col].iloc[0])
    new_regions_cro = pd.DataFrame({'NUTS2_ID': ['HR06','HR02','HR05'], 'Region': ['Sjeverna Hrvatska', 'Panonska Hrvatska', 'Grad Zagreb'], payment_col: [paymentsHR04, paymentsHR04, paymentsHR04]})
    df = pd.concat([df, new_regions_cro], ignore_index=True)
    df = df.drop(df[df['NUTS2_ID']=='HR04'].index)
    
    paymetsINLND = float(df[df['NUTS2_ID']=='UKI1'][payment_col].iloc[0])
    new_regions_uk1 = pd.DataFrame({'NUTS2_ID':['UKI4', 'UKI3'], 'Region': ['Inner London — East', 'Inner London — West'], payment_col: [paymetsINLND, paymetsINLND]})
    df = pd.concat([df, new_regions_uk1], ignore_index=True)
    df = df.drop(df[df['NUTS2_ID']=='UKI1'].index)
    paymentsOUTLND = float(df[df['NUTS2_ID']=='UKI2'][payment_col].iloc[0])
    new_regions_uk2 = pd.DataFrame({'NUTS2_ID':['UKI5', 'UKI6','UKI7'], 'Region': ['Outer London — East and North East', 'Outer London — South','Outer London — West and North West'], payment_col: [paymentsOUTLND, paymentsOUTLND, paymentsOUTLND]})
    df = pd.concat([df, new_regions_uk2], ignore_index=True)
    df = df.drop(df[df['NUTS2_ID']=='UKI2'].index)

    df.loc[df['NUTS2_ID']=='IE01', 'Region'] = 'Northern and Western'
    df.loc[df['Region']=='Northern and Western', 'NUTS2_ID'] = 'IE04'
    paymentsIE2 = float(df[df['NUTS2_ID']=='IE02'][payment_col].iloc[0])
    new_regions_ie2 = pd.DataFrame({'NUTS2_ID':['IE03', 'IE04'], 'Region': ['Southern', 'Eastern and Midland'], payment_col: [paymentsIE2, paymentsIE2]})
    df = pd.concat([df, new_regions_ie2], ignore_index=True)
    df = df.drop(df[df['NUTS2_ID']=='IE02'].index)

    return df

def ranking_visualization(df, title, n=10, top_bot = 'both', show=False, fig=None, ax=None):
    """
    Visualize the ranking of the data.
    
    Inputs:
    - df: (df) dataframe with the data
    - title: (str) the title of the plot
    - n: (int) the number of top regions to display (default: 10)
    - top_bot: (str 'top', 'bot', 'both') the top or bottom regions to display (default: 'both')
    - show: (bool) if True, show the plot (default: False)
    - fig: (plt.figure) the figure object (default: None)
    - ax: (plt.axis) the axis object (default: None)
    
    Returns:
    - fig: (plt.figure) the figure object
    - ax: (plt.axis) the axis object
    """
    try:
        df = df.drop(df[df['NUTS2_ID']=='UKZZ'].index)
    except:
        pass
    df = df.dropna(subset=['Region'])
    df = df.drop(columns='NUTS2_ID')
    df = df.sort_values(by='EU_Payments', ascending=False)
    if top_bot == 'top':
        df = df.head(n)
        title = f'{title} - Top {n} Regions'
    elif top_bot == 'bot':
        df = df.tail(n)
        title = f'{title} - Bottom {n} Regions'
    elif top_bot == 'both':
        n=+1 if n % 2 != 0 else n
        df = pd.concat([df.head(int(n/2)), df.tail(int(n/2))])
        title = f'{title} - Top {int(n/2)} and Bottom {int(n/2)} Regions'
    else:
        raise ValueError("top_bot must be 'top', 'bot', or 'both'")
    
    if fig is None and ax is None:
        fig, ax = plt.subplots()
    df.plot(kind='bar', x='Region', y='EU_Payments', ax=ax)
    plt.title(title)
    plt.ylabel('EU Payments (all time)')
    plt.xlabel('Region')
    plt.legend().remove()
    plt.xticks(rotation=15)
    if show:
        plt.show()
    return fig, ax

def display_map(df, shapefile, title, continental=True, cmap='gnuplot'):
    """
    Display the map of the data.
    
    Inputs:
    - df: (df) dataframe with the data
    - shapefile: (str) the path to the shapefile
    - title: (str) the title of the plot
    - continental: (bool) if True, display only continental Europe (default: True)
    - cmap: (str) the color map to use (default: 'gnuplot')
    
    Returns:
    - None
    """
    try:
        df = df.drop(df[df['NUTS2_ID']=='UKZZ'].index)
    except:
        pass
    if continental:
        try: 
            df = df.drop(df[df['Region'].str.contains('Região Autónoma dos Açores')].index)
        except:
            pass
        try:
            df = df.drop(df[df['Region'].str.contains('Região Autónoma da Madeira')].index)
        except:
            pass
        try:
            df = df.drop(df[df['Region'].str.contains('Canarias')].index)
        except:
            pass
        try:
            df = df.drop(df[df['Region'].str.contains('Guayane')].index)
        except:
            pass
        try:
            df = df.drop(df[df['Region'].str.contains('Guadeloupe')].index)
        except:
            pass
        try:
            df = df.drop(df[df['Region'].str.contains('Martinique')].index)
        except:
            pass
        try:
            df = df.drop(df[df['Region'].str.contains('La Réunion')].index)
        except:
            pass
        try:
            df = df.drop(df[df['Region'].str.contains('Ciudad Autónoma de Ceuta')].index)
        except:
            pass
        try:
            df = df.drop(df[df['Region'].str.contains('Ciudad Autónoma de Melilla')].index)
        except:
            pass

    gdf = gpd.read_file(shapefile)
    dif1 = set(df['Region']) - set(gdf['NAME_LATN'])
    df.rename(columns={'Region': 'NAME_LATN'}, inplace=True)
    gdf = gdf.merge(df, on='NAME_LATN')

    fig, ax = plt.subplots(1, 1)
    gdf.plot(column='EU_Payments', 
             ax=ax, 
             legend=True,
             legend_kwds={'label': "EU Payments (all time)", 'orientation': "vertical"},
             cmap=cmap,
             missing_kwds={ 
                "color": "lightgrey",
                "label": "Missing values",
             })
    plt.title(title)
    ax.set_axis_off()
    if continental:
        plt.xlim([-1.3*10**6, 3.94*10**6])
        plt.ylim([4.01*10**6, 1.12*10**7])
    plt.show()
    return None


if __name__ == "__main__":
    #shapefile = "mapfiles/NUTS_RG_01M_2021_4326_LEVL_2.shp"
    shapefile = "mapfiles/NUTS_RG_01M_2021_3857_LEVL_2.shp"
    #shapefile = "mapfiles/NUTS_RG_01M_2021_3035_LEVL_2.shp"
    # Load the data
    df_erdf = df_name_cleanup(pd.read_csv("data/erdf_map.csv"))
    df_eafrd = df_name_cleanup(pd.read_csv("data/eafrd_map.csv"))
    df_other = df_name_cleanup(pd.read_csv("data/others_map.csv"))
    df_all = df_name_cleanup(pd.read_csv("data/all_funds_map.csv"))

    df_erdf_norm = pd.read_csv("data/erdf_norm.csv")
    df_eafrd_norm = pd.read_csv("data/eafrd_norm.csv")
    df_other_norm = pd.read_csv("data/others_norm.csv")
    df_all_norm = pd.read_csv("data/all_funds_norm.csv")

    # Rankings - TOTAL
    ranking_visualization(df_erdf, 'ERDF Funds', top_bot='top')
    ranking_visualization(df_eafrd, 'EAFRD Funds', top_bot='top')
    ranking_visualization(df_other, 'Other Funds', top_bot='top')
    ranking_visualization(df_all, 'All Development Regional and Cohesion Funds', top_bot='top', show=True)

    # Maps - TOTAL
    display_map(df_erdf, shapefile, 'ERDF Funds')
    display_map(df_eafrd, shapefile, 'EAFRD Funds')
    display_map(df_other, shapefile, 'Other Funds')
    display_map(df_all, shapefile, 'All Development Regional and Cohesion Funds')

    # Rankings - by population	
    ranking_visualization(df_erdf_norm, 'ERDF Funds (per capita)', top_bot='top')
    ranking_visualization(df_eafrd_norm, 'EAFRD Funds (per capita)', top_bot='top')
    ranking_visualization(df_other_norm, 'Other Funds (per capita)', top_bot='top')
    ranking_visualization(df_all_norm, 'All Development Regional and Cohesion Funds (per capita)', top_bot='top', show=True)

    # Maps - by population
    display_map(df_erdf_norm, shapefile, 'ERDF Funds (per capita)')
    display_map(df_eafrd_norm, shapefile, 'EAFRD Funds (per capita)')
    display_map(df_other_norm, shapefile, 'Other Funds (per capita)')
    display_map(df_all_norm, shapefile, 'All Development Regional and Cohesion Funds (per capita)')