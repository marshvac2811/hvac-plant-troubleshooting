"""
diagnostic_rules.py — Interactive Rule-Based Diagnostic Engine

Implements the 7 explicit, quantifiable diagnostic rules from the domain
expert's knowledge base — each rule is an AND-condition that, when all
inputs are true, points to a specific likely fault. These rules are
transcribed exactly as specified; this module only evaluates them.
"""

RULES = {
    "chl_hp_trip": {
        "label": "Chiller — High Pressure Trip",
        "description": "IF Discharge Pressure > HP Limit AND CW Entering Temp > 33°C THEN Cooling Tower Performance Poor",
        "inputs": [
            {"key": "discharge_pressure", "label": "Discharge Pressure (bar)", "type": "number"},
            {"key": "hp_limit", "label": "HP Trip Limit (bar)", "type": "number"},
            {"key": "cw_entering_temp", "label": "CW Entering Temperature (°C)", "type": "number"},
        ],
        "conclusion": "Cooling Tower Performance Poor",
    },
    "chl_lp_trip": {
        "label": "Chiller — Low Pressure Trip",
        "description": "Low suction pressure + Low evaporator pressure + High superheat → Likely refrigerant shortage",
        "inputs": [
            {"key": "suction_pressure_low", "label": "Suction Pressure Low?", "type": "bool"},
            {"key": "evap_pressure_low", "label": "Evaporator Pressure Low?", "type": "bool"},
            {"key": "superheat_high", "label": "Superheat High?", "type": "bool"},
        ],
        "conclusion": "Likely Refrigerant Shortage",
    },
    "ahu_dirty_filter": {
        "label": "AHU — Low Airflow",
        "description": "DP Filter > Threshold AND Fan Speed Normal → Dirty Filter",
        "inputs": [
            {"key": "filter_dp", "label": "Filter Differential Pressure (Pa)", "type": "number"},
            {"key": "filter_dp_threshold", "label": "Filter DP Threshold (Pa)", "type": "number"},
            {"key": "fan_speed_normal", "label": "Fan Speed Normal?", "type": "bool"},
        ],
        "conclusion": "Dirty Filter",
    },
    "ahu_water_leak": {
        "label": "AHU — Water Leakage",
        "description": "Water Leak Sensor = ON AND Drain DP High → Drain Blockage",
        "inputs": [
            {"key": "leak_sensor_on", "label": "Water Leak Sensor ON?", "type": "bool"},
            {"key": "drain_dp_high", "label": "Drain DP High?", "type": "bool"},
        ],
        "conclusion": "Drain Blockage",
    },
    "pump_motor_fault": {
        "label": "Pump — Not Starting",
        "description": "Start Command AND Breaker ON AND No Current → Motor Fault",
        "inputs": [
            {"key": "start_command", "label": "Start Command Given?", "type": "bool"},
            {"key": "breaker_on", "label": "Breaker ON?", "type": "bool"},
            {"key": "no_current", "label": "No Current Drawn?", "type": "bool"},
        ],
        "conclusion": "Motor Fault",
    },
    "pump_bypass_open": {
        "label": "Pump — Low Differential Pressure",
        "description": "Flow Normal AND DP Low → Bypass Valve Open",
        "inputs": [
            {"key": "flow_normal", "label": "Flow Normal?", "type": "bool"},
            {"key": "dp_low", "label": "Differential Pressure Low?", "type": "bool"},
        ],
        "conclusion": "Bypass Valve Open",
    },
    "pump_cavitation": {
        "label": "Pump — Cavitation",
        "description": "High Vibration AND Noise AND Low Suction Pressure → Cavitation",
        "inputs": [
            {"key": "high_vibration", "label": "High Vibration?", "type": "bool"},
            {"key": "noise", "label": "Unusual Noise?", "type": "bool"},
            {"key": "low_suction_pressure", "label": "Low Suction Pressure?", "type": "bool"},
        ],
        "conclusion": "Cavitation",
    },
}


def evaluate_rule(rule_id: str, values: dict) -> dict:
    if rule_id not in RULES:
        raise ValueError(f"Unknown rule: {rule_id}")

    rule = RULES[rule_id]
    conditions_met = []
    all_true = True

    if rule_id == "chl_hp_trip":
        discharge_pressure = float(values["discharge_pressure"])
        hp_limit = float(values["hp_limit"])
        cw_entering_temp = float(values["cw_entering_temp"])
        cond1 = discharge_pressure > hp_limit
        cond2 = cw_entering_temp > 33
        conditions_met = [
            (f"Discharge Pressure ({discharge_pressure}) > HP Limit ({hp_limit})", cond1),
            (f"CW Entering Temp ({cw_entering_temp}°C) > 33°C", cond2),
        ]
        all_true = cond1 and cond2

    elif rule_id in ("chl_lp_trip", "ahu_water_leak", "pump_bypass_open", "pump_cavitation", "pump_motor_fault", "ahu_dirty_filter"):
        if rule_id == "ahu_dirty_filter":
            filter_dp = float(values["filter_dp"])
            threshold = float(values["filter_dp_threshold"])
            fan_normal = values["fan_speed_normal"] == "yes"
            cond1 = filter_dp > threshold
            conditions_met = [
                (f"Filter DP ({filter_dp} Pa) > Threshold ({threshold} Pa)", cond1),
                ("Fan Speed Normal", fan_normal),
            ]
            all_true = cond1 and fan_normal
        else:
            # All boolean-input rules: every input must be "yes" for the rule to fire
            bool_inputs = [inp for inp in rule["inputs"] if inp["type"] == "bool"]
            for inp in bool_inputs:
                is_true = values.get(inp["key"]) == "yes"
                conditions_met.append((inp["label"], is_true))
            all_true = all(met for _, met in conditions_met)

    return {
        "rule_label": rule["label"],
        "description": rule["description"],
        "conditions_met": conditions_met,
        "all_conditions_met": all_true,
        "conclusion": rule["conclusion"] if all_true else None,
    }
