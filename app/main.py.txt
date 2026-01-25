from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Staff

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    staff = db.query(Staff).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "staff": staff}
    )

@app.post("/add")
def add_staff(
    first_name: str = Form(...),
    last_name: str = Form(...),
    db: Session = Depends(get_db)
):
    new_staff = Staff(first_name=first_name, last_name=last_name)
    db.add(new_staff)
    db.commit()
    return RedirectResponse("/", status_code=303)
