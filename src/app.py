import logging
import uvicorn
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Annotated

from models import models
from services.data_loader import DataLoader
from database.database import engine, get_database_session

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    """
    Executes on startup of application and initializes data ingestion process into database
    """
    try:
        dbs = DataLoader()
        db = next(get_database_session())
        models.Base.metadata.drop_all(bind=engine)
        models.Base.metadata.create_all(bind=engine)
        if not db.query(models.Record).count() or not db.query(models.Station).count():
            dbs.load_data_from_files()
        if not db.query(models.Statistics).count():
            dbs.calculate_statistics()
    except Exception as e:
        logging.error(f"Error during startup of application: {e}")

        
@app.get('/api/weather')
async def fetch_weather_data(
    db: Annotated[Session, Depends(get_database_session)], 
    station_id: Optional[int] = None, 
    date: Optional[str] = None, 
    page: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1)
):
    """
    Fetch weather records based on station ID and date.
    
    @param: db :: Database session.
    @param: station_id :: Optional station ID for filtering.
    @param: date:: Optional date for filtering.
    @param: page :: Page number for pagination.
    @param: limit :: Number of records per page.
    """
    try:
        query = db.query(models.Record)
        
        if station_id:
            query = query.filter(models.Record.station_id == station_id)
            if not query.count():
                raise ValueError(f'Station ID {station_id} does not exist.')
        
        if date:
            query = query.filter(models.Record.date == date)
            if not query.count():
                raise ValueError(f'Date {date} does not exist.')

        records = query.offset(page * limit).limit(limit).all()
        return {'count': len(records), 'data': records}
    
    except Exception as e:
        return {'error': str(e)}

@app.get('/api/weather/stats')
async def fetch_weather_stats(
    db: Annotated[Session, Depends(get_database_session)], 
    station_id: Optional[int] = None, 
    year: Optional[int] = None, 
    page: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1)
):
    """
    Fetch weather statistics based on station ID and year.
    
    @param: db :: Database session.
    @param: station_id :: Optional station ID for filtering.
    @param: year:: Optional year for filtering.
    @param: page :: Page number for pagination.
    @param: limit :: Number of records per page.
    """
    try:
        query = db.query(models.Statistics)
        
        if station_id:
            query = query.filter(models.Statistics.station_id == station_id)
            if not query.count():
                raise ValueError(f'Station ID {station_id} does not exist.')
        
        if year:
            query = query.filter(models.Statistics.year == year)
            if not query.count():
                raise ValueError(f'Year {year} does not exist.')

        stats = query.offset(page * limit).limit(limit).all()
        return {'count': len(stats), 'data': stats}
    
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
