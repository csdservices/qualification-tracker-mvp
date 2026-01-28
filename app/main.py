from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models

app = FastAPI()

# 🔥 THIS CREATES YOUR TABLES
models.Base.metadata.create_all(bind=engine)

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

@app.get("/", response_class=HTMLResponse)
def read_root(
    request: Request,
    db: Session = Depends(get_db)
):
    organisations = db.query(models.Organisation).all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "organisations": organisations
        }
    )


@app.get("/organisations")
def read_organisations(db: Session = Depends(get_db)):
    organisations = db.query(models.Organisation).all()
    return [
        {"id": org.id, "name": org.name}
        for org in organisations
    ]


# -- ADDING STAFF VIA WEB FORM --
from fastapi import Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

@app.post("/staff")
def create_staff(
    name: str = Form(...),
    organisation_id: int = Form(...),
    db: Session = Depends(get_db)
):
    # Check if staff already exists? (Optional, for multi-org scenario)
    staff = Staff(name=name)
    db.add(staff)
    db.commit()
    db.refresh(staff)

    # Link staff to organisation
    org = db.query(models.Organisation).get(organisation_id)
    if org:
        org.staff_members.append(staff)
        db.commit()

    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)


