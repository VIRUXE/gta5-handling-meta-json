local vehicleNames = {}

for _, modelName in pairs(GetAllVehicleModels()) do
    -- Ignore if the model is add-on
    local displayName = GetDisplayNameFromVehicleModel(modelName)
          displayName = displayName == 'CARNOTFOUND' and nil or displayName
    local labelText   = GetLabelText(displayName)

    vehicleNames[modelName] = {
        displayName = displayName,
        labelText   = labelText
    }
end

print('Saved vehicle names.')

TriggerServerEvent('vehicleNames:send', vehicleNames)