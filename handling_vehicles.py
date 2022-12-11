import json
import xml.dom.minidom

# Load 'vehicles.meta' file, which is XML
doc = xml.dom.minidom.parse('vehicles.meta')

# Let's build up a dictionary of vehicles and their handling IDs so we can easily look them up later
vehicles_meta = dict()
for element in doc.getElementsByTagName('Item'):
    if element.getElementsByTagName('modelName'): # Has a model name so this Item actually is a vehicle
        modelName = element.getElementsByTagName('modelName')[0].firstChild.nodeValue
        handlingId = element.getElementsByTagName('handlingId')[0].firstChild.nodeValue.upper() # Make sure the handling ID is uppercase

        vehicles_meta[handlingId] = modelName # We need the model name to update the handling.json file afterwards

# Load 'handling.json' file, which is JSON as an object
handling_json = json.load(open('handling.json'))

# Now we can loop through the handling JSON
new_handling_json = dict()
for handlingId, data in handling_json.items():
    handlingId = handlingId.upper() # Make sure the handling ID is uppercase
    new_key = handlingId # We'll use this later

    # Make sure this 'handlingId' exists in 'vehicles_meta' before we try to use it
    if handlingId in vehicles_meta:
        new_key = vehicles_meta[handlingId].upper() # We'll use the model name instead of the handling ID

    # Add it to the new handling JSON
    new_handling_json[new_key] = data

# Count how many vehicles we have now
print('Found {} vehicles'.format(len(new_handling_json)))

# Save the new handling JSON
with open('handling.json', 'w') as f:
    json.dump(new_handling_json, f, indent=4)
    print('Saved handling.json')
