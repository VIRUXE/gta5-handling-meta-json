RegisterNetEvent('vehicleNames:send', function (vehicleNames)
    print('Saving vehicle names to file...')
    SaveResourceFile(GetCurrentResourceName(), 'vehicle_names.json', json.encode(vehicleNames), -1)
end)