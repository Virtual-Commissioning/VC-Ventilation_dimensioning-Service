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


## Now we need to create a service that loops through the system and applies the airflow

def service_to_calculate_airflow(ventilation_components):

    for supply_component in ventilation_components:
        
        if supply_component["ComponentType"] == "AirTerminal":
            
            if supply_component["ConnectedWith"][0]["ConnectorType"] == "suppliesFluidFrom":
                lookup_dictionary = create_lookup_dictionary(ventilation_components)
            
                airflow = supply_component["ConnectedWith"][0]["DesignFlow"]
                previous_component_tag = 0
                supply_system = True

                loop_to_supplying_fan(supply_component, airflow, previous_component_tag, lookup_dictionary, supply_system)
            
            elif supply_component["ConnectedWith"][0]["ConnectorType"] == "suppliesFluidTo":
                lookup_dictionary = create_lookup_dictionary(ventilation_components)
            
                airflow = supply_component["ConnectedWith"][0]["DesignFlow"]
                previous_component_tag = 0
                supply_system = False

                loop_to_supplying_fan(supply_component, airflow, previous_component_tag, lookup_dictionary, supply_system)
    

## Loop out to the supplying ventilation fan and sum up all the flows


def loop_to_supplying_fan(component, airflow, previous_component_tag, lookup_dictionary, supply_system):
    
    next_component_tag = find_next_component(component, lookup_dictionary, supply_system)
    
    ## Add the airflow to all the ports involved (excluded for instance ports from Tees that go in the wrong direction)
    add_airflow_to_ports(component, previous_component_tag, airflow)

    if component["ComponentType"] == "Fan":
        return 

    component_at_index = lookup_dictionary[next_component_tag]
    next_component = ventilation_components[component_at_index]
    previous_component_tag = component["Tag"]

    loop_to_supplying_fan(next_component, airflow, previous_component_tag, lookup_dictionary, supply_system)



def find_next_component(component, lookup_dictionary, supply_system):
    ports = component["ConnectedWith"]

    if supply_system == True:
        for port in ports:
            if port["ConnectorType"] == "suppliesFluidFrom" and port["Tag"] in lookup_dictionary:
                return port["Tag"]
    
    elif supply_system == False:
        for port in ports:
            if port["ConnectorType"] == "suppliesFluidTo" and port["Tag"] in lookup_dictionary:
                return port["Tag"]
            



def add_airflow_to_ports(component, previous_component_tag, airflow):
    ports = component["ConnectedWith"]
    
    for port in ports:
        if port["Tag"] == previous_component_tag and previous_component_tag != 0:
            port["DesignFlow"] += airflow
            
            if port["ConnectorType"] == "suppliesFluidFrom":
                port["DesignFlow"] += airflow
        


def create_lookup_dictionary(ventilation_components):
    lookup_dictionary = {}

    for i in range(len(ventilation_components)):
        lookup_dictionary[ventilation_components[i]["Tag"]] = i
    
    return lookup_dictionary


## Write the file
with open("../ressources/test_file.json", "w") as outfile:
    json.dump(ventilation_components, outfile)