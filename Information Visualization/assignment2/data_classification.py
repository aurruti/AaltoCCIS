import pandas as pd
from visualize import df_name_cleanup

def class_by_fund(df, fund, folder='data', inverse=False):
    """
    Classify the data by fund.
    
    nputs:
    - df: (df) dataframe with the data
    - fund: (str) the fund to classify by
    - folder: (str) the folder to save the data (default: 'data')
    - inverse: (bool) if True, classify by all funds except the one specified (default: False)
    
    Returns:
    - df_fund: (df) dataframe with the data classified by fund
    - df_fund_map: (df) dataframe with the data classified by fund and NUTS2_ID (and only these columns)
    """
    if not inverse:
        df_fund = df[df['Fund'] == fund]
    else:
        df_fund = df[df['Fund'] != fund]
    df_fund_map = df_fund.groupby('NUTS2_ID').sum().reset_index()
    df_fund_map = df_fund_map[['NUTS2_ID', 'EU_Payment_annual']]
    df_fund_map.rename(columns={'EU_Payment_annual': 'EU_Payments'}, inplace=True)
    
    # Add region name column from NUTS2_name column in df_fund
    df_fund_map['Region'] = str('')
    for nuts2id in df_fund_map['NUTS2_ID'].values:
        region_name = df_fund[df_fund['NUTS2_ID'] == nuts2id]['NUTS2_name'].values[0]
        df_fund_map.loc[df_fund_map['NUTS2_ID'] == nuts2id, 'Region'] = region_name
    
    # Save the data
    df_fund_map.to_csv(f"{folder}/{fund.lower()}_map.csv", index=False) if not inverse else df_fund_map.to_csv(f"{folder}/not_{fund}_map.csv", index=False)
    return df_fund, df_fund_map

def read_pop_data(filepath, sheet_name='Sheet 1', skiprows=range(0,7), pop_row=0, year=2019):
    """
    Read the population data.
    
    Inputs:
    - filepath: (str) the path to the population data
    - sheet_name: (str) the name of the sheet in the Excel file (default: 'Sheet 1')
    - skiprows: (list) the rows to skip when reading the Excel file (default: range(0,7))
    - pop_row: (int) row to pop, with not useful data (default: 0)
    - year: (int) the year to get the population data for (default: 2019)

    Returns:
    - df: (df) dataframe with the population data
    """
    df = pd.read_excel(filepath, sheet_name=sheet_name, skiprows=skiprows)
    df = df.drop(pop_row)
    df = df[['TIME', 'TIME.1', '2019', '2020']]
    df.rename(columns={'TIME': 'NUTS2_ID', 'TIME.1': 'Region'}, inplace=True)
    for pop in df.iterrows():
        if pop[1]['2019'] == ':' and pop[1]['2020'] != ':':
            df.loc[df['NUTS2_ID'] == pop[1]['NUTS2_ID'], '2019'] = pop[1]['2020']
    df = df[['NUTS2_ID', 'Region', '2019']]
    return df

def norm_by_pop(df, df_pop, name, folder='data'):
    """
    Normalize the data by population.
    
    Inputs:
    - df: (df) dataframe with the data
    - df_pop: (df) dataframe with the population data
    - folder: (str) the folder to save the data (default: 'data')
    
    Returns:
    - df_norm: (df) dataframe with the data normalized by population
    """
    df = df_name_cleanup(df)
    for datapoint in df.iterrows():
        already = False
        nuts2id = datapoint[1]['NUTS2_ID']
        if nuts2id == 'UKM2':
            nuts2id = 'UKM7'
            df.loc[df['NUTS2_ID'] == 'UKM2', 'NUTS2_ID'] = 'UKM7'
        if nuts2id == 'UKM3':
            nuts2id = 'UKM9'
            df.loc[df['NUTS2_ID'] == 'UKM3', 'NUTS2_ID'] = 'UKM9'
        if nuts2id == 'LT01' or nuts2id == 'LT02':
            df_pop.loc[df_pop['NUTS2_ID'] == nuts2id, '2019'] = df_pop[df_pop['NUTS2_ID'] == 'LT0']['2019'].values[0]
        if nuts2id == 'IE05' or nuts2id == 'IE06':
            already = True
            pop = df_pop[df_pop['NUTS2_ID'] == 'IE05']['2019'].values[0] + df_pop[df_pop['NUTS2_ID'] == 'IE06']['2019'].values[0]
            df.loc[df['NUTS2_ID'] == nuts2id, 'EU_Payments'] = df.loc[df['NUTS2_ID'] == nuts2id, 'EU_Payments'] / pop
        
        if not already:
            try:
                pop = df_pop[df_pop['NUTS2_ID'] == nuts2id]['2019'].values[0]
                df.loc[df['NUTS2_ID'] == nuts2id, 'EU_Payments'] = df.loc[df['NUTS2_ID'] == nuts2id, 'EU_Payments'] / pop
            except:
                region = datapoint[1]['Region']
                try:
                    pop = df_pop[df_pop['Region'] == region]['2019'].values[0]
                    df.loc[df['Region'] == region, 'EU_Payments'] = df.loc[df['Region'] == region, 'EU_Payments'] / pop
                except:
                    if nuts2id != 'UKZZ':
                        print(f"Population data not found for {nuts2id} - {region}") 
                    continue
        
    
    # Save the data
    df.to_csv(f"{folder}/{name}_norm.csv", index=False)
    return df
    

if __name__ == "__main__":
    # # Read the CSV file
    # df = pd.read_csv("data/Historic_EU_payments_-_regionalised_and_modelled.csv")

    # # Clean up the numeric columns
    # numeric_cols = ['EU_Payment_annual', 'Modelled_annual_expenditure', 'Standard_Deviation_of_annual_expenditure']
    # for col in numeric_cols:
    #     df[col] = df[col].str.replace(',', '').astype(float)

    # # ERDF Funds
    # _, df_erdf = class_by_fund(df, 'ERDF')
    # print(df_erdf.head(10))

    # # EAFRD Funds
    # _, df_eafrd = class_by_fund(df, 'EAFRD')
    # print(df_eafrd.head(10))

    # # Other Funds
    # df_other, _ = class_by_fund(df, 'EAFRD', inverse=True)
    # _, df_other = class_by_fund(df_other, 'ERDF', inverse=True)
    # print(df_other.head(10))

    # # All Funds
    # df_all = df.groupby('NUTS2_ID').sum().reset_index()
    # df_all = df_all[['NUTS2_ID', 'EU_Payment_annual']]
    # df_all.rename(columns={'EU_Payment_annual': 'EU_Payments'}, inplace=True)
    # df_all['Region'] = str('')
    # for nuts2id in df_all['NUTS2_ID'].values:
    #     region_name = df[df['NUTS2_ID'] == nuts2id]['NUTS2_name'].values[0]
    #     df_all.loc[df_all['NUTS2_ID'] == nuts2id, 'Region'] = region_name
    # df_all.to_csv("data/all_funds_map.csv", index=False)

    df_pop = read_pop_data("data/demo_r_gind3_spreadsheet.xlsx")
    df = pd.read_csv("data/all_funds_map.csv")
    df = norm_by_pop(df, df_pop, 'all_funds')
    df = pd.read_csv("data/erdf_map.csv")
    df = norm_by_pop(df, df_pop, 'erdf')
    df = pd.read_csv("data/eafrd_map.csv")
    df = norm_by_pop(df, df_pop, 'eafrd')
    df = pd.read_csv("data/others_map.csv")
    df = norm_by_pop(df, df_pop, 'others')