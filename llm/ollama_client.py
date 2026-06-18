import requests

from core.config import (
    OLLAMA_URL,
    OLLAMA_MODEL
)


def ask_llm(prompt, mode="normal"):

    if not OLLAMA_URL:
        return """
LLM Error:
OLLAMA_URL is not configured.
"""

    if mode == "rules":

        temperature = 0.05
        predict = 600

    elif mode == "analysis":

        temperature = 0.2
        predict = 1200

    else:

        temperature = 0.1
        predict = 700

    payload = {

        "model": OLLAMA_MODEL,

        "prompt": prompt,

        "stream": False,

        "options": {

            "temperature": temperature,

            "top_p": 0.85,

            "top_k": 40,

            "num_predict": predict,

            "repeat_penalty": 1.15,

            "num_ctx": 12000,

            "seed": 42,

            "stop": [
                "END_RESPONSE",
                "###"
            ]
        }
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=600
        )

        response.raise_for_status()

        data = response.json()

        output = data.get(
            "response",
            ""
        )

        return output.strip()

    except requests.exceptions.ConnectionError:

        return f"""
Cannot connect to Ollama.

Configured URL:
{OLLAMA_URL}

Possible causes:
- Ollama is not running
- URL is incorrect
- Streamlit Cloud cannot access local Ollama
"""

    except requests.exceptions.Timeout:

        return """
LLM timeout.

Try:
- reduce input size
- increase Ollama resources
- use larger context model
"""

    except Exception as e:

        return f"LLM Error: {str(e)}"