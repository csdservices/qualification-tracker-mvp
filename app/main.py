from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


from fastapi import Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/organisations")
def read_organisations(db: Session = Depends(get_db)):
    orgs = db.query(models.Organisation).all()
    return [{"id": o.id, "name": o.name} for o in orgs]
