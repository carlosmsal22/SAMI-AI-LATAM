import openai
import os
from datetime import datetime
import csv
import run_gpt

def run_gpt(prompt, model="gpt-3.5-turbo", temperature=0.7):
    """Handle GPT analysis with error handling"""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a business intelligence analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Analysis failed: {str(e)}"
# Add this at the bottom of gpt_helpers.py
run_gpt = run_gpt_prompt
