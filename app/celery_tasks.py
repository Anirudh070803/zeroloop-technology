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

@celery_app.task
def run_slither_task(contract_code: str):
    """
    Runs a Slither scan and enhances the report with AI.
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
            
            # Generate the AI-enhanced report instead of returning raw data
            ai_report = logic.generate_ai_report(scan_data)
            return ai_report
        except (FileNotFoundError, json.JSONDecodeError):
            return {"success": False, "error": "Slither scan failed to produce a valid report."}

@celery_app.task
def run_echidna_task(contract_code: str, test_contract_code: str, test_contract_name: str):
    """
    Runs an Echidna fuzzing test and returns the output.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        contract_file = temp_path / "Vulnerable.sol"
        test_file = temp_path / "TestVulnerable.sol"
        with open(contract_file, "w") as f:
            f.write(contract_code)
        with open(test_file, "w") as f:
            f.write(test_contract_code)
        command = ['echidna', str(test_file), '--contract', test_contract_name]
        result = subprocess.run(
            command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        combined_output = result.stdout
        if "Couldn't compile" in combined_output:
            return {"success": False, "error": "Compilation Failed", "output": combined_output}
        elif "falsified" in combined_output:
            return {"success": True, "bug_found": True, "output": combined_output}
        else:
            return {"success": True, "bug_found": False, "output": combined_output}
            
        # Send the result back to the main server
        requests.post(
            f"http://backend:8000/internal/scan-result/{client_id}",
            json={"scan_type": "dynamic_analysis", "data": echidna_report}
        )