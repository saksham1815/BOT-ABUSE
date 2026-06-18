INDUSTRY = {
    "bot_block_rate": 0.82,
    "ato_success_rate": 0.015,
    "scraping_loss_pct": 0.03,
}


def compare(metric, value):
    baseline = INDUSTRY.get(metric)
    if baseline is None:
        return "No benchmark"
    if value >= baseline:
        return "Above benchmark"
    return "Below benchmark"