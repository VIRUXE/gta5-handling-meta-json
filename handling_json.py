"""
First we read each 'vehicle.meta' file (XML format) inside the 'vehiclesmeta' folder.
If vehicle is not present in the dict already, add the 'modelName' to the dict, using the 'handlingId' as key.

The 'modelName' will serve afterwards as a key to the JSON file, in correlation to the 'handlingId' from the 'handling.meta' files (XML format), that will contain the handling data, for each vehicle.
"""

import os
import xml.etree.ElementTree as ET
import json
import time

# Dict to store the 'modelName' and 'handlingId' for each vehicle
handling_models = {}

# Iterate through all files in the 'vehiclesmeta' folder
start_time = time.time()
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
            handling_id = handling_id.text.upper() # Convert the handling ID to uppercase, so it matches the handling IDs from the 'handling.meta' files

            if handling_id in handling_models and model_name.text not in handling_models[handling_id]: # If handling ID is present and model name is not present in the list of model names
                handling_models[handling_id].append(model_name.text) # Append the model name to the list of model names
            else: # If handling ID is not present
                handling_models[handling_id] = [model_name.text] # Add the handling ID and the model name to the dict

parse_time = time.time() - start_time
print(f"\nFinished parsing 'vehicles.meta' files in {parse_time:.2f} seconds\n")

model_count = 0
handling_with_multiple_models = 0
for handling_id, models in handling_models.items():
    model_count += len(models)
    models_string = ', '.join(models)

    # Use a green color for handling IDs that are used by more than 1 vehicle
    if len(models) > 1:
        handling_with_multiple_models += 1
        print(f"\033[92mHandling '{handling_id}' is used by {len(models)} vehicles: '{models_string}'\033[0m")
    else:
        print(f"Handling '{handling_id}' is used by 1 vehicle: '{models_string}'")

# Count the number of vehicles
print(f"\nCompiled {len(handling_models)} handling IDs")
print(f"Compiled {model_count} vehicles")
print(f"Compiled {handling_with_multiple_models} handling IDs with multiple vehicles")

# Save the dict to a JSON file
with open('handling_models.json', 'w') as file:
    json.dump(handling_models, file, indent=4)
    print("Saved 'handling_models.json'")

"""
    Now we do almost the same thing, but for the 'handling.meta' files (XML format).
    We iterate through all files in the 'handlingmeta' folder.

    The 'handlingName' will serve afterwards as a key to the JSON file, in correlation to the 'handlingId' from the 'vehicle.meta' files
"""

def item_to_dict(item): # ! value attributes need to be parsed correctly
    """
    Convert an 'Item' element and all its children to a dict.
    """
    item_dict = {}

    for child in item:
        # If the child has children, recursively call this function
        if len(child) > 0:
            item_dict[child.tag] = item_to_dict(child)
        else:
            item_dict[child.tag] = child.text

    return item_dict

print("\n --- HANDLING META --- \n")
handling_meta = {}

# Iterate through all files in the 'handlingmeta' folder
start_time = time.time()
handling_not_present = list()

for file in os.listdir('handlingmeta'):
    print(f"Reading {file}...")
    # Read the XML file
    file_path = os.path.join('handlingmeta', file)
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Iterate through all 'Item' tags in the XML file, which contain the handling data
    for item in root.find('HandlingData'):
        handling_name = item.find('handlingName')
        handling_name = handling_name.text.upper() # Convert the handling name to uppercase, so it matches the handling IDs from the 'vehicle.meta' files

        # Only do something if this is a vehicle item and it's not already in the dict
        if handling_name is not None and handling_name not in handling_meta:
            print(f"[{file}] Checking vehicle '{handling_name}'...")

            if handling_name in handling_models: # If the handling ID is present in the 'handling_models' dict
                # Append it's equivalent models from 'handling_models' to the 'handling_meta' dict, using the 'models' key
                handling_meta[handling_name] = {
                    "models": handling_models[handling_name],
                    # ! This needs some more work since the values are not parsed correctly
                    "data": item_to_dict(item) # Convert entire 'item' element and all its children to a dict
                }
                # Print a green message if the handling ID is present in the 'handling_models' dict
                print(f"\033[92m[{file}] Added vehicle '{handling_name}' to 'handling_meta'\033[0m")
            else:
                # Add it to a list to output later
                if handling_name not in handling_not_present:
                    handling_not_present.append(handling_name)
                    print(f"\033[93m[{file}] Handling '{handling_name}' is not present in the 'handling_models' dict\033[0m")

parse_time = time.time() - start_time
print(f"\nFinished parsing 'handling.meta' files in {parse_time:.2f} seconds\n")

# Save the dict to a JSON file
with open('handling_meta.json', 'w') as file:
    json.dump(handling_meta, file, indent=4)
    print("Saved 'handling_meta.json'\n")

# Print all handling IDs that are not present in the 'handling_models' dict
print(f"Handling IDs that are not present in the 'handling.meta' files:\n{handling_not_present}")