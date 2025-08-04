from fastapi import FastAPI, UploadFile, File, HTTPException, Body, Depends, status, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta

from . import models, crud, logic, security, schemas
from .celery_tasks import run_slither_task, run_echidna_task
from .database import SessionLocal, engine, Base
from .connection_manager import manager

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ZeroLoop Technology API")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

# --- Dependencies ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Authentication Endpoints ---
@app.post("/users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Scanning Endpoints ---
@app.post("/scan/file", response_model=schemas.ScanTaskResponse)
async def start_comprehensive_scan(client_id: str = Body(...), contract_file: UploadFile = File(...), test_file: UploadFile = File(...)):
    if not contract_file.filename.endswith('.sol') or not test_file.filename.endswith('.sol'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload .sol files.")
    
    contract_code = (await contract_file.read()).decode('utf-8')
    test_contract_code = (await test_file.read()).decode('utf-8')
    
    run_slither_task.delay(contract_code, client_id)
    run_echidna_task.delay(contract_code, test_contract_code, 'TestVulnerable', client_id)
    
    return {"task_id": client_id, "status": "Comprehensive scan started"}

# --- Internal & WebSocket Endpoints ---
@app.post("/internal/scan-result/{client_id}")
async def post_scan_result(client_id: str, result: schemas.ScanResultPayload):
    await manager.send_personal_message(result.model_dump_json(), client_id)
    return {"status": "result delivered"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        manager.disconnect(client_id)