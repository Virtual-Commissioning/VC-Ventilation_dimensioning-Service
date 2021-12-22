def faulty_component(component):
    return {component["Tag"] : False}


def correct_component(component):
    return {component["Tag"]: True}


def has_in_and_out_connector(component):
    connectors = component["ConnectedWith"]
    has_supplies_fluid_from = False
    has_supplies_fluid_to = False

    for connector in connectors:

        if connector["ConnectorType"] == "suppliesFluidTo":
            has_supplies_fluid_to = True
        
        if connector["ConnectorType"] == "suppliesFluidFrom":
            has_supplies_fluid_from = True
        
        if connector["Tag"] == "Not connected":
            return False
    
    if has_supplies_fluid_from and has_supplies_fluid_to:
        return True
    
    else: 
        return False


def is_contained_in_two_systems(subsystem, component):
    connectors = component["ConnectedWith"]
    is_in_other_subsystem = False

    for connector in connectors:
        if connector["Tag"] not in subsystem:
            is_in_other_subsystem == True
    
    return False


def check_air_terminal(air_terminal):
    connectors = air_terminal["ConnectedWith"]

    if len(connectors) != 1:
        return faulty_component(air_terminal)

    return correct_component(air_terminal)


def check_flow_segment(flow_segment):
    connectors = flow_segment["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(flow_segment)
    
    if not has_in_and_out_connector(flow_segment):
        return faulty_component(flow_segment)
    
    return correct_component(flow_segment)


def check_motorized_damper(motorized_damper):
    connectors = motorized_damper["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(motorized_damper)

    if not has_in_and_out_connector(motorized_damper):
        return faulty_component(motorized_damper)
    
    return correct_component(motorized_damper)


def check_fire_damper(fire_damper):
    connectors = fire_damper["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(fire_damper)

    if not has_in_and_out_connector(fire_damper):
        return faulty_component(fire_damper)
    
    return correct_component(fire_damper)


def check_balancing_damper(balancing_damper):
    connectors = balancing_damper["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(balancing_damper)

    if not has_in_and_out_connector(balancing_damper):
        return faulty_component(balancing_damper)
    
    return correct_component(balancing_damper)


def check_bend(bend):
    connectors = bend["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(bend)

    if not has_in_and_out_connector(bend):
        return faulty_component(bend)
    
    if bend["Angle"] <= 0:
        return faulty_component(bend)
    
    return correct_component(bend)


def check_tee(tee):
    connectors = tee["ConnectedWith"]

    if len(connectors) != 3:
        return faulty_component(tee)
    
    if not has_in_and_out_connector(tee):
        return faulty_component(tee)
    
    return correct_component(tee)


def check_reduction(reduction):
    connectors = reduction["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(reduction)
    
    if not has_in_and_out_connector(reduction):
        return faulty_component(reduction)
    
    return correct_component(reduction)


def check_cross(cross):
    connectors = cross["ConnectedWith"]

    if len(connectors) != 4:
        return faulty_component(cross)
    
    if not has_in_and_out_connector(cross):
        return faulty_component(cross)
    
    return correct_component(cross)


def check_heat_exchanger(subsystem, heat_exchanger):
    connectors = heat_exchanger["ConnectedWith"]

    if len(connectors) != 4:
        return faulty_component(heat_exchanger)
    
    if not has_in_and_out_connector(heat_exchanger):
        return faulty_component(heat_exchanger)

    # if not is_contained_in_two_systems(subsystem, heat_exchanger):
    #     return faulty_component(heat_exchanger)
    
    return correct_component(heat_exchanger)


def check_fan(fan):
    connectors = fan["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(fan)
    
    if not has_in_and_out_connector(fan):
        return faulty_component(fan)
    
    return correct_component(fan)


def check_pump(fan):
    connectors = fan["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(fan)
    
    if not has_in_and_out_connector(fan):
        return faulty_component(fan)
    
    return correct_component(fan)


def check_radiator(radiator): 
    connectors = radiator["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(radiator)
    
    if not has_in_and_out_connector(radiator):
        return faulty_component(radiator)
    
    return correct_component(radiator)


def check_balancing_valve(balancing_valve):
    connectors = balancing_valve["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(balancing_valve)
    
    if not has_in_and_out_connector(balancing_valve):
        return faulty_component(balancing_valve)
    
    return correct_component(balancing_valve)


def check_check_valve(check_valve):
    connectors = check_valve["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(check_valve)
    
    if not has_in_and_out_connector(check_valve):
        return faulty_component(check_valve)
    
    return correct_component(check_valve)


def check_differential_pressure_valve(differential_pressure_valve):
    connectors = differential_pressure_valve["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(differential_pressure_valve)
    
    if not has_in_and_out_connector(differential_pressure_valve):
        return faulty_component(differential_pressure_valve)
    
    return correct_component(differential_pressure_valve)


def check_motorized_valve(motorized_valve):
    connectors = motorized_valve["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(motorized_valve)
    
    if not has_in_and_out_connector(motorized_valve):
        return faulty_component(motorized_valve)
    
    return correct_component(motorized_valve)


def check_safety_valve(safety_valve):
    connectors = safety_valve["ConnectedWith"]

    if len(connectors) != 2:
        return faulty_component(safety_valve)
    
    if not has_in_and_out_connector(safety_valve):
        return faulty_component(safety_valve)
    
    return correct_component(safety_valve)


def check_shunt_valve(shunt_valve):
    connectors = shunt_valve["ConnectedWith"]

    if len(connectors) != 4:
        return faulty_component(shunt_valve)
    
    if not has_in_and_out_connector(shunt_valve):
        return faulty_component(shunt_valve)
    
    return correct_component(shunt_valve)