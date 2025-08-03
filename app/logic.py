# app/logic.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def enhance_vulnerability_with_ai(vulnerability: dict) -> dict:
    """
    Takes a vulnerability from Slither and uses an LLM to add a
    simplified explanation and a confidence score for false positives.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert smart contract security auditor with deep knowledge of Solidity. Your task is to analyze a finding from the Slither static analysis tool and provide a clear, concise analysis for a client.

    **Slither Finding:**
    - **Name:** {vulnerability.get('name')}
    - **Severity:** {vulnerability.get('severity')}
    - **Tool Description:** {vulnerability.get('description')}

    **Your Tasks:**
    1.  **Analyze Confidence:** Based on the description, assess the likelihood that this is a true, exploitable vulnerability versus a false positive. Provide a "confidence" score of "High", "Medium", or "Low". High confidence means it is very likely a real issue. Low confidence means it might be a false positive.
    2.  **Simplify Explanation:** Provide a "simplified_explanation" of what this vulnerability means in simple, easy-to-understand terms for a non-technical client.

    **Output Format:**
    Your response MUST be only a valid JSON object with the keys "confidence" and "simplified_explanation".

    **Example Response:**
    {{
      "confidence": "High",
      "simplified_explanation": "This is a brief, easy-to-understand explanation of the potential security risk."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        ai_response_text = response.text.strip().replace('```json', '').replace('```', '')
        ai_data = json.loads(ai_response_text)
        
        vulnerability['confidence'] = ai_data.get('confidence', 'Medium')
        vulnerability['simplified_explanation'] = ai_data.get('simplified_explanation')
        
    except Exception as e:
        print(f"Error calling AI model: {e}")
        vulnerability['confidence'] = "Error"
        vulnerability['simplified_explanation'] = "Could not generate AI explanation."

    return vulnerability

# The generate_ai_report function remains the same, as it already calls the function above.
def generate_ai_report(slither_json: dict) -> dict:
    if not slither_json or not slither_json.get('success', False):
        return {"summary": "Scan failed.", "vulnerabilities": []}

    vulnerabilities = slither_json.get('results', {}).get('detectors', [])
    report = {
        "summary": f"Scan complete. Found {len(vulnerabilities)} potential vulnerability type(s).",
        "vulnerabilities": []
    }

    for vuln in vulnerabilities:
        vuln_details = {
            "name": vuln.get('check'),
            "severity": vuln.get('impact'),
            "description": vuln.get('description').strip()
        }
        enhanced_details = enhance_vulnerability_with_ai(vuln_details)
        report["vulnerabilities"].append(enhanced_details)
        
    return report