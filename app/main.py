from data_validation.model import Operation
from database.model import Event
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from operations.operations import (
    SNAPSHOT_THRESHOLD,
    create_snapshot,
    get_balance,
    get_db,
)
from sqlalchemy.orm import Session
from utils.config import send_message_to_sqs

app = FastAPI()


@app.post("/deposit")
async def deposit(
    operation: Operation,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if operation.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    event = Event(
        event_type="deposit", amount=operation.amount, account_id=operation.account_id
    )
    db.add(event)
    db.commit()

    background_tasks.add_task(
        send_message_to_sqs,
        {
            "event_type": "deposit",
            "amount": operation.amount,
            "account_id": operation.account_id,
        },
    )

    event_count = (
        db.query(Event).filter(Event.account_id == operation.account_id).count()
    )
    if event_count % SNAPSHOT_THRESHOLD == 0:
        create_snapshot(db, operation.account_id)

    return {"status": "success", "balance": get_balance(db, operation.account_id)}


@app.post("/withdraw")
async def withdraw(
    operation: Operation,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
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

    background_tasks.add_task(
        send_message_to_sqs,
        {
            "event_type": "withdrawal",
            "amount": -operation.amount,
            "account_id": operation.account_id,
        },
    )

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
