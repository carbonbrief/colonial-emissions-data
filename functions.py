import pandas as pd
import numpy as np

def update_colonization_data(colonization_df, empire_df):
    # Initialize a copy of the second dataframe
    updated_empire_df = empire_df.copy()
    # Iterate through the first dataframe
    for _, row in colonization_df.iterrows():
        country = row['country']
        start_year = row['min year']
        end_year = row['max year']
        empire_country = row['empire1']
        # Filter the rows in the second dataframe where the year is within the colonization period
        mask = (empire_df['country'] == country) & (empire_df['year'] >= start_year) & (empire_df['year'] <= end_year)
        # Set the corresponding column value to 1 for the empire country during the colonization years
        updated_empire_df.loc[mask, empire_country] = 1
    updated_empire_df.fillna(0, inplace=True)
    return updated_empire_df

def get_empire_sums(wimmer_empire,drop_columns=['cowcode','country','year']):
    wimmer_empire_sum=wimmer_empire.drop(columns=drop_columns).sum(axis=1)
    sum_empire=pd.DataFrame({'sum':wimmer_empire_sum})
    wimmer_empire_merge=wimmer_empire.merge(sum_empire,left_index=True,right_index=True)
    sum_1_country_years=wimmer_empire_merge[wimmer_empire_merge['sum']==1]
    sum_0_country_years=wimmer_empire_merge[wimmer_empire_merge['sum']==0]
    sum_2_country_years=wimmer_empire_merge[wimmer_empire_merge['sum']==2]
    sum_0_2_country_years=wimmer_empire_merge[(wimmer_empire_merge['sum']!=0) & (wimmer_empire_merge['sum']!=1) & (wimmer_empire_merge['sum']!=2)]
    # with pd.option_context('display.max_rows', None, 'display.max_columns', 100):
    total_years=sum_1_country_years.size+sum_0_country_years.size+sum_2_country_years.size+sum_0_2_country_years.size
    return (sum_1_country_years.size/total_years, sum_0_country_years.size/total_years,sum_2_country_years.size/total_years, sum_0_2_country_years.size/total_years),sum_1_country_years, sum_0_country_years, sum_2_country_years, sum_0_2_country_years

def get_country_year_ranges(df):
    country_list=df.loc[:,'country'].unique()
    min_year_list=[]
    max_year_list=[]

    for country in country_list:
        min_year=df.loc[df['country']==country]['year'].min()
        min_year_list.append(min_year)
        max_year=df.loc[df['country']==country]['year'].max()
        max_year_list.append(max_year)

    range_df=pd.DataFrame({'country':country_list, 'min year':min_year_list, 'max year':max_year_list})
    return range_df

def get_country_empire_year_ranges(df):
    country_list=df.loc[:,'country'].unique()
    min_year_list=[]
    max_year_list=[]
    empire_list=[]
    emp=df.iloc[:,3:-1]
    for country in country_list:
        empires=emp.loc[df['country']==country].columns[emp.loc[df['country']==country].any()].to_list()
        min_year=df.loc[df['country']==country]['year'].min()
        min_year_list.append(min_year)
        max_year=df.loc[df['country']==country]['year'].max()
        max_year_list.append(max_year)
        empire_list.append(empires)

    range_df=pd.DataFrame({'country':country_list, 'min year':min_year_list, 'max year':max_year_list,'empires':empire_list})
    return range_df

def get_country_empire_year_ranges_2(df):
    country_list_unique=df.loc[:,'country'].unique()
    min_year_list=[]
    max_year_list=[]
    empire1_list=[]
    empire2_list=[]
    empire3_list=[]
    emp=df.iloc[:,3:-1]
    # print(emp.columns)
    country_list=[]
    for country in country_list_unique:
        country_years=df.loc[df['country']==country]['year'].to_list()
        country_years_split=split_into_consecutive_years(country_years)
        # print(country_years_split)
        for years in country_years_split:
            #calculate min and max year in this years segment
            min_year=df.loc[(df['country']==country) & (df['year'].isin(years))]['year'].min()
            max_year=df.loc[(df['country']==country) & (df['year'].isin(years))]['year'].max()
            #calculate empires at start and end of sequence to see if they are different
            min_empires=empires=emp.loc[(df['country']==country) & (df['year']==min_year)].columns[emp.loc[(df['country']==country) & (df['year']==min_year)].any()].to_list()
            max_empires=empires=emp.loc[(df['country']==country) & (df['year']==max_year)].columns[emp.loc[(df['country']==country) & (df['year']==max_year)].any()].to_list()
            empires=emp.loc[(df['country']==country) & (df['year'].isin(years))].columns[emp.loc[(df['country']==country) & (df['year'].isin(years))].any()].to_list()
            if min_empires !=max_empires: #suggests changes in empire status (even if sum is the same), need to split these into the different empire states
                # print(min_empires)
                # print(max_empires)
                change_years=find_years_with_column_changes(df.loc[(df['country']==country) & (df['year'].isin(years))], empires)
                # print(country)
                # print(change_years)
                change_years.insert(0,min_year)
                change_years.append(max_year)
                # print(change_years)
                range_loop=range(len(change_years[:-1]))
                for i in range(len(change_years[:-1])): #loop over years where changes occur
                    min_year=change_years[i]
                    if i != range_loop[-1]: #if last year, then do not subtract from max year
                        max_year=change_years[i+1]-1 #subtact minus 1 from change year to prevent overlap in entries
                    else:
                        max_year=change_years[i+1]
                    empires=emp.loc[(df['country']==country) & (df['year']==min_year)].columns[emp.loc[(df['country']==country) & (df['year']==min_year)].any()].to_list()
                    min_year_list.append(min_year)
                    max_year_list.append(max_year)
                    country_list.append(country)
                    empire1_list.append('')
                    empire2_list.append('')
                    empire3_list.append('')
                    if len(empires)>=1:
                        empire1_list[-1]=empires[0]
                    if len(empires)>=2:
                        empire2_list[-1]=empires[1]
                    if len(empires)>=3:
                        empire3_list[-1]=empires[2]
            else: #if empire lists not different at beginning and end 
                min_year_list.append(min_year)
                max_year_list.append(max_year)
                country_list.append(country)
                empire1_list.append('')
                empire2_list.append('')
                empire3_list.append('')
                if len(empires)>=1:
                    empire1_list[-1]=empires[0]
                if len(empires)>=2:
                    empire2_list[-1]=empires[1]
                if len(empires)>=3:
                    empire3_list[-1]=empires[2]
    range_df=pd.DataFrame({'country':country_list, 'min year':min_year_list, 'max year':max_year_list,'empire1':empire1_list,'empire2':empire2_list,'empire3':empire3_list})
    return range_df

def update_colonization_data_2(colonization_df, empire_df):
    # Initialize a copy of the second dataframe
    updated_empire_df = empire_df.copy()
    # Iterate through the first dataframe
    for _, row in colonization_df.iterrows():
        country = row['country']
        # print(country)
        start_year = row['min year']
        end_year = row['max year']
        empire_country = row['empire1']
        empire_country2 = row['empire2']
        empire_country3 = row['empire3']
        # Filter the rows in the second dataframe where the year is within the colonization period
        mask = (empire_df['country'] == country) & (empire_df['year'] >= start_year) & (empire_df['year'] <= end_year)
        #Determine other columns based on whether there are one or two empire columns in edit file
        if pd.isna(empire_country2) and pd.isna(empire_country3):
            other_columns=updated_empire_df.columns.difference(['cowcode','country','year',empire_country])
        elif pd.isna(empire_country3):
            other_columns=updated_empire_df.columns.difference(['cowcode','country','year',empire_country,empire_country2])
        else:
            other_columns=updated_empire_df.columns.difference(['cowcode','country','year',empire_country,empire_country2,empire_country3])
        #Assign empire values based on number of empires
        if pd.isna(empire_country2) and pd.isna(empire_country3):
            # print('yes')
            updated_empire_df.loc[mask, empire_country] = 1
        elif pd.isna(empire_country3):
            if empire_country=='Ottoman': #if Ottoman, use ratio to find other share
                updated_empire_df.loc[mask, empire_country2] = 1-updated_empire_df.loc[mask, empire_country]
            else:
                updated_empire_df.loc[mask, empire_country] = 1/2
                updated_empire_df.loc[mask, empire_country2] = 1/2
        else:
            if empire_country=='Ottoman':#if Ottoman, use ratio to find other share, for three empires, split other share into 2
                updated_empire_df.loc[mask, empire_country2] = (1-updated_empire_df.loc[mask, empire_country])/2
                updated_empire_df.loc[mask, empire_country3] = (1-updated_empire_df.loc[mask, empire_country])/2
            else:
                updated_empire_df.loc[mask, empire_country] = 1/3
                updated_empire_df.loc[mask, empire_country2] = 1/3
                updated_empire_df.loc[mask, empire_country3] = 1/3
        #Set other empire values to 0 based on other columns
        updated_empire_df.loc[mask, other_columns] = 0
    #Set Nans to 0
    updated_empire_df.fillna(0, inplace=True)
    return updated_empire_df

def update_colonization_data_not_0_1_2(colonization_df, empire_df):
    # Initialize a copy of the second dataframe
    updated_empire_df = empire_df.copy()
    # Iterate through the first dataframe
    for _, row in colonization_df.iterrows():
        country = row['country']
        start_year = row['min year']
        end_year = row['max year']
        empire_country = row['empire']
        empire_country2 = row['empire2']
        # Filter the rows in the second dataframe where the year is within the colonization period
        mask = (empire_df['country'] == country) & (empire_df['year'] >= start_year) & (empire_df['year'] <= end_year)

        if pd.isna(empire_country2):
            other_columns=updated_empire_df.columns.difference(['cowcode','country','year',empire_country])
        else:
            other_columns=updated_empire_df.columns.difference(['cowcode','country','year',empire_country,empire_country2])
        # Set the corresponding column value to 1 for the empire country during the colonization years
        if not pd.isna(empire_country2):
            if empire_country=='Ottoman':
                # updated_empire_df.loc[mask, empire_country] = updated_empire_df.loc[mask, empire_country]
                updated_empire_df.loc[mask, empire_country2] = 1-updated_empire_df.loc[mask, empire_country]
            else:
                updated_empire_df.loc[mask, empire_country] = 0.5
                updated_empire_df.loc[mask, empire_country2] = 0.5
        else:
            updated_empire_df.loc[mask, empire_country] = 1
        updated_empire_df.loc[mask, other_columns] = 0
    updated_empire_df.fillna(0, inplace=True)
    return updated_empire_df

def add_missing_countries_to_wimmer(wimmer,missing_df,copy_country):
    for i in range(len(missing_df['country'])):
        original_rows = wimmer[wimmer['country'] == copy_country]
        copied_rows = original_rows.copy()
        copied_rows['country'] = missing_df.loc[i,'country']
        copied_rows['cowcode'] = missing_df.loc[i,'cowcode']
        copied_rows['cowcode']=copied_rows['cowcode'].astype(int)
        wimmer = pd.concat([wimmer, copied_rows], ignore_index=True)
    return wimmer

def sort_cumu_emissions_terri_col(df,sortname1,sortname2,rankname1='Territorial Rank',rankname2='Colonial Rank'):
    df=df.sort_values(by=sortname1,ascending=False)
    df[rankname1] = range(1, len( df) + 1)
    df=df.sort_values(by=sortname2,ascending=False)
    df[rankname2] = range(1, len(df) + 1)
    df['Change in Rank']=df[rankname1]-df[rankname2]
    return df

def get_top20(df,sortname1,sortname2=np.nan):
    top20_1=df.head(20)
    top20_2=df.sort_values(by=sortname1,ascending=False).head(20)
    if not pd.isna(sortname2):
        top20_3=df.sort_values(by=sortname2,ascending=False).head(20)
        top20= pd.concat([top20_1,top20_2,top20_3]).drop_duplicates().reset_index(drop=True)
    else:
        top20= pd.concat([top20_1, top20_2]).drop_duplicates().reset_index(drop=True)
    return top20

def get_top21(df,sortname1,sortname2=np.nan):
    top20_1=df.head(21)
    top20_2=df.sort_values(by=sortname1,ascending=False).head(21)
    if not pd.isna(sortname2):
        top20_3=df.sort_values(by=sortname2,ascending=False).head(21)
        top20= pd.concat([top20_1,top20_2,top20_3]).drop_duplicates().reset_index(drop=True)
    else:
        top20= pd.concat([top20_1, top20_2]).drop_duplicates().reset_index(drop=True)
    return top20

def split_into_consecutive_years(years):
    if not years:
        return []

    sorted_years = sorted(set(years))
    consecutive_year_lists = []
    current_year_list = [sorted_years[0]]

    for year in sorted_years[1:]:
        if year == current_year_list[-1] + 1:
            current_year_list.append(year)
        else:
            consecutive_year_lists.append(current_year_list)
            current_year_list = [year]

    consecutive_year_lists.append(current_year_list)

    return consecutive_year_lists

def find_years_with_column_changes(dataframe, columns_to_check):
    if dataframe.empty:
        return []

    result_years = []
    current_values = None

    for index, row in dataframe.iterrows():
        year = row['year']  # Assuming 'Year' is the column with the years, replace it with your actual year column
        values = row[columns_to_check]

        if current_values is None:
            current_values = values
        elif any(values != current_values):
            result_years.append(year)
            current_values = values

    return result_years

def find_years_with_column_changes_2(dataframe, columns_to_check):
    if dataframe.empty:
        return []

    changed_rows = dataframe[columns_to_check].ne(dataframe[columns_to_check].shift(-1)).any(axis=1)
    result_years = dataframe.loc[changed_rows, 'year'].tolist()

    return result_years

def interpolate_column(group,column_name):
    group[column_name] = group[column_name].interpolate(method='linear',limit_direction='both')
    return group