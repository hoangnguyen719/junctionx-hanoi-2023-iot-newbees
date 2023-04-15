from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import select

import models, schemas, database


def read_root():
    return {'name': 'fastapi-songs'}

def read_songs(db: Session):
    return db.query(models.Song).all()

def read_all_lte_signals(db: Session):
    return db.query(models.LteSignal).all()

def read_all_cells(db: Session):
    return db.query(models.LteCell).all()

def get_last_value(db: Session, model: database.Base, sort_attr: InstrumentedAttribute):
    with db:
        statement = select(model).order_by(sort_attr.desc()).limit(1)
        results = db.execute(statement)
        results = results.all()
    if len(results) > 0:
        return results[0][model.__name__]
    else:
        return None

def get_last_signal(db: Session):
    return get_last_value(db=db, model=models.LteSignal, sort_attr=models.LteSignal.ts)

def get_last_cell(db: Session):
    return get_last_value(db=db, model=models.LteCell, sort_attr=models.LteCell.last_seen)

def get_current_frequency(db: Session):
    return get_last_value(
        db=db, model=models.Frequency, sort_attr=models.CurrentFrequency.updated_at
    )

def append_signal(signal: schemas.Signal, db: Session, dt: datetime):
    with db:
        # Append signal to table
        db_signal = models.LteSignal(
            ts = dt
            , scellid = signal.scellid
            , rsrq = signal.rsrq
            , rsrp = signal.rsrp
        )
        db.add(db_signal)
        db.commit()
        db.refresh(db_signal)
    return db_signal

def update_cell(signal: schemas.Signal, db: Session, dt: datetime):
    # If cell is the same as last cell, update `last_seen`
    # Otherwise, append the cell as a new cell
    with db:
        # Get last cell
        last_cell = get_last_cell(db)

        if (last_cell == []) | (last_cell.scellid != signal.scellid):
            last_cell = models.LteCell(
                pcellid = signal.pcellid
                , scellid = signal.scellid
                , mcc = signal.mcc
                , mnc = signal.mnc
                , first_seen = dt
                , last_seen = dt
            )
        else:
            setattr(last_cell, 'last_seen', dt)
        db.add(last_cell)
        db.commit()
        db.refresh(last_cell)
    return last_cell

def update_current_frequency(freq: schemas.Frequency, db: Session, dt: datetime):
    with db:
        # Get last cell
        cur_freq = get_current_frequency(db)
        # if cur_freq is None or cur_freq is different, update

def update_frequency_history(frequency: schemas.Frequency, db: Session, dt: datetime):
    # If new frequency is different from current frequency, update history of frequency
    pass

def get_signals(
    db: Session
    , signal_count: int
    , scellid: str | None = None
    ):
    with db:
        statement = select(models.LteSignal)
        if scellid:
            statement = statement.where(models.LteSignal.scellid == scellid)
        statement = statement.order_by(models.LteSignal.ts.desc()).limit(signal_count)
        results = db.execute(statement)
        results = results.all()
    return list(reversed([s["LteSignal"] for s in results]))