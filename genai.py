import requests

openai_api_key = "" # Add your Open API key

def generate_summary_with_openai(st, transcript, num_sentences=5):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}",
        }
        data = {
            "model": "gpt-4o-mini",  # Or "gpt-4" if you have access
            "messages": [
                {"role": "developer",
                 "content": f"Summarize the following text in approximately {num_sentences} sentences:\n\n{transcript}"}
            ]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        response_json = response.json()
        summary = response_json["choices"][0]["message"]["content"].strip()
        return summary

    except requests.exceptions.RequestException as e:
        st.error(f"OpenAI API error: {e}")
        return None
    except (KeyError, IndexError) as e:  # Handle potential JSON parsing errors
        st.error(
            f"Error parsing OpenAI response: {e}. Raw Response: {response.text if 'response' in locals() else 'Not available'}")  # Print raw response for debugging.
        return None
