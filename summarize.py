import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_tldr(comments_list):
    """
    Takes a list of comment dictionaries, extracts the top 100, 
    and generates a 3-sentence summary.
    """
    if not comments_list:
        return "Not enough comments to generate a summary."

    top_comments = comments_list[:100]
    raw_text = " ".join([c["comment_text"] for c in top_comments])
    
    raw_text = raw_text[:10000] 

    prompt = (
        "You are an expert YouTube strategist. Read the following YouTube comments "
        "and provide a concise, 3-sentence executive summary of the overall audience reaction, "
        "sentiment, and main topics discussed. \n\n"
        f"Comments: {raw_text}"
    )

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary could not be generated at this time."