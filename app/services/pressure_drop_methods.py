import json

f = open('../ressources/hvacexporter_data.json')
data = json.load(f)

ventilation_system = data["system"]["SubSystems"]["ventilation"]["Components"]

print(ventilation_system)