def decision_engine(predicted_demand, station_capacity):
    """
    Decision Intelligence Engine
    ----------------------------
    Input:
    - predicted_demand (float): forecasted EV demand (kWh)
    - station_capacity (float): max capacity of station (kWh)

    Output:
    - decision (dict): structured decision output
    """

    utilization = predicted_demand / station_capacity

    decision = {
        "predicted_demand": round(predicted_demand, 2),
        "capacity": station_capacity,
        "utilization_ratio": round(utilization, 2),
        "risk_level": None,
        "action": None
    }

    # Decision rules
    if utilization < 0.7:
        decision["risk_level"] = "LOW"
        decision["action"] = "Normal operation"

    elif 0.7 <= utilization < 1.0:
        decision["risk_level"] = "MEDIUM"
        decision["action"] = "Monitor load and prepare mitigation"

    else:
        decision["risk_level"] = "HIGH"
        decision["action"] = (
            "Shift charging to off-peak hours or "
            "redistribute load to nearby stations"
        )

    return decision
