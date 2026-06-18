
def simulate(base_attacks, multiplier, mitigation_gain, tool_cost):
    attacks = base_attacks * multiplier
    prevented = attacks * mitigation_gain
    savings = prevented * 5
    roi = savings - tool_cost
    return {
        "attacks": attacks,
        "prevented": prevented,
        "savings": savings,
        "net_roi": roi
    }