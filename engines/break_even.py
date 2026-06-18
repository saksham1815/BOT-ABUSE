def max_vendor_spend(annual_savings):
    return annual_savings


def min_mitigation_needed(attacks, value_per_attack, tool_cost):
    return tool_cost / max(attacks * value_per_attack, 1)


def min_attack_volume(tool_cost, mitigation_rate, value_per_attack):
    return tool_cost / max(mitigation_rate * value_per_attack, 1)