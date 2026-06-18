import pandas as pd


def endpoint_risk():
    return pd.DataFrame([
        ["/login",92,"Critical"],
        ["/checkout",71,"High"],
        ["/search",44,"Medium"],
        ["/api/cart",31,"Low"],
    ], columns=["endpoint","score","severity"])


def trust_score(device, typing, mouse):
    return round((device + typing + mouse) / 3, 1)