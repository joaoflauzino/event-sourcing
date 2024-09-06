# Event Sourcing System

This repository contains an implementation of an event sourcing system using FastAPI, SQLAlchemy, and PostgreSQL. The system tracks events such as deposits and withdrawals for accounts, and periodically creates snapshots to optimize state reconstruction.

## Features

- **Event Sourcing**: Each account operation (e.g., deposit, withdrawal) is stored as an event in the database.
- **Snapshots**: Periodically creates snapshots to store the current state of an account, reducing the need to replay all events.
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.6+.
- **SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **PostgreSQL**: Open-source object-relational database system.

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Poetry (recommended for creating isolated Python environments)

### Step 1: Clone the Repository

```bash
git clone https://github.com/joaoflauzino/event-sourcing-system.git
cd event-sourcing-system
```
## Step 2: Install Dependencies

```bash
poetry install
```
## Step 3: Start postgres database

```bash
docker-compose up -d
```

Create a SQS queue

```sh
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name topic-bank --region sa-east-1
```

## Usage 

### Running the api

```bash
cd app/
fastapi dev main.py
```

### Running the pooling

```bash
cd app/
python pooling.py
```


### API Endpoints

- Deposit:

    - Endpoint: /deposit/
    - Method: POST
    - Description: Creates a new deposit for an account.
    - Request example:

```bash
curl -X POST "http://127.0.0.1:8000/deposit/" -H "Content-Type: application/json" -d '{"account_id": 1, "amount": 100.0}'
```


- Withdraw:

    - Endpoint: /withdraw/
    - Method: POST
    - Description: Creates a new withdraw for an account.
    - Request example:


```bash
curl -X POST "http://127.0.0.1:8000/withdraw/" -H "Content-Type: application/json" -d '{"account_id": 1, "amount": 100.0}'
```

- Get account balance:

    - Endpoint: /accounts/{account_id}
    - Method: GET
    - Description: Retrieves the current balance of an account by replaying all events and applying snapshots.


## Event Sourcing Logic

The system tracks events for each account in the events table. Each event represents an operation, such as a deposit or withdrawal. To optimize the reconstruction of an account's state, the system periodically creates snapshots, which store the current balance of the account and the ID of the last event applied.

## Snapshot Creation

Snapshots are created after a certain number of events (configured by SNAPSHOT_THRESHOLD). When the number of events reaches this threshold, a snapshot is created, storing the current balance of the account and reducing the need to replay all previous events in future queries.

## Example Data Flow

- Event Creation: A user deposits $100 into their account.
- Event Stored: The deposit event is stored in the events table.
- Snapshot Triggered: If the event count reaches the SNAPSHOT_THRESHOLD, a snapshot is created and stored in the snapshots table.
- Account Balance Query: When querying the balance, the system will use the latest snapshot and replay any events that occurred after the snapshot to compute the current balance.
 

