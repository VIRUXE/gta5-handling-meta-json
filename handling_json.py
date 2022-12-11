"""
First we read each 'vehicle.meta' file (XML format) inside the 'vehiclesmeta' folder.
If vehicle is not present in the dict already, add the 'modelName' to the dict, using the 'handlingId' as key.

The 'modelName' will serve afterwards as a key to the JSON file, in correlation to the 'handlingId' from the 'handling.meta' files (XML format), that will contain the handling data, for each vehicle.
"""

import os
import xml.etree.ElementTree as ET
import json

# Dict to store the 'modelName' and 'handlingId' for each vehicle
model_names = {}

# Iterate through all files in the 'vehiclesmeta' folder
for file in os.listdir('vehiclesmeta'):
    print(f"Reading {file}...")
    # Read the XML file
    file_path = os.path.join('vehiclesmeta', file)
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Iterate through all 'Item' tags in the XML file, which contain the vehicle data
    # Not all 'Item' tags are vehicles, so we need to check if both 'modelName' and 'handlingId' are present
    # The tags are inside the 'InitDatas' tag
    # Use modelName as value, handlingId as key
    for item in root.find('InitDatas'):
        # Get the elements 'modelName' and 'handlingId' from the 'Item' tag
        model_name = item.find('modelName')
        handling_id = item.find('handlingId')

        # Check if both elements are present
        if model_name is not None and handling_id is not None:
            # Since an handling ID can be used for multiple vehicles, we need to check if the handling ID is already present in the dict
            # If it is, we need to append the model name to the list of model names
            # If it isn't, we need to add the handling ID and the model name to the dict
            if handling_id.text in model_names and model_name.text not in model_names[handling_id.text]: # If handling ID is present and model name is not present in the list of model names
                model_names[handling_id.text].append(model_name.text) # Append the model name to the list of model names
            else: # If handling ID is not present
                model_names[handling_id.text] = [model_name.text] # Add the handling ID and the model name to the dict

# Count how many vehicles are in each handling ID
model_count = 0
handling_with_multiple_models = 0
for handling_id, models in model_names.items():
    model_count += len(models)
    models_string = ', '.join(models)
    # Use a red color for handling IDs that are used by more than 1 vehicle
    if len(models) > 1:
        handling_with_multiple_models += 1
        print(f"\033[31mHandling ID '{handling_id}' is used by {len(models)} vehicles: '{models_string}'\033[0m")
    else:
        print(f"Handling ID '{handling_id}' is used by {len(models)} vehicles: '{models_string}'")

# Count the number of vehicles
print(f"\nCompiled {len(model_names)} handling IDs")
print(f"Compiled {model_count} vehicles")
print(f"Compiled {handling_with_multiple_models} handling IDs with multiple vehicles")
# Save the dict to a JSON file
with open('handling_models.json', 'w') as file:
    json.dump(model_names, file, indent=4)
    print("Saved 'handling_models.json'")