from dataclasses import dataclass

@dataclass
class ROIResult:
    annual_savings: float
    tool_cost: float
    net_roi: float
    roi_ratio: float
    payback_months: float


def calculate_roi(annual_savings: float, tool_cost: float) -> ROIResult:
    net = annual_savings - tool_cost
    ratio = net / tool_cost if tool_cost else 0
    payback = (tool_cost / max(annual_savings,1)) * 12
    return ROIResult(annual_savings, tool_cost, net, ratio, payback)


def ato_savings(login_attempts, attack_rate, success_rate, fraud_loss, support_cost):
    compromised = login_attempts * attack_rate * success_rate
    return compromised * (fraud_loss + support_cost)