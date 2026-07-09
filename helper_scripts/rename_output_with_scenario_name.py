# Takes the output files of the transience_eu_mfa model and renames them to include the scenario name. 
# This way the output of different scenarios can be easily distinguished and compared.

import os
import shutil

# Parameters
module = 'plastics'  # Change this to your module name
scenario_name = 'certificates_baseline_germany_package_v3'  # Change this to your scenario name
file_prefix = 'v3' # If you want to rename the files with a specific prefix, set it here. Otherwise, it will use the scenario name as prefix.
new_output_dir = os.path.join('data', scenario_name + '_' + module, 'output', 'export', 'flows_renamed') # If you want to save the renamed files in a different directory, set it here. Otherwise, it will save them in a new directory next to the original folder.

if file_prefix is None:
    file_prefix = scenario_name
   
if new_output_dir is None:
    new_output_dir = os.path.join('data', scenario_name + '_' + module, 'output', 'export', 'flows_renamed')

# Define the original output directory
output_dir = os.path.join('data', scenario_name + '_' + module, 'output', 'export', 'flows')

# Create the new output directory if it doesn't exist and remove old files if it does exist
os.makedirs(new_output_dir, exist_ok=True)
for filename in os.listdir(new_output_dir):
    os.remove(os.path.join(new_output_dir, filename))

# Loop through the files in the original output directory
for filename in os.listdir(output_dir):
    if filename.endswith('.csv'):
        # Define the new filename with the scenario name as prefix
        new_filename = f"{file_prefix}_{filename}"
        # Define the full path for the original and new files
        original_file = os.path.join(output_dir, filename)
        new_file = os.path.join(new_output_dir, new_filename)
        # Rename (copy) the file to the new location with the new name
        shutil.copy2(original_file, new_file)
        print(f"Renamed '{original_file}' to '{new_file}' and saved it in '{new_output_dir}'")