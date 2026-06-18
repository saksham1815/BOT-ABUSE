def recommend(roi_ratio, ato_score, scraping_score, ticket_score):
    recs = []
    if roi_ratio > 1:
        recs.append("Deploy immediately: projected ROI exceeds 100%.")
    if ato_score > 70:
        recs.append("Enable MFA, velocity checks, device fingerprinting.")
    if scraping_score > 60:
        recs.append("Deploy JS challenges, API schema validation, rotating defenses.")
    if ticket_score > 60:
        recs.append("Use queueing, session integrity, purchase limits.")
    if not recs:
        recs.append("Maintain controls and continue monitoring.")
    return recs