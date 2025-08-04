# app/celery_tasks.py
from celery import Celery
import subprocess
import json
import tempfile
from pathlib import Path
from . import logic
import requests

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

# --- CORRECTED FUNCTION SIGNATURE BELOW ---
@celery_app.task
def run_slither_task(contract_code: str, client_id: str):
    """
    Runs a Slither scan, enhances the report with AI, and posts the
    final report back to the main API server.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        contract_file = Path(temp_dir) / "contract.sol"
        with open(contract_file, "w") as f:
            f.write(contract_code)

        output_file = Path(temp_dir) / "slither-output.json"
        command = ['slither', str(contract_file), '--json', str(output_file)]
        subprocess.run(command, capture_output=True, text=True)

        try:
            with open(output_file, 'r') as f:
                scan_data = json.load(f)
            
            ai_report = logic.generate_ai_report(scan_data)
            
            requests.post(
                f"http://backend:8000/internal/scan-result/{client_id}",
                json={"scan_type": "static_analysis", "data": ai_report}
            )
        except (FileNotFoundError, json.JSONDecodeError):
            error_report = {"summary": "Slither scan failed.", "vulnerabilities": []}
            requests.post(
                f"http://backend:8000/internal/scan-result/{client_id}",
                json={"scan_type": "static_analysis", "data": error_report}
            )

# This task already has the correct arguments, no change needed here.
@celery_app.task
def run_echidna_task(contract_code: str, test_contract_code: str, test_contract_name: str, client_id: str):
    with tempfile.TemporaryDirectory() as temp_dir:
        contract_file = Path(temp_dir) / "Vulnerable.sol"
        test_file = Path(temp_dir) / "TestVulnerable.sol"
        with open(contract_file, "w") as f:
            f.write(contract_code)
        with open(test_file, "w") as f:
            f.write(test_contract_code)
        command = ['echidna', str(test_file), '--contract', test_contract_name]
        result = subprocess.run(
            command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        combined_output = result.stdout
        echidna_report = {}
        if "Couldn't compile" in combined_output:
            echidna_report = {"success": False, "error": "Compilation Failed", "output": combined_output}
        elif "falsified" in combined_output:
            echidna_report = {"success": True, "bug_found": True, "output": combined_output}
        else:
            echidna_report = {"success": True, "bug_found": False, "output": combined_output}
        requests.post(
            f"http://backend:8000/internal/scan-result/{client_id}",
            json={"scan_type": "dynamic_analysis", "data": echidna_report}
        )