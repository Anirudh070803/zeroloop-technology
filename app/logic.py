# app/logic.py

def generate_human_readable_report(slither_json: dict) -> dict:
    """
    Processes raw JSON from a Slither scan and creates a simple,
    human-readable summary report.
    """
    if not slither_json or not slither_json.get('success'):
        return {
            "summary": "Scan failed or produced no results.",
            "vulnerabilities": []
        }

    vulnerabilities = slither_json.get('results', {}).get('detectors', [])
    
    report = {
        "summary": f"Scan complete. Found {len(vulnerabilities)} potential vulnerability type(s).",
        "vulnerabilities": []
    }

    for vuln in vulnerabilities:
        report["vulnerabilities"].append({
            "name": vuln.get('check'),
            "severity": vuln.get('impact'),
            "description": vuln.get('description').strip()
        })
        
    return report