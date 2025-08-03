from celery import Celery

client_celery_app = Celery(
    'client_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

def main():
    print("Reading smart contract and test files...")
    with open('Vulnerable.sol', 'r') as f:
        contract_code = f.read()
    with open('TestVulnerable.sol', 'r') as f:
        test_contract_code = f.read()

    print("Sending Echidna scan task to the Celery worker...")
    
    task = client_celery_app.send_task(
        'app.celery_tasks.run_echidna_task',
        args=[contract_code, test_contract_code, 'TestVulnerable']
    )
    
    print(f"Task sent! The Task ID is: {task.id}")
    print("Check the Docker terminal to see the worker's log.")

if __name__ == "__main__":
    main()