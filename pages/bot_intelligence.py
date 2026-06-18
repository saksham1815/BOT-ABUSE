import streamlit as st
from llm.ollama_client import ask_llm


def extract_pdf_content(file):

    import fitz
    import base64

    doc = fitz.open(stream=file.read(), filetype="pdf")

    text = ""
    images = []

    for page_num, page in enumerate(doc):

        # extract text
        page_text = page.get_text()

        text += f"\n\nPAGE {page_num+1}\n"
        text += page_text


        # extract images
        for img in page.get_images(full=True):

            xref = img[0]

            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]

            encoded = base64.b64encode(
                image_bytes
            ).decode()

            images.append(encoded)


    return text, images



def render(df, intel):


    st.title("Bot Intelligence Report Analyzer")


    uploaded = st.file_uploader(
        "Upload Bad Bot Report PDF",
        type=["pdf"]
    )


    if not uploaded:
        st.info(
            "Upload a bot report to analyze attack trends."
        )
        return



    if st.button("Analyze Report"):


        with st.spinner(
            "Analyzing bot intelligence..."
        ):


            text, images = extract_pdf_content(
                uploaded
            )


            prompt = f"""

You are a bot security analyst.

Use the provided Bad Bot Report content.

Identify:

1. Common bot attack patterns
2. Bot techniques being used
3. Detection indicators
4. Customer risks
5. Recommended security controls
6. Actions organizations should implement

Focus on practical security recommendations.

Report text:

{text[:30000]}


Return:

Attack Patterns:
-

Detection Strategy:
-

Customer Actions:
-

Recommended Controls:
-

"""


            result = ask_llm(prompt)


            st.markdown(result)