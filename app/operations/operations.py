from database.model import Event, SessionLocal, Snapshot
from sqlalchemy.orm import Session

SNAPSHOT_THRESHOLD = 10


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_snapshot(db: Session, account_id: int):

    balance = get_balance(db, account_id)

    last_event = (
        db.query(Event)
        .filter(Event.account_id == account_id)
        .order_by(Event.id.desc())
        .first()
    )

    if last_event:
        snapshot = Snapshot(
            account_id=account_id, balance=balance, last_event_id=last_event.id
        )
        db.add(snapshot)
        db.commit()


def get_balance(db: Session, account_id: int):

    snapshot = (
        db.query(Snapshot)
        .filter(Snapshot.account_id == account_id)
        .order_by(Snapshot.id.desc())
        .first()
    )

    if snapshot:

        balance = snapshot.balance
        last_event_id = snapshot.last_event_id

        print(balance)

        events = (
            db.query(Event)
            .filter(Event.account_id == account_id, Event.id > last_event_id)
            .all()
        )
    else:

        events = db.query(Event).filter(Event.account_id == account_id).all()
        balance = 0

    for event in events:
        balance += event.amount

    return balance
