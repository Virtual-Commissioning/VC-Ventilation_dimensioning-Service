import json
from component_checker import *

## Return json with success or errors

def return_success_json():
    success_json = {"status": "sucessfully_parsed"}
    return success_json

## Write function to loop through each ventilation component

def check_ventilation_components(data):
    ventilation_components = data["system"]["SubSystems"]["ventilation"]

    for ventilation_component in ventilation_components:
        component_type = ventilation_component["ComponentType"] 
        
        if  component_type == "AirTerminal":
            check_air_terminal(ventilation_component)

        elif component_type == "FlowSegment":
            check_flow_segment(ventilation_component)
        
        elif component_type == "MotorizedDamper":
            check_motorized_damper(ventilation_component)

        elif component_type == "FireDamper":
            check_fire_damper(ventilation_component)
        
        elif component_type == "BalancingDamper":
            check_balancing_damper(ventilation_component)
        
        elif component_type == "Bend":
            check_bend(ventilation_component)
        
        elif component_type == "Tee":
            check_tee(ventilation_component)

        elif component_type == "Reduction":
            check_reduction(ventilation_component)

        elif component_type == "Cross":
            check_cross(ventilation_component)
        
        elif component_type == "HeatExchanger":
            check_heat_exchanger(ventilation_components, ventilation_component)

        elif component_type == "Fan":
            check_fan(ventilation_component)
        

## Write function to loop through each heating component

def check_heating_components(data):
    heating_components = data["system"]["SubSystems"]["heating"]

    for heating_component in heating_components:
        component_type = heating_component["ComponentType"] 

        if component_type == "FlowSegment":
            check_flow_segment(heating_component)
        
        elif component_type == "Bend":
            check_bend(heating_component)
        
        elif component_type == "Tee":
            check_tee(heating_component)
        
        elif component_type == "Cross":
            check_cross(heating_component)

        elif component_type == "Reduction":
            check_reduction(heating_component)
        
        elif component_type == "HeatExchanger":
            check_heat_exchanger(heating_components, heating_component)

        elif component_type == "Radiator":
            check_radiator(heating_component)

        elif component_type == "Pump":
            check_pump(heating_component)

        elif component_type == "BalancingValve":
            check_balancing_valve(heating_component)
        
        elif component_type == "CheckValve":
            check_check_valve(heating_component)
            
        elif component_type == "DifferentialPressureValve":
            check_differential_pressure_valve(heating_component)
            
        elif component_type == "MotorizedValve":
            check_motorized_valve(heating_component)
            
        elif component_type == "SafetyValve":
            check_safety_valve(heating_component)
        
        elif component_type == "ShuntValve":
            check_shunt_valve(heating_component)


## Write function to loop through each cooling component

def check_cooling_components(data):
    cooling_components = data["system"]["SubSystems"]["cooling"]

    for cooling_component in cooling_components:
        component_type = cooling_component["ComponentType"] 

        if component_type == "FlowSegment":
            check_flow_segment(cooling_component)
        
        elif component_type == "Bend":
            check_bend(cooling_component)
        
        elif component_type == "Tee":
            check_tee(cooling_component)
        
        elif component_type == "Cross":
            check_cross(cooling_component)

        elif component_type == "Reduction":
            check_reduction(cooling_component)
        
        elif component_type == "HeatExchanger":
            check_heat_exchanger(cooling_components, cooling_component)

        elif component_type == "Radiator":
            check_radiator(cooling_component)

        elif component_type == "Pump":
            check_pump(cooling_component)

        elif component_type == "BalancingValve":
            check_balancing_valve(cooling_component)
        
        elif component_type == "CheckValve":
            check_check_valve(cooling_component)
            
        elif component_type == "DifferentialPressureValve":
            check_differential_pressure_valve(cooling_component)
            
        elif component_type == "MotorizedValve":
            check_motorized_valve(cooling_component)
            
        elif component_type == "SafetyValve":
            check_safety_valve(cooling_component)
        
        elif component_type == "ShuntValve":
            check_shunt_valve(cooling_component)

## Write the file
