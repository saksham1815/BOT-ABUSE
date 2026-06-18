import streamlit as st

from llm.ollama_client import ask_llm

from llm.prompts import (
    rule_generation_prompt,
    moi_validation_prompt
)


def render(df, intel):

    st.title("MOI Rule Assistant")

    # =====================================================
    # LOAD MOI REFERENCE FILES
    # =====================================================

    moi = ""
    rules = ""

    try:

        with open("docs/moi.txt", "r", encoding="utf-8") as f:
            moi = f.read()

        with open("docs/rules.txt", "r", encoding="utf-8") as f:
            rules = f.read()

    except:
        st.warning("MOI reference files not found")

    # =====================================================
    # MODE TOGGLE
    # =====================================================

    mode = st.toggle(
        "Validation Mode",
        value=False
    )

    st.divider()

    # =====================================================
    # GENERATION MODE
    # =====================================================

    if not mode:

        st.subheader("Rule Generation")

        prompt = st.text_area(
            "Describe the protection logic",
            height=180,
            placeholder="""Examples:
- Create ATO protection for login APIs
- Detect scraping on pricing pages
- Protect checkout from automation
- Block suspicious POST login requests
"""
        )

        # =================================================
        # LOG SUMMARY
        # =================================================

        log_summary = f"""
Traffic Summary

Total Requests:
{intel['total_requests']}

Login Requests:
{intel['login_requests']}

Scraping Requests:
{intel['scraping_requests']}

Ticketing Requests:
{intel['ticket_requests']}

Alerts:
{len(intel['alerts'])}

Top URLs:
{', '.join(df['url'].astype(str).head(10).tolist()) if 'url' in df.columns else 'N/A'}

Top User Agents:
{', '.join(df['useragent'].astype(str).head(10).tolist()) if 'useragent' in df.columns else 'N/A'}
"""

        if st.button("Generate Rule"):

            with st.spinner("Generating MOI rule..."):

                final_prompt = rule_generation_prompt(
                    prompt,
                    moi,
                    rules,
                    log_summary
                )

                result = ask_llm(final_prompt)

            st.subheader("Generated Rule")

            st.code(
                result,
                language="lisp"
            )

            st.download_button(
                "Download Rule",
                result,
                file_name="generated_rule.txt"
            )

    # =====================================================
    # VALIDATION MODE
    # =====================================================

    else:

        st.subheader("Rule Validation")

        rule_text = st.text_area(
            "Paste MOI Rule",
            height=280,
            placeholder="""Example:

(all
  apollo.heavy_scraper_v4_high_account

  (any
    (geo_country_code != "US")
    (request.method == "POST")
  )

  (not
    (matches client_platform "android" "ios")
  )
)
"""
        )

        st.info("""
Supported MOI Logic:

• any
(any a b c)
→ true if ANY condition matches

• all
(all a b c)
→ true if ALL conditions match

• not
(not expression)
→ negates the condition
""")

        if st.button("Validate Rule"):

            if not rule_text.strip():
                st.error("Please paste a rule")
                st.stop()

            with st.spinner("Validating MOI rule..."):

                validation_prompt = moi_validation_prompt(
                    rule_text,
                    moi,
                    rules
                )

                result = ask_llm(validation_prompt)

            st.subheader("Validation Result")

            st.markdown(result)

            # =============================================
            # LOCAL VALIDATIONS
            # =============================================

            errors = []

            # bracket validation
            open_brackets = rule_text.count("(")
            close_brackets = rule_text.count(")")

            if open_brackets != close_brackets:
                errors.append(
                    "Bracket mismatch detected"
                )

            # unsupported keywords
            invalid_keywords = [
                "if",
                "then",
                "else",
                "&&",
                "||"
            ]

            for keyword in invalid_keywords:

                if keyword in rule_text.lower():
                    errors.append(
                        f"Unsupported keyword/operator detected: {keyword}"
                    )

            # ensure logic exists
            allowed_keywords = [
                "all",
                "any",
                "not"
            ]

            contains_logic = any(
                f"({k}" in rule_text
                for k in allowed_keywords
            )

            if not contains_logic:
                errors.append(
                    "No valid MOI logical operators found"
                )

            st.divider()

            if errors:

                st.error("Validation Failed")

                for e in errors:
                    st.write(f"• {e}")

            else:

                st.success(
                    "Rule structure appears valid"
                )

            st.code(
                rule_text,
                language="lisp"
            )