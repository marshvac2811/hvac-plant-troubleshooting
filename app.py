"""
app.py — HVAC Plant Troubleshooting Tool
Run locally: python app.py  →  http://127.0.0.1:5008
"""
from flask import Flask, render_template, request
import knowledge_base as kb
import diagnostic_rules as dr

app = Flask(__name__)


@app.route("/", methods=["GET"])
def browse():
    equipment_key = request.args.get("equipment", "chiller")
    symptom_key = request.args.get("symptom", "")

    equipment = kb.EQUIPMENT.get(equipment_key)
    symptom = None
    if equipment and symptom_key:
        symptom = equipment["symptoms"].get(symptom_key)

    return render_template(
        "browse.html",
        all_equipment=kb.EQUIPMENT,
        equipment_key=equipment_key,
        equipment=equipment,
        symptom_key=symptom_key,
        symptom=symptom,
        active="browse",
    )


@app.route("/diagnose", methods=["GET", "POST"])
def diagnose():
    result = None
    error = None
    selected_rule = request.values.get("rule_id", "chl_hp_trip")
    form_values = {}

    if request.method == "POST":
        selected_rule = request.form.get("rule_id", selected_rule)
        rule_def = dr.RULES.get(selected_rule)
        try:
            for inp in rule_def["inputs"]:
                form_values[inp["key"]] = request.form.get(inp["key"], "")
            result = dr.evaluate_rule(selected_rule, form_values)
        except (ValueError, KeyError, TypeError):
            error = "Please fill in all fields with valid values."

    return render_template(
        "diagnose.html",
        rules=dr.RULES,
        selected_rule=selected_rule,
        rule_def=dr.RULES.get(selected_rule),
        form_values=form_values,
        result=result,
        error=error,
        active="diagnose",
    )


@app.route("/priority")
def priority():
    return render_template("priority.html", priority_list=kb.FAULT_PRIORITY, active="priority")


@app.route("/sensor-check", methods=["GET", "POST"])
def sensor_check():
    results = []
    if request.method == "POST":
        for i, rule in enumerate(kb.SENSOR_VALIDATION_RULES):
            val_a = request.form.get(f"val_a_{i}", "")
            val_b = request.form.get(f"val_b_{i}", "")
            if val_a.strip() and val_b.strip():
                try:
                    a, b = float(val_a), float(val_b)
                    valid = a > b if rule["comparison"] == "greater" else None
                    results.append({"rule": rule, "val_a": a, "val_b": b, "valid": valid})
                except ValueError:
                    results.append({"rule": rule, "val_a": val_a, "val_b": val_b, "valid": None, "error": True})

    return render_template("sensor_check.html", validation_rules=kb.SENSOR_VALIDATION_RULES, results=results, active="sensor")


if __name__ == "__main__":
    app.run(debug=True, port=5008)
