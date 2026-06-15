import logging
import os
import shutil
import pandas as pd
import numpy as np

logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

# This script reads the output csv-files from the modelrun and transforms them into a format that is better suited for the visualisation in excel. 

# Define the scenario name and the input, output and processed paths
scenario_name = 'baseline_germany_package_v2'

input_path = os.path.join('data', scenario_name, 'input', 'datasets')
output_path = os.path.join('data', scenario_name, 'output', 'export', 'flows')
processed_path = os.path.join('data', scenario_name, 'output', 'post-processing')

# Check if processed_path exists and handle accordingly
if os.path.exists(processed_path):
    shutil.rmtree(processed_path)
    os.makedirs(processed_path)
else:
    os.makedirs(processed_path)

# Define the list of csv files to be processed
csv_files = {'input': ['DomesticDemand'],
             'output': ['plastics_manufacturing__plastics_market', 'plastics_market__end_use_stock', 
                        'end_use_stock__waste_collection', 'waste_collection__waste_sorting', 'waste_sorting__sorted_waste_market', 
                        'sorted_waste_market__recycling', 'recycling__recyclate_sysenv']}

# Process each csv file
for category, files in csv_files.items():
    for file in files:
        # Read the csv file into a pandas dataframe
        if category == 'input':
            df = pd.read_csv(os.path.join(input_path, f'{file}.csv'))
            # Check the columns of the dataframe
            value_column = 'value' # Assuming the value column is named 'value', adjust if necessary
            index_column = 'time' # Assuming the index column is named 'time', adjust if necessary
            main_column = 'polymer' # Assuming the main column to pivot on is named 'polymer', adjust if necessary
            remaining_columns = [col for col in df.columns if col not in [index_column, value_column, main_column] and df[col].nunique() > 1]
            # Pivot the dataframe to have polymers as columns and years as rows
            pivot_df = df.pivot_table(index=index_column, columns=[main_column] + remaining_columns, values=value_column, aggfunc='sum')
            # Save the pivoted dataframe to a new csv file in the processed path
            pivot_df.to_csv(os.path.join(processed_path, f'{file}_processed.csv'))
            logging.info(f"Processed input file '{file}.csv' and saved it as '{file}_processed.csv' in '{processed_path}'")

        elif category == 'output':
            df = pd.read_csv(os.path.join(output_path, f'{file}.csv'), index_col=0)
            # Check the columns of the dataframe
            value_column = 'value' # Assuming the value column is named 'value', adjust if necessary
            index_column = 'time' # Assuming the index column is named 'time', adjust if necessary
            main_column = 'polymer' # Assuming the main column to pivot on is named 'polymer', adjust if necessary
            remaining_columns = [col for col in df.columns if col not in [index_column, value_column, main_column] and df[col].nunique() > 1]

            # Extra filter for regions: Germany only Scenario - Keep only rows where 'region' is 'Germany'
            if 'region' in df.columns:
                df = df[df['region'] == 'Germany']

            # Extra filter for waste_category: Keep only rows where 'waste_category' is 'mechanical_recycling'
            #if 'waste_category' in df.columns:
            #    df = df[df['waste_category'] == 'mechanical_recycling']

            # Pivot the dataframe to have polymers as columns and years as rows
            pivot_df = df.pivot_table(index=index_column, columns=[main_column] + remaining_columns, values=value_column, aggfunc='sum')
            # Save the pivoted dataframe to a new csv file in the processed path
            pivot_df.to_csv(os.path.join(processed_path, f'{file}_processed.csv'))
            logging.info(f"Processed output file '{file}.csv' and saved it as '{file}_processed.csv' in '{processed_path}'")