import json

def airflow_determinator(data):
    flow_system_classes = json.loads(data)
    ventilation_components = flow_system_classes["system"]["SubSystems"]["ventilation"]["Components"]
    
    set_all_flows_to_zero(ventilation_components)

    rooms_with_terminals = find_air_terminals_and_airflow(flow_system_classes, ventilation_components)

    apply_ventilation_req_from_room_to_terminal(rooms_with_terminals, ventilation_components)

    service_to_calculate_airflow(ventilation_components)

    return json.dumps(ventilation_components)



## Set all flows to zero
def set_all_flows_to_zero(ventilation_components):
    for component in ventilation_components:
        ports = component["ConnectedWith"]
        
        for port in ports:
            port["DesignFlow"] = 0



## Find the air terminals and their airflow demand
def find_air_terminals_and_airflow(flow_system_classes,ventilation_components):
    rooms = flow_system_classes["spaces"]["SpacesInModel"]
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

    return rooms_with_terminals


## Apply the ventilation requirement from the room, to the air terminal
def apply_ventilation_req_from_room_to_terminal(rooms_with_terminals, ventilation_components):
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

                loop_to_supplying_fan(ventilation_components, supply_component, airflow, previous_component_tag, lookup_dictionary, supply_system)
            
            elif supply_component["ConnectedWith"][0]["ConnectorType"] == "suppliesFluidTo":
                lookup_dictionary = create_lookup_dictionary(ventilation_components)
            
                airflow = supply_component["ConnectedWith"][0]["DesignFlow"]
                previous_component_tag = 0
                supply_system = False

                loop_to_supplying_fan(ventilation_components, supply_component, airflow, previous_component_tag, lookup_dictionary, supply_system)
    

## Loop out to the supplying ventilation fan and sum up all the flows


def loop_to_supplying_fan(ventilation_components, component, airflow, previous_component_tag, lookup_dictionary, supply_system):
    
    next_component_tag = find_next_component(component, lookup_dictionary, supply_system)
    
    ## Add the airflow to all the ports involved (excluded for instance ports from Tees that go in the wrong direction)
    add_airflow_to_ports(component, previous_component_tag, airflow)

    if component["ComponentType"] == "Fan":
            return

    component_at_index = lookup_dictionary[next_component_tag]
    next_component = ventilation_components[component_at_index]
    previous_component_tag = component["Tag"]

    loop_to_supplying_fan(ventilation_components, next_component, airflow, previous_component_tag, lookup_dictionary, supply_system)



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
        


def create_lookup_dictionary(ventilation_components):
    lookup_dictionary = {}

    for i in range(len(ventilation_components)):
        lookup_dictionary[ventilation_components[i]["Tag"]] = i
    
    return lookup_dictionary

## Write the file
