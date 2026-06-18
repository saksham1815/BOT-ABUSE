import pandas as pd


def find_col(df, options):
    """
    Return first matching column name.
    """
    cols = {c.lower(): c for c in df.columns}

    for opt in options:
        if opt.lower() in cols:
            return cols[opt.lower()]

    return None


def load_logs(file):
    df = pd.read_csv(file)

    # Clean headers
    df.columns = [c.strip() for c in df.columns]

    # --------------------------
    # REQUESTS / VOLUME
    # --------------------------
    req_col = find_col(df, [
        "requests",
        "request_count",
        "hits",
        "count",
        "pagehitcount",
        "totalhitcount",
        "visits",
        "events"
    ])

    if req_col:
        df["requests"] = pd.to_numeric(df[req_col], errors="coerce").fillna(1)
    else:
        df["requests"] = 1

    # --------------------------
    # PATH / URL
    # --------------------------
    path_col = find_col(df, [
        "path",
        "url",
        "uri",
        "endpoint",
        "request_uri",
        "page",
        "resource"
    ])

    if path_col:
        df["path"] = df[path_col].astype(str)
    else:
        df["path"] = "/"

    # --------------------------
    # STATUS CODE
    # --------------------------
    status_col = find_col(df, [
        "status",
        "status_code",
        "response_code",
        "http_status",
        "requestresult"
    ])

    if status_col:
        if status_col.lower() == "requestresult":
            df["status"] = df[status_col].map({
                "ALLOWED": 200,
                "BLOCKED": 403,
                "CHALLENGED": 429
            }).fillna(200)
        else:
            df["status"] = pd.to_numeric(df[status_col], errors="coerce").fillna(200)
    else:
        df["status"] = 200

    # --------------------------
    # USER AGENT
    # --------------------------
    ua_col = find_col(df, [
        "user_agent",
        "useragent",
        "ua",
        "agent",
        "browser"
    ])

    if ua_col:
        df["user_agent"] = df[ua_col].astype(str)
    else:
        df["user_agent"] = "Unknown"

    # --------------------------
    # GEO LOCATION
    # --------------------------
    geo_col = find_col(df, [
        "geo_location",
        "country",
        "countrycode",
        "city",
        "region",
        "location"
    ])

    if geo_col:
        df["geo_location"] = df[geo_col].astype(str)
    else:
        df["geo_location"] = "Unknown"

    # --------------------------
    # TIMESTAMP
    # --------------------------
    time_col = find_col(df, [
        "timestamp",
        "time",
        "datetime",
        "date",
        "requesttime",
        "requeststarttime"
    ])

    if time_col:
        df["timestamp"] = df[time_col]
    else:
        df["timestamp"] = pd.Timestamp.now()

    # --------------------------
    # IP ADDRESS
    # --------------------------
    ip_col = find_col(df, [
        "ip",
        "clientip",
        "clientipex",
        "source_ip",
        "remote_addr",
        "xforwardedfor"
    ])

    if ip_col:
        df["ip"] = df[ip_col].astype(str)
    else:
        df["ip"] = "0.0.0.0"

    return df