"""
Grab the contents of 'handling.meta.json' onto the 'handling' variable
Print the first entry of the 'HandlingData' key
"""
import json

with open('handling.meta.json') as f:
    handling = json.load(f)

vehicles = handling['HandlingData']
# Count the number of vehicles in the 'vehicles' list
print ('Amount of vehicles: ' + str(len(vehicles)) + ' in handling.meta.json')

# def getInternalVehicleName(handlingName):


def sanitizeVehicle(vehicle_node):
    del vehicle_node['type'] # Delete the 'type' key
    # del vehicle_node['handlingName'] # Delete the 'handlingName' key

    for key, value in vehicle_node.items(): # Loop through all the parameters in the vehicle node
        # Check if value is a node and contains a 'value' key
        if isinstance(value, dict) and 'value' in value:
            vehicle_node[key] = value['value']
        elif isinstance(value, list): # Check if the value is a list
            new_node = dict() # Create a new list
            for node in range(len(value)):
                sub_handling_type = value[node]['type'] # Grab the sub handling type
                # Ignore if sub handling type is 'null'
                if sub_handling_type != 'NULL':
                    del value[node]['type'] # Delete the 'type' key
                    for sub_key, sub_value in value[node].items():
                        if 'value' in sub_value:
                            if '\n' in sub_value['value']: # 
                                new_list = list()
                                for line in sub_value['value'].split('\n'):
                                    # Trim whitespace from the beginning and end of the line
                                    line = line.strip()
                                    new_list.append(line)

                                value[node][sub_key] = new_list # Replace the 'value' key with the actual value
                            else:
                                value[node][sub_key] = sub_value['value'] # Replace the 'value' key with the actual value
                        else: # Means it's either a list or a dict
                            # Now we want to make sure there are no empty lists inside other lists
                            if isinstance(sub_value, list):
                                # Go through the list and remove any empty lists
                                for sub_sub_key, sub_sub_value in enumerate(sub_value):
                                    # If the value is a list and it's empty, remove it
                                    if isinstance(sub_sub_value, list):
                                        del sub_value[sub_sub_key]
                                    
                        new_node[sub_handling_type] = value[node] # Add the node to the new list

            vehicle_node[key] = new_node # Add the sub handling type as a key to the list

    # Now let's create a fresh dict with only the keys that are not an empty dict
    new_vehicle_node = dict()
    for key, value in vehicle_node.items():
        if value != {}:
            new_vehicle_node[key] = value

    return new_vehicle_node # Return the sanitized vehicle node

# Sanitize all the vehicles in the 'vehicles' list and them to the 'jsonOutput' list, without brackets
jsonOutput = dict()
for vehicle in vehicles:
    vehicle_name = vehicle['handlingName'].upper() # Grab the name of the vehicle so we can use it as a key
    jsonOutput[vehicle_name] = sanitizeVehicle(vehicle)

# Write the sanitized vehicles to a new file
with open('handling.json', 'w') as f:
    json.dump(jsonOutput, f, indent=4, sort_keys=True)