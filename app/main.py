from data_validation.model import Operation
from database.model import Event
from fastapi import Depends, FastAPI, HTTPException
from operations.operations import (
    SNAPSHOT_THRESHOLD,
    create_snapshot,
    get_balance,
    get_db,
)
from sqlalchemy.orm import Session

app = FastAPI()


@app.post("/deposit/")
async def deposit(operation: Operation, db: Session = Depends(get_db)):
    if operation.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    event = Event(
        event_type="deposit", amount=operation.amount, account_id=operation.account_id
    )
    db.add(event)
    db.commit()

    # Check if it's time to create a snapshot
    event_count = (
        db.query(Event).filter(Event.account_id == operation.account_id).count()
    )
    if event_count % SNAPSHOT_THRESHOLD == 0:
        create_snapshot(db, operation.account_id)

    return {"status": "success", "balance": get_balance(db, operation.account_id)}


@app.post("/withdraw/")
async def withdraw(operation: Operation, db: Session = Depends(get_db)):
    if operation.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    balance = get_balance(db, operation.account_id)
    if operation.amount > balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    event = Event(
        event_type="withdrawal",
        amount=-operation.amount,
        account_id=operation.account_id,
    )
    db.add(event)
    db.commit()

    # Check if it's time to create a snapshot
    event_count = (
        db.query(Event).filter(Event.account_id == operation.account_id).count()
    )
    if event_count % SNAPSHOT_THRESHOLD == 0:
        create_snapshot(db, operation.account_id)

    return {"status": "success", "balance": get_balance(db, operation.account_id)}


@app.get("/balance/{account_id}")
async def balance(account_id: int, db: Session = Depends(get_db)):
    balance = get_balance(db, account_id)
    return {"account_id": account_id, "balance": balance}
