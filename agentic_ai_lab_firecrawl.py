import ollama
import requests
from fpdf import FPDF

FIRECRAWL_API_KEY = 'fc-4b13e15b33bf4a88b7f9989f331c7f15'
TARGET_URL = 'https://api.firecrawl.dev/v1/scrape'
MODEL_NAME = 'mistral:latest'

def fetch_page_content(url):
    headers = {
        "Accept": "application/json",
        "Authorization": f'Bearer {FIRECRAWL_API_KEY}'
    }
    json_data = {
        'url': url
    }
    response = requests.post(TARGET_URL, json=json_data, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e}')
        try:
            print("Response content:", response.json())
        except ValueError:  # Handle invalid JSON response
            print("Response content:", response.text)
            raise
    data = response.json()
    if not data.get("text", ""):
        print("Full API response:", data)
    return data.get("text") or data.get("data", {}).get("markdown", "")

def process_with_llm(content):
    print("Processing content with offline LLM...")
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{
            "role": "user", 
            "content": f'Please summarize and extract key points from the following text for a cybersecurity student:\n\n{content}'
        }]
    )
    return response['message']['content']
def generate_pdf(text, filename='agentic_ai_summary.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    lines = text.split('\n')
    for line in lines:
            pdf.multi_cell(0, 10, txt=line)
    pdf.output(filename)
    print(f"PDF report generated: {filename}")

def main():
    print("=== Agentic AI Lab: Firecrawl LLM Test ===")
    url = input("Enter the URL to scrape and process: ")
    
    try:
        scraped_content = fetch_page_content(url)
        if not scraped_content:
            print("No content found at the provided URL.")
            return
        
        summary = process_with_llm(scraped_content)
        print("\n -- LLM Summary Response --")
        print(summary)
        
        generate_pdf(summary)
        
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    main()