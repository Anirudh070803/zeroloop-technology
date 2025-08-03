# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, Body
from .celery_tasks import run_slither_task
from . import schemas
from .connection_manager import manager

app = FastAPI(title="ZeroLoop Technology API")

@app.post("/scan/file", response_model=schemas.ScanTaskResponse)
async def start_scan_from_file(client_id: str = Body(...), file: UploadFile = File(...)):
    """
    Receives a smart contract file and a client_id, starts a scan,
    and returns immediately.
    """
    if not file.filename.endswith('.sol'):
        raise HTTPException(status_code=400, detail="Invalid file type.")
    
    contract_code = (await file.read()).decode('utf-8')
    
    # Start the background task, passing the client_id
    run_slither_task.delay(contract_code, client_id)
    
    # We use the client_id as the task_id for simplicity
    return {"task_id": client_id, "status": "Scan started"}

@app.post("/internal/scan-result/{client_id}")
async def post_scan_result(client_id: str, report: schemas.HumanReadableReport):
    """
    An internal-only endpoint for the Celery worker to post results to.
    This endpoint then pushes the result to the client via WebSocket.
    """
    await manager.send_personal_message(report.model_dump_json(), client_id)
    return {"status": "result delivered"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        manager.disconnect(client_id)