from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import Form

from fastapi import Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

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


# -- Admin dashboard --
@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    organisations = db.query(models.Organisation).all()
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "organisations": organisations}
    )


# -- Add staff to an organisation --
@app.post("/admin/add_staff")
def add_staff(
    org_id: int = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    import uuid
    from datetime import datetime
    from .models import Staff, Organisation

    # Generate UID
    uid = str(uuid.uuid4())

    # Create new staff
    new_staff = Staff(
        uid=uid,
        name=name,
        email=email,
        created_at=datetime.utcnow()
    )
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)

    # Link staff to organisation
    org = db.query(Organisation).filter(Organisation.id == org_id).first()
    if org:
        org.staff_members.append(new_staff)
        db.commit()

    return {"status": "success", "staff_id": new_staff.id, "uid": new_staff.uid}

# List all staff
@app.get("/staff")
def read_staff(db: Session = Depends(get_db)):
    staff_members = db.query(models.Staff).all()
    return [
        {
            "id": staff.id,
            "uid": staff.uid,
            "name": staff.name,
            "email": staff.email,
            "created_at": staff.created_at
        }
        for staff in staff_members
    ]


# -- CREATE ORGANISATIONS
@app.post("/organisations/create")
def create_organisation(
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    organisation = models.Organisation(name=name)
    db.add(organisation)
    db.commit()
    db.refresh(organisation)

    return RedirectResponse(
        url="/admin",
        status_code=HTTP_303_SEE_OTHER
    )

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, db: Session = Depends(get_db)):
    organisations = db.query(models.Organisation).all()

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "organisations": organisations
        }
    )
