import google.generativeai as genai
import os
from PIL import Image
import io
import time
import random

def configure_genai():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)

def retry_with_backoff(func):
    def wrapper(*args, **kwargs):
        retries = 3
        delay = 2
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Check for rate limit error (usually 429)
                if "429" in str(e) or "Quota exceeded" in str(e):
                    if i == retries - 1:
                        raise e
                    sleep_time = delay + random.uniform(0, 1)
                    print(f"Rate limit hit. Retrying in {sleep_time:.2f} seconds...")
                    time.sleep(sleep_time)
                    delay *= 2
                else:
                    raise e
    return wrapper

@retry_with_backoff
def identify_plant_from_image(image_data, mime_type='image/jpeg'):
    configure_genai()
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = """
    Identify this medicinal plant. 
    Provide the response in valid HTML format. Use <b> tags for labels and <br> tags for line breaks. 
    Strictly follow this format:
    <b>Plant Name</b>: [Name]<br>
    <b>Scientific Name</b>: [Scientific Name]<br>
    <b>Tamil Name</b>: [Tamil Name]<br>
    <b>Medicinal Uses</b>: [List of uses]<br>
    
    
    If it's not a plant, clearly state that it is not a plant.
    """
    
    try:
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        else:
            image = image_data

        response = model.generate_content([prompt, image])
        text = response.text
        # Clean up code blocks if present
        text = text.replace("```html", "").replace("```", "")
        return text
    except Exception as e:
        return f"Error identifying plant: {str(e)}"

@retry_with_backoff
def get_growth_tips(plant_name):
    configure_genai()
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Provide detailed growth tips for the medicinal plant: {plant_name}.
    Include:
    1. Soil requirements
    2. Climate/Temperature
    3. Watering schedule
    4. Sunlight needs
    5. Common pests and cures
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting tips: {str(e)}"

@retry_with_backoff
def chat_with_bot(message, history=[]):
    configure_genai()
    # Using a valid model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # System instruction to restrict domain
    system_prompt = """
    You are a helpful botanical assistant for 'The Green Healers'. 
    Your role is to answer questions ONLY related to:
    - Medicinal plants and their uses
    - Gardening, soil, and climate for plants
    - Botany and plant identification
    - Natural home remedies using plants
    
    If the user asks about ANYTHING else (e.g., coding, movies, math, general knowledge, politics), 
    politely refuse and say: "I am a Green Healers botanical assistant. I can only help you with questions related to plants and gardening."
    
    Keep your answers helpful, concise, and accurate.
    """
    
    # We prepend the system prompt to the chat history or message
    # For a simple implementation, we can structure the chat to include this context.
    
    try:
        chat = model.start_chat(history=history)
        
        # Send message with instruction if it's the start, or just relies on the persona
        # To be safe, we can wrap the user message with the instruction for every turn or rely on the model.
        # Let's try sending the instruction as context effectively.
        
        full_prompt = f"{system_prompt}\n\nUser Question: {message}"
        
        response = chat.send_message(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
