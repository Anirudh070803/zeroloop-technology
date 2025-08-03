import subprocess
import json
import os

def run_slither_scan(file_path):
    """
    Runs a Slither scan and reads the JSON output from a temporary file.
    """
    output_file = 'slither-output.json'
    command = ['slither', file_path, '--json', output_file]

    print(f"Running command: {' '.join(command)}")
    
    # Run the command and capture its output streams
    result = subprocess.run(command, capture_output=True, text=True)

    # Slither often exits with a non-zero code when it finds vulnerabilities.
    # So, instead of checking the return code, we'll check if the JSON
    # result file was successfully created.
    try:
        print("Scan complete. Reading results from file...")
        with open(output_file, 'r') as f:
            scan_data = json.load(f)
        
        # Clean up the temporary file after we're done with it
        os.remove(output_file)
        
        return scan_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # This code will now run only if the scan truly failed to produce a valid result file.
        print(f"Error reading or parsing the result file: {e}")
        print("\nSlither's raw error output (if any):")
        print(result.stderr)
        return None

# --- Main execution part remains the same ---
if __name__ == "__main__":
    contract_file = 'Vulnerable.sol'
    scan_results = run_slither_scan(contract_file)

    if scan_results and scan_results.get('success'):
        print("\n--- Slither Scan Report ---")
        vulnerabilities = scan_results.get('results', {}).get('detectors', [])
        
        if not vulnerabilities:
            print("No vulnerabilities found.")
        else:
            print(f"Found {len(vulnerabilities)} vulnerability type(s):")
            for vuln in vulnerabilities:
                print(f"\n[!] Vulnerability: {vuln.get('check')}")
                print(f"    Description: {vuln.get('description')}")
    else:
        print("\nScan failed or produced no valid results.")