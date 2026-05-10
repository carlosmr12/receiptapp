import os
import base64
import json
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client for OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def resize_and_encode_image(image_path, max_size=(1024, 1024)):
    """Resizes, converts to JPEG, and base64 encodes an image."""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size)
            # Convert to JPEG to ensure compatibility and reduce size
            import io
            buffer = io.BytesIO()
            img.convert('RGB').save(buffer, format="JPEG")
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def extract_receipt_data_with_openrouter(image_path):
    """Extracts receipt data using a multimodal LLM via OpenRouter."""
    encoded_image = resize_and_encode_image(image_path)
    if not encoded_image:
        return None

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENROUTER_MODEL"),  # A cost-effective and capable model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze the receipt image and extract the store name, date of purchase, and the final total amount. The date should be in YYYY-MM-DD format. The total amount should be a decimal number without the dolar sign. Return the result as a clean JSON object with the keys 'store', 'date_of_purchase', and 'total_amount'."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.0, # We want deterministic output
            response_format={"type": "json_object"}, # Request JSON output
        )

        # The response content will be a JSON string, so we need to parse it.
        response_content = response.choices[0].message.content
        return json.loads(response_content)

    except Exception as e:
        print(f"Error calling OpenRouter API: {e}")
        return None