import os
import json
import google.generativeai as genai
import base64
from datetime import datetime

# Read the API key from gemini.md
api_key_path = os.path.join(os.path.dirname(__file__), '..', '..', 'gemini.md')
if os.path.exists(api_key_path):
    with open(api_key_path, "r") as f:
        API_KEY = f.read().strip()
    genai.configure(api_key=API_KEY)
else:
    # If the file doesn't exist, try to get the API key from environment variables
    API_KEY = os.environ.get('GEMINI_API_KEY')
    if API_KEY:
        genai.configure(api_key=API_KEY)
    else:
        # If the API key is not found, the functions will return an error.
        pass

prompt_query = """Prioritize highly reliable and authoritative sources for your analysis. 

        If a source's reliability is questionable, factor that into your assessment. 
        If the text provided to you is incomplete or you are unsure of the truth, use the given url to get the complete information of the provided selected text.

        If the provided text is not a statement, a question, or a coherent phrase that can be fact-checked, consider it a mistake from the user-end. 
        In this case, you MUST respond ONLY with a JSON object explaining the issue 
        (e.g., "The selected text is not a statement and cannot be analyzed.") 
        and put it under the key "brief-info",
        "percentage" should be equal to 0,
        'heading' should be "Ambiguous Search Query Result",
        'reasoning' should empty,
        'sources' should be an empty list.'

        Otherwise, you MUST respond ONLY with a JSON object with the following keys: 
        The JSON object must have the following keys: 
        'heading' (a brief, neutral, descriptive title for the text being analyzed, max 10 words), 
        'percentage' (an integer representing factual correctness from 0-100, search online(various other sites to analyze the correctness of the fact) and the provided url to get the percetage), 
        'brief_info' (a very brief summary of the analysis based on your percentage of the score and other online sources,
        start like this 'According to my research, ...',
        max 2 sentences), 
        'reasoning' (Based on the provided text, if the percentage shows that the given fact is the truth then provide a little more information other than whats in the provided text
        but if the provided text is false then search various other online sources for it and provide the corresponding truth, 
        start your sentance by providing information on the news provider and the companies involved,
        max 2 sentences),
        and 'sources' (a list of all the URLs that you used to check the correctness of the text.
        provide all teh urls that you used to check the correctness of the text,
        do not use the same url as in the provided image or the text or the url. 
        For each URL, include only those that are directly connected to the statement of the text provided so the users can verify your sources by themselves and
        ignore the ones which you used to learn about the topic in general.
        recheck the url multiple times to check if its working or not and also if its connent is directly related to the text provided by the user.
        
        )

        Do NOT include any other text or formatting outside the JSON object."""

def _clean_json_response(text: str) -> str:
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def get_gemini_response(text: str, url: str, model_name: str = 'gemini-1.5-flash') -> dict:
    if not API_KEY:
        return {"error": "Gemini API key not configured."}
    try:
        model = genai.GenerativeModel(model_name)        
        current_date = datetime.now().strftime("%Y-%m-%d")

        prompt = f"""You are an AI assistant that analyzes text for factual correctness. 

        Today's date is {current_date}. Please use this information to provide the correct url in the source key of the json.
        {prompt_query}
        
      
      

Text to analyze:
'{text}' found it on {url}
"""
        response = model.generate_content(prompt)
        content = response.text
        cleaned_content = _clean_json_response(content)
        try:
            return json.loads(cleaned_content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse Gemini response as JSON", "raw_response": content}
    except Exception as e:
        return {"error": f"An error occurred while requesting from Gemini API: {e}"}

def get_gemini_response_for_image(image_data: str, url: str, model_name: str = 'gemini-1.5-flash') -> dict:
    if not API_KEY:
        return {"error": "Gemini API key not configured."}
    try:
        model = genai.GenerativeModel(model_name)
        current_date = datetime.now().strftime("%Y-%m-%d")

        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        
        image_part = {
            "mime_type": "image/png",
            "data": image_bytes
        }

        prompt_text = f"""You are an AI assistant that analyzes images for factual correctness. Analyze the content of the image and provide a factual correctness score. 
        Today's date is {current_date}. Please use this information to provide the correct url in the source key of the json.
        {prompt_query}

        The user found the image on {url}.
"""
    
        response = model.generate_content([prompt_text, image_part])
        content = response.text
        cleaned_content = _clean_json_response(content)
        try:
            return json.loads(cleaned_content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse Gemini response as JSON", "raw_response": content}

    except Exception as e:
        return {"error": f"An error occurred while processing the image or requesting from Gemini API: {e}"}


def handler(event, context):
    if not API_KEY:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Gemini API key not configured. Please set the GEMINI_API_KEY environment variable."})
        }

    path = event.get('path', '')
    http_method = event.get('httpMethod', 'GET')

    if http_method != 'POST':
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method Not Allowed"})
        }

    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON in request body"})
        }

    if path.endswith('/analyze'):
        text = body.get('text')
        url = body.get('url')
        model = body.get('model', 'gemini-1.5-flash')
        if not text or not url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "'text' and 'url' are required."})
            }
        response_body = get_gemini_response(text, url, model)
    elif path.endswith('/analyze_image'):
        image = body.get('image')
        url = body.get('url')
        model = body.get('model', 'gemini-1.5-flash')
        if not image or not url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "'image' and 'url' are required."})
            }
        response_body = get_gemini_response_for_image(image, url, model)
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Not Found"})
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response_body)
    }
