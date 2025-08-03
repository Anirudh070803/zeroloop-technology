# app/logic.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def enhance_vulnerability_with_ai(vulnerability: dict) -> dict:
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    A smart contract scan found this vulnerability:
    - Name: {vulnerability.get('name')}
    - Severity: {vulnerability.get('severity')}
    - Tool Description: {vulnerability.get('description')}

    Explain this vulnerability in simple, easy-to-understand terms for a non-technical client. Your response must be only the explanation text, nothing else.
    """
    try:
        response = model.generate_content(prompt)
        vulnerability['simplified_explanation'] = response.text.strip()
    except Exception as e:
        vulnerability['simplified_explanation'] = f"Could not generate AI explanation: {e}"
    return vulnerability

def generate_ai_report(slither_json: dict) -> dict:
    if not slither_json or not slither_json.get('success'):
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