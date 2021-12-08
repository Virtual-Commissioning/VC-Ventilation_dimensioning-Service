import json

f = open('../ressources/hvacexporter_data.json')
data = json.load(f)

## ventilation_system = data["system"]["SubSystems"]["ventilation"]["Components"]

## Set all flows to zero

ventilation_components = data["system"]["SubSystems"]["ventilation"]["Components"]

for component in ventilation_components:
    ports = component["ConnectedWith"]
    
    for port in ports:
        port["DesignFlow"] = 0

## Find the air terminals and their airflow demand

rooms = data["spaces"]["SpacesInModel"]
rooms_with_terminals = []

for room in rooms:
    tag = room["Tag"]
    ventilation_req = room["IndoorClimateZone"]["Ventilation"]["AirFlow"]["DesignerRequirement"]

    supply_terminals = []
    extract_terminals = []

    for component in ventilation_components:
        if component["ComponentType"] == "AirTerminal":
            if tag in component["ContainedInSpaces"]:
                for port in component["ConnectedWith"]:
                    if port["ConnectorType"] == "suppliesFluidFrom":
                        supply_terminals.append(component["Tag"])
                    if port["ConnectorType"] == "suppliesFluidTo":
                        extract_terminals.append(component["Tag"])
 
    room_terminal_dict = {tag: {"ventilation_airflow": ventilation_req, 
                                "supply_terminals": supply_terminals,
                                "extract_terminals": extract_terminals}}
    
    rooms_with_terminals.append(room_terminal_dict)

print(rooms_with_terminals)

## Apply the ventilation requirement from the room, to the air terminal

for rooms in rooms_with_terminals:
    for key in rooms.keys():
        room = rooms[key]
        
        no_of_supply_terminals_in_room = len(room["supply_terminals"])
        ventilation_demand_pr_supply_terminal = room["ventilation_airflow"] / no_of_supply_terminals_in_room

        no_of_extract_terminals_in_room = len(room["extract_terminals"])
        ventilation_demand_pr_extract_terminal = room["ventilation_airflow"] / no_of_extract_terminals_in_room

        ## Set the new value on the terminals
        for component in ventilation_components:
            
            if component["Tag"] in room["supply_terminals"]:
                for port in component["ConnectedWith"]:
                    port["DesignFlow"] = ventilation_demand_pr_supply_terminal
            
            if component["Tag"] in room["extract_terminals"]:
                for port in component["ConnectedWith"]:
                    port["DesignFlow"] = ventilation_demand_pr_extract_terminal
                    print(port["DesignFlow"])

## Now we need to create a service that loops through the system and applies the airflow






    



## Loop out to the supplying ventilation fan and sum up all the flows