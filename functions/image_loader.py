import base64
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_image(uploaded_file):
    image_bytes = uploaded_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all readable text from this image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()
