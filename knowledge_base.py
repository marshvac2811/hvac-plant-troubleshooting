"""
knowledge_base.py — HVAC Plant Troubleshooting Knowledge Base

All diagnostic content in this module (symptoms, causes, required data,
recommended actions, and rule logic) was authored by a domain expert with
26+ years of HVAC/MEP field experience — not generated or invented by AI.
This module only structures that knowledge for lookup and evaluation.
"""

EQUIPMENT = {
    "chiller": {
        "label": "Chiller",
        "symptoms": {
            "chw_supply_high": {
                "label": "Chilled Water Supply Temperature High",
                "causes": [
                    {"cause": "Low refrigerant", "required_data": "Suction pressure, superheat",
                     "logic": "Low suction pressure + High superheat", "action": "Leak test, recharge refrigerant"},
                    {"cause": "Dirty condenser", "required_data": "Condenser approach temperature",
                     "logic": "Condenser approach > 5°C", "action": "Clean condenser tubes"},
                    {"cause": "Low condenser water flow", "required_data": "CW flow meter",
                     "logic": "Flow < design", "action": "Check pump/valves"},
                    {"cause": "Compressor inefficient", "required_data": "Compressor amps, COP",
                     "logic": "Normal load + High power", "action": "Service compressor"},
                    {"cause": "Evaporator fouling", "required_data": "Evaporator approach",
                     "logic": "Approach increasing over time", "action": "Clean evaporator"},
                    {"cause": "Excessive load", "required_data": "CHW return temp",
                     "logic": "Return temp much higher than design", "action": "Add capacity/load shedding"},
                ],
            },
            "high_pressure_trip": {
                "label": "High Pressure Trip",
                "causes": [
                    {"cause": "Dirty condenser", "required_data": "Condenser approach", "logic": "", "action": ""},
                    {"cause": "Cooling tower fan failed", "required_data": "Fan status", "logic": "", "action": ""},
                    {"cause": "Cooling tower water hot", "required_data": "CW entering temp", "logic": "", "action": ""},
                    {"cause": "Air in refrigerant", "required_data": "High discharge pressure", "logic": "", "action": ""},
                    {"cause": "Condenser water flow low", "required_data": "Flow meter", "logic": "", "action": ""},
                    {"cause": "Condenser valve closed", "required_data": "Valve position", "logic": "", "action": ""},
                ],
                "rule_id": "chl_hp_trip",
            },
            "low_pressure_trip": {
                "label": "Low Pressure Trip",
                "causes": [
                    {"cause": "Refrigerant leakage", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Low evaporator load", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Expansion valve stuck", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Frozen evaporator", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Low CHW flow", "required_data": "", "logic": "", "action": ""},
                ],
                "rule_id": "chl_lp_trip",
            },
            "poor_cop": {
                "label": "Poor COP",
                "causes": [
                    {"cause": "Dirty condenser", "required_data": "Power meter, cooling capacity, water temps, flow rate", "logic": "", "action": ""},
                    {"cause": "Dirty evaporator", "required_data": "Power meter, cooling capacity, water temps, flow rate", "logic": "", "action": ""},
                    {"cause": "High condenser temperature", "required_data": "Power meter, cooling capacity, water temps, flow rate", "logic": "", "action": ""},
                    {"cause": "Low load", "required_data": "Power meter, cooling capacity, water temps, flow rate", "logic": "", "action": ""},
                    {"cause": "Compressor wear", "required_data": "Power meter, cooling capacity, water temps, flow rate", "logic": "", "action": ""},
                ],
            },
        },
    },
    "ahu": {
        "label": "AHU",
        "symptoms": {
            "sat_high": {
                "label": "Supply Air Temperature Too High",
                "causes": [
                    {"cause": "CHW valve closed", "required_data": "Valve feedback", "logic": "Valve <20%", "action": ""},
                    {"cause": "No chilled water", "required_data": "CHW flow", "logic": "Flow=0", "action": ""},
                    {"cause": "Dirty cooling coil", "required_data": "Coil ΔT", "logic": "Low air temp drop", "action": ""},
                    {"cause": "Fan speed low", "required_data": "VFD speed", "logic": "RPM below setpoint", "action": ""},
                    {"cause": "Mixed air damper open", "required_data": "Damper position", "logic": "Outside air too high", "action": ""},
                    {"cause": "Sensor calibration", "required_data": "Compare sensors", "logic": "Difference >2°C", "action": ""},
                ],
            },
            "low_airflow": {
                "label": "Low Airflow",
                "causes": [
                    {"cause": "Dirty filters", "required_data": "Filter differential pressure", "logic": "", "action": ""},
                    {"cause": "Belt slipping", "required_data": "Fan RPM", "logic": "", "action": ""},
                    {"cause": "Damper closed", "required_data": "Damper feedback", "logic": "", "action": ""},
                    {"cause": "Fan VFD issue", "required_data": "Frequency", "logic": "", "action": ""},
                    {"cause": "Fan rotating wrong direction", "required_data": "RPM + Airflow", "logic": "", "action": ""},
                ],
                "rule_id": "ahu_dirty_filter",
            },
            "high_humidity": {
                "label": "High Humidity",
                "causes": [
                    {"cause": "CHW valve not opening", "required_data": "RH sensor, supply air temp, coil temp, valve %", "logic": "", "action": ""},
                    {"cause": "Coil not cold enough", "required_data": "RH sensor, supply air temp, coil temp, valve %", "logic": "", "action": ""},
                    {"cause": "Fan too fast", "required_data": "RH sensor, supply air temp, coil temp, valve %", "logic": "", "action": ""},
                    {"cause": "Fresh air too much", "required_data": "RH sensor, supply air temp, coil temp, valve %", "logic": "", "action": ""},
                    {"cause": "Coil dirty", "required_data": "RH sensor, supply air temp, coil temp, valve %", "logic": "", "action": ""},
                ],
            },
            "water_leakage": {
                "label": "Water Leakage",
                "causes": [
                    {"cause": "Drain blocked", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Drain trap broken", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Frozen coil", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Coil sweating", "required_data": "", "logic": "", "action": ""},
                ],
                "rule_id": "ahu_water_leak",
            },
            "fan_not_running": {
                "label": "Fan Not Running",
                "causes": [
                    {"cause": "MCC Trip", "required_data": "MCC status, VFD fault code, fire alarm, motor current", "logic": "", "action": ""},
                    {"cause": "VFD Fault", "required_data": "MCC status, VFD fault code, fire alarm, motor current", "logic": "", "action": ""},
                    {"cause": "Fire alarm interlock", "required_data": "MCC status, VFD fault code, fire alarm, motor current", "logic": "", "action": ""},
                    {"cause": "Motor overload", "required_data": "MCC status, VFD fault code, fire alarm, motor current", "logic": "", "action": ""},
                    {"cause": "Broken coupling", "required_data": "MCC status, VFD fault code, fire alarm, motor current", "logic": "", "action": ""},
                ],
            },
        },
    },
    "pump": {
        "label": "Chilled Water Pump",
        "symptoms": {
            "not_starting": {
                "label": "Pump Not Starting",
                "causes": [
                    {"cause": "MCC Trip", "required_data": "Breaker", "logic": "", "action": ""},
                    {"cause": "Overload", "required_data": "Relay", "logic": "", "action": ""},
                    {"cause": "VFD Fault", "required_data": "Alarm", "logic": "", "action": ""},
                    {"cause": "Local mode", "required_data": "HOA switch", "logic": "", "action": ""},
                    {"cause": "BMS command absent", "required_data": "Command", "logic": "", "action": ""},
                ],
                "rule_id": "pump_motor_fault",
            },
            "low_flow": {
                "label": "Low Flow",
                "causes": [
                    {"cause": "Air lock", "required_data": "Flow meter, pressure sensors, VFD frequency", "logic": "", "action": ""},
                    {"cause": "Strainer blocked", "required_data": "Flow meter, pressure sensors, VFD frequency", "logic": "", "action": ""},
                    {"cause": "Impeller damaged", "required_data": "Flow meter, pressure sensors, VFD frequency", "logic": "", "action": ""},
                    {"cause": "Valve closed", "required_data": "Flow meter, pressure sensors, VFD frequency", "logic": "", "action": ""},
                    {"cause": "Pump speed low", "required_data": "Flow meter, pressure sensors, VFD frequency", "logic": "", "action": ""},
                ],
            },
            "low_dp": {
                "label": "Low Differential Pressure",
                "causes": [
                    {"cause": "Pump wear", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Pipe leakage", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Bypass valve open", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Air in line", "required_data": "", "logic": "", "action": ""},
                ],
                "rule_id": "pump_bypass_open",
            },
            "high_motor_current": {
                "label": "High Motor Current",
                "causes": [
                    {"cause": "Bearing failure", "required_data": "Current, vibration, temperature", "logic": "", "action": ""},
                    {"cause": "Impeller jam", "required_data": "Current, vibration, temperature", "logic": "", "action": ""},
                    {"cause": "Misalignment", "required_data": "Current, vibration, temperature", "logic": "", "action": ""},
                    {"cause": "High flow", "required_data": "Current, vibration, temperature", "logic": "", "action": ""},
                ],
            },
            "cavitation": {
                "label": "Cavitation",
                "causes": [
                    {"cause": "Low suction pressure", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Air entering suction", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Low water level", "required_data": "", "logic": "", "action": ""},
                    {"cause": "High water temperature", "required_data": "", "logic": "", "action": ""},
                ],
                "rule_id": "pump_cavitation",
            },
        },
    },
    "cooling_tower": {
        "label": "Cooling Tower",
        "symptoms": {
            "cw_temp_high": {
                "label": "CW Temperature High",
                "causes": [
                    {"cause": "Fan failure", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Fill dirty", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Pump low flow", "required_data": "", "logic": "", "action": ""},
                    {"cause": "Drift eliminator blocked", "required_data": "", "logic": "", "action": ""},
                ],
            },
            "tower_overflow": {
                "label": "Tower Overflow",
                "causes": [
                    {"cause": "Float valve failure", "required_data": "", "logic": "", "action": ""},
                ],
            },
            "basin_low_level": {
                "label": "Basin Low Level",
                "causes": [
                    {"cause": "Leakage", "required_data": "", "logic": "", "action": ""},
                ],
            },
        },
    },
}

FAULT_PRIORITY = [
    {"priority": "Critical", "fault": "High Pressure Trip"},
    {"priority": "Critical", "fault": "Low Pressure Trip"},
    {"priority": "Critical", "fault": "Pump Failure"},
    {"priority": "Critical", "fault": "Compressor Failure"},
    {"priority": "High", "fault": "No CHW Flow"},
    {"priority": "High", "fault": "Cooling Tower Failure"},
    {"priority": "High", "fault": "AHU Fan Failure"},
    {"priority": "Medium", "fault": "Dirty Filter"},
    {"priority": "Medium", "fault": "Dirty Coil"},
    {"priority": "Medium", "fault": "Valve Failure"},
    {"priority": "Low", "fault": "Sensor Drift"},
    {"priority": "Low", "fault": "Calibration Error"},
]

SENSOR_VALIDATION_RULES = [
    {"label": "Return Air Temp vs Supply Air Temp", "rule": "Return Air Temp must be > Supply Air Temp",
     "field_a": "Return Air Temp", "field_b": "Supply Air Temp", "comparison": "greater"},
    {"label": "CHW Return Temp vs CHW Supply Temp", "rule": "CHW Return Temp must be > CHW Supply Temp",
     "field_a": "CHW Return Temp", "field_b": "CHW Supply Temp", "comparison": "greater"},
    {"label": "Condenser Water Leaving vs Entering", "rule": "Condenser Water Leaving must be > Entering Water",
     "field_a": "Condenser Water Leaving", "field_b": "Condenser Water Entering", "comparison": "greater"},
]
