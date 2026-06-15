import os
import pandas as pd


# This script reads in a csv file and copies parameter information for one plymer and adds them to the file for multiple new polymers that have the same parameters

filenames = ['EoLCollectionRate', 'EoLUtilisationRate', 'SortingRate', 'DeprivedRate', 'RecyclingConversionRate', 'RecyclateShare', 'Lifetime']
#filenames = ['MarketShare'] 
sector = 'PET beverage bottles'

#polymers = {'PP': ['PP-Food-Flex', 'PP-Food-Rigid', 'PP-Non-Food'],
#            'PE-LD/-LLD': ['LDPE-Food-Flex', 'LDPE-Food-Rigid', 'LDPE-Non-Food'],
#            'PE-HD/-MD': ['HDPE-Food-Rigid', 'HDPE-Non-Food']}
polymers = {'PET': ['PET-Food']}


# Read in the csv files
for file in filenames:

    df = pd.read_csv(os.path.join('data', 'new_polymers_germany_plastics', 'input', 'datasets', f'{file}.csv'))
    # Define the polymers to be added
   
    new_rows = []
    for old_polymer, new_polymers in polymers.items():
        # Filter the dataframe for the specified sector and old polymer
        filtered_df = df[(df['sector'] == sector) & (df['polymer'] == old_polymer)]
        # Create new rows for each new polymer
        for new_polymer in new_polymers:
            new_row = filtered_df.copy()
            new_row['polymer'] = new_polymer
            new_rows.append(new_row)

    # Concatenate the new rows with the original dataframe
    new_df = pd.concat([df] + new_rows, ignore_index=True)
    # Save the updated dataframe to a new csv file
    print(f"Saving updated dataframe for {file} with {len(new_df)} rows.")
    new_path = os.path.join('data', 'new_polymers_germany_plastics', 'input', 'new_datasets', f'{file}.csv')
    new_df.to_csv(new_path, index=False)