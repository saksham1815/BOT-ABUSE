from core.config import ALERT_THRESHOLD


def frictionless_score(df):
    suspicious = df[df["user_agent"].str.contains(
        "bot|python|curl|scrapy|headless|playwright|selenium",
        case=False,
        na=False
    )]

    blocked = suspicious[suspicious["status"].isin([403, 429])]["requests"].sum()
    suspicious_total = suspicious["requests"].sum()

    legit = df[~df.index.isin(suspicious.index)]
    legit_total = legit["requests"].sum()

    legit_failed = legit[legit["status"].isin([403, 429, 401])]["requests"].sum()
    legit_success = legit[legit["status"] == 200]["requests"].sum()

    bot_block_rate = (blocked / suspicious_total * 100) if suspicious_total else 0
    human_friction = (legit_failed / legit_total * 100) if legit_total else 0
    ux_safety = (legit_success / legit_total * 100) if legit_total else 100

    score = (
        (0.50 * bot_block_rate) +
        (0.35 * ux_safety) -
        (0.15 * human_friction)
    )

    return round(max(0, min(score, 100)), 1)


def analyze_logs(df):
    alerts = []

    total = df["requests"].sum()

    login = df[df["path"].str.contains("/login|/signin|/auth", na=False)]["requests"].sum()

    scrape = df[df["path"].str.contains(
        "/pricing|/search|/catalog|/api/products",
        na=False
    )]["requests"].sum()

    ticket = df[df["path"].str.contains(
        "/buy|/checkout|/events|/cart",
        na=False
    )]["requests"].sum()

    if login > ALERT_THRESHOLD:
        alerts.append({
            "type": "ATO",
            "message": f"/login exceeded threshold ({login:,.0f})",
            "severity": "Critical"
        })

    if scrape > ALERT_THRESHOLD:
        alerts.append({
            "type": "Scraping",
            "message": f"Scraping endpoints exceeded threshold ({scrape:,.0f})",
            "severity": "High"
        })

    if ticket > ALERT_THRESHOLD:
        alerts.append({
            "type": "Ticketing",
            "message": f"Ticketing abuse surge ({ticket:,.0f})",
            "severity": "High"
        })

    geo = df.groupby("geo_location")["requests"].sum().reset_index()

    f_score = frictionless_score(df)

    return {
        "total_requests": total,
        "login_requests": login,
        "scraping_requests": scrape,
        "ticket_requests": ticket,
        "geo": geo,
        "alerts": alerts,
        "frictionless_score": f_score
    }