# app/celery_tasks.py
from celery import Celery
import subprocess
import json
import tempfile
from pathlib import Path

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def run_slither_task(contract_code: str):
    """
    Receives smart contract code, saves it to a temporary file,
    runs a Slither scan, and returns the JSON results.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        contract_file = temp_path / "contract.sol"
        with open(contract_file, "w") as f:
            f.write(contract_code)

        output_file = temp_path / "slither-output.json"
        command = ['slither', str(contract_file), '--json', str(output_file)]
        subprocess.run(command, capture_output=True, text=True)

        try:
            with open(output_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"success": False, "error": "Slither scan failed to produce a valid report."}

# --- Add this new task ---
@celery_app.task
def run_echidna_task(contract_code: str, test_contract_code: str, test_contract_name: str):
    """
    Receives a main contract and a test contract, saves them with correct names,
    runs an Echidna fuzzing test, and returns the output.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # FIX: Use the filenames that the import statement expects.
        contract_file = temp_path / "Vulnerable.sol"
        test_file = temp_path / "TestVulnerable.sol"

        with open(contract_file, "w") as f:
            f.write(contract_code)
        with open(test_file, "w") as f:
            f.write(test_contract_code)

        # FIX: The command should point to the test file, which imports the other.
        command = ['echidna', str(test_file), '--contract', test_contract_name]

        result = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        combined_output = result.stdout

        # Improved error checking for more accurate results
        if "Couldn't compile" in combined_output:
            return {"success": False, "error": "Compilation Failed", "output": combined_output}
        elif "falsified" in combined_output:
            return {"success": True, "bug_found": True, "output": combined_output}
        else:
            return {"success": True, "bug_found": False, "output": combined_output}