CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR,
    amount FLOAT,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    account_id INTEGER
);

CREATE INDEX ix_events_id ON events (id);
CREATE INDEX ix_events_event_type ON events (event_type);
CREATE INDEX ix_events_account_id ON events (account_id);



CREATE TABLE snapshots (
    id SERIAL PRIMARY KEY,
    account_id INTEGER,
    balance FLOAT,
    last_event_id INTEGER REFERENCES events(id),
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_snapshots_id ON snapshots (id);
CREATE INDEX ix_snapshots_account_id ON snapshots (account_id);
