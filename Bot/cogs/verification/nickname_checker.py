import re
from dotenv import load_dotenv
import os
import openai



load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client  = openai.OpenAI(api_key=OPENAI_API_KEY)


def is_nick_name_valid(nickname: str) -> bool:
    if not is_wild_west_name(nickname):
        return False
    
    if not re.match(r"^[A-Z][a-z]+ [A-Z][a-z]+$", nickname):
        return False
    
    return True


def is_wild_west_name(nickname: str) -> bool:
    """Check if the nickname is a wild west name."""
    
    prompt = (
        f"Consider historical records from the 19th-century American Wild West. "
        f"Would the name '{nickname}' be a realistic name from that era? "
        f"Answer with only 'yes' or 'no'. Do not add a period or any explanation."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in 19th-century American Wild West history and naming conventions."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_response = response.choices[0].message.content.strip().lower()
        print(f"API Response: {ai_response}")  # Debugging
        return ai_response == "yes"
    
    except Exception as e:
        print(f"API Error: {e}")
        return False




def suggest_valid_nickname(nickname: str) -> str:
    """OpenAi to suggest a valid nickname."""

    prompt = (
        f"Suggest three valid 19th-century to current century real Wild West names similar to '{nickname}'. "
        "Follow these rules: Reply only with the names, separated by commas, no explanation nor extra words just the name, "
        "capitalize the first letter of each word, and do not add a period at the end."
    )

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages= [
            {"role": "system", "content": "You are an expert in historical names."},
            {"role": "user", "content": prompt}
        ]
    )

    

    return response.choices[0].message.content













 # data = {
    #     "model": "deepseek-r1:8b",  # Change model name if using a different one
    #     "prompt": prompt,
    #     "stream": False
    # }

    # try:
    #     response = requests.post(OLLAMA_API_URL, json=data).json()
    #     response_json = response.get("response", "").strip()
    #     result = re.sub(r"<think>.*?</think>", "", response_json, flags=re.DOTALL).strip()
    #     print(result)
    #     return result == "yes"
    #     # print("API Response:", response_json)  # Debugging
    # except Exception as e:
    #     print("Error:", e)  # Print any errors
    #     return False









# data = {
    #     "model": "deepseek-r1:8b",  # Change model if needed
    #     "prompt": prompt,
    #     "stream": False
    # }

    # async with httpx.AsyncClient(timeout=15.0) as client:

    #     response = await client.post(OLLAMA_API_URL, json=data)
    #     response_json = response.json()
        
    # result = response_json.get("response", "").strip()
    # # Remove anything between <think> and </think>
    # result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL).strip()

    # return result






