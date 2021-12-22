import json
from app.services.component_checker import *

## Write function to loop through each ventilation component

def check_ventilation_components(data):
    ventilation_components = data["system"]["SubSystems"]["ventilation"]["Components"]
    check_json = []

    for ventilation_component in ventilation_components:
        status_json = {}

        component_type = ventilation_component["ComponentType"]
        
        if  component_type == "AirTerminal":
            status_json = check_air_terminal(ventilation_component)

        elif component_type == "FlowSegment":
            status_json = check_flow_segment(ventilation_component)
            
        elif component_type == "MotorizedDamper":
            status_json = check_motorized_damper(ventilation_component)
        
        elif component_type == "FireDamper":
            status_json = check_fire_damper(ventilation_component)
            
        elif component_type == "BalancingDamper":
            status_json = check_balancing_damper(ventilation_component)
                    
        elif component_type == "Bend":
            status_json = check_bend(ventilation_component)
                    
        elif component_type == "Tee":
            status_json = check_tee(ventilation_component)
            
        elif component_type == "Reduction":
            status_json = check_reduction(ventilation_component)
            
        elif component_type == "Cross":
            status_json = check_cross(ventilation_component)
                    
        elif component_type == "HeatExchanger":
            status_json = check_heat_exchanger(ventilation_components, ventilation_component)
            
        elif component_type == "Fan":
            status_json = check_fan(ventilation_component)

        elif component_type == "PressureSensor":
            status_json = {ventilation_component["Tag"] : True}

        elif component_type == "TemperatureSensor":
            status_json = {ventilation_component["Tag"] : True}

        check_json.append(status_json)

    return check_json
        

## Write function to loop through each heating component

def check_heating_components(data):
    heating_components = data["system"]["SubSystems"]["heating"]["Components"]
    check_json = []

    for heating_component in heating_components:
        component_type = heating_component["ComponentType"] 

        if component_type == "FlowSegment":
            status_json = check_flow_segment(heating_component)
        
        elif component_type == "Bend":
            status_json = check_bend(heating_component)
        
        elif component_type == "Tee":
            status_json = check_tee(heating_component)
        
        elif component_type == "Cross":
            status_json = check_cross(heating_component)

        elif component_type == "Reduction":
            status_json = check_reduction(heating_component)
        
        elif component_type == "HeatExchanger":
            status_json = check_heat_exchanger(heating_components, heating_component)

        elif component_type == "Radiator":
            status_json = check_radiator(heating_component)

        elif component_type == "Pump":
            status_json = check_pump(heating_component)

        elif component_type == "BalancingValve":
            status_json = check_balancing_valve(heating_component)
        
        elif component_type == "CheckValve":
            status_json = check_check_valve(heating_component)
            
        elif component_type == "DifferentialPressureValve":
            status_json = check_differential_pressure_valve(heating_component)
            
        elif component_type == "MotorizedValve":
            status_json = check_motorized_valve(heating_component)
            
        elif component_type == "SafetyValve":
            status_json = check_safety_valve(heating_component)
        
        elif component_type == "ShuntValve":
            status_json = check_shunt_valve(heating_component)
        
        check_json.append(status_json)

    return check_json


## Write function to loop through each cooling component

def check_cooling_components(data):
    cooling_components = data["system"]["SubSystems"]["cooling"]["Components"]
    check_json = []

    for cooling_component in cooling_components:
        component_type = cooling_component["ComponentType"] 

        if component_type == "FlowSegment":
            status_json = check_flow_segment(cooling_component)
        
        elif component_type == "Bend":
            status_json = check_bend(cooling_component)
        
        elif component_type == "Tee":
            status_json = check_tee(cooling_component)
        
        elif component_type == "Cross":
            status_json = check_cross(cooling_component)

        elif component_type == "Reduction":
            status_json = check_reduction(cooling_component)
        
        elif component_type == "HeatExchanger":
            status_json = check_heat_exchanger(cooling_components, cooling_component)

        elif component_type == "Radiator":
            status_json = check_radiator(cooling_component)

        elif component_type == "Pump":
            status_json = check_pump(cooling_component)

        elif component_type == "BalancingValve":
            status_json = check_balancing_valve(cooling_component)
        
        elif component_type == "CheckValve":
            status_json = check_check_valve(cooling_component)
            
        elif component_type == "DifferentialPressureValve":
            status_json = check_differential_pressure_valve(cooling_component)
            
        elif component_type == "MotorizedValve":
            status_json = check_motorized_valve(cooling_component)
            
        elif component_type == "SafetyValve":
            status_json = check_safety_valve(cooling_component)
        
        elif component_type == "ShuntValve":
            status_json = check_shunt_valve(cooling_component)
        
        check_json.append(status_json)
    
    return check_json

## Write the file

def rule_checker(data):
    data = json.loads(data)
    ventilation_components_status = check_ventilation_components(data)
    heating_components_status = check_heating_components(data)
    cooling_components_status = check_cooling_components(data)

    status_json = ventilation_components_status + heating_components_status + cooling_components_status

    return json.dumps(status_json)