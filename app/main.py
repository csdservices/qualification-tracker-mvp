from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import SessionLocal
from . import models

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="app/templates")


# ---------- Database Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Routes ----------

# Homepage
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# Test DB connection
@app.get("/organisations")
def read_organisations(db: Session = Depends(get_db)):
    organisations = db.query(models.Organisation).all()
    return [
        {"id": org.id, "name": org.name}
        for org in organisations
    ]
