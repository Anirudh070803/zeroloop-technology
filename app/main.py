# app/main.py
from fastapi import FastAPI, Body, UploadFile, File, HTTPException
from .celery_tasks import run_slither_task, celery_app
from . import schemas, logic

app = FastAPI(title="ZeroLoop Technology API")

@app.post("/scan", response_model=schemas.ScanResponse)
def start_scan(request: schemas.ScanRequest):
    """
    Receives smart contract code as JSON and starts a Slither scan.
    """
    task = run_slither_task.delay(request.contract_code)
    return {"task_id": task.id, "status": "Scan started"}

@app.post("/scan/text", response_model=schemas.ScanResponse)
def start_scan_from_text(contract_code: str = Body(..., media_type="text/plain")):
    """
    Receives raw smart contract code as plain text and starts a scan.
    """
    task = run_slither_task.delay(contract_code)
    return {"task_id": task.id, "status": "Scan started"}

# --- Add this new endpoint ---
@app.post("/scan/file", response_model=schemas.ScanResponse)
async def start_scan_from_file(file: UploadFile = File(...)):
    """
    Receives a smart contract file, starts a Slither scan in the background,
    and returns a task ID.
    """
    if not file.filename.endswith('.sol'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .sol file.")
    
    contract_code = (await file.read()).decode('utf-8')
    task = run_slither_task.delay(contract_code)
    return {"task_id": task.id, "status": "Scan started"}

@app.get("/results/{task_id}", response_model=schemas.ResultResponse)
def get_scan_results(task_id: str):
    """
    Retrieves the status and result of a background scan task.
    """
    task_result = celery_app.AsyncResult(task_id)
    
    if task_result.state == 'SUCCESS':
        raw_results = task_result.get()
        # Use our new function from logic.py
        human_readable_report = logic.generate_human_readable_report(raw_results)
        return {"task_id": task_id, "status": task_result.state, "result": human_readable_report}
    
    elif task_result.state == 'FAILURE':
        return {"task_id": task_id, "status": task_result.state, "result": "Task failed to execute."}
        
    return {"task_id": task_id, "status": task_result.state, "result": "Scan is still in progress..."}