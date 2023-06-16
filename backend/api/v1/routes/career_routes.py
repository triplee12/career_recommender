#!/usr/bin/python3
"""Career routes module."""
import numpy as np
from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from tensorflow.keras.models import load_model
from sklearn.preprocessing import QuantileTransformer, StandardScaler
from backend.api.db_config import get_db
from backend.api.settings import TEMPLATES
from backend.api.v1.models.careers import Career
from backend.api.v1.schemas.career_schemas import (
    CareerCreate, CareerUpdate
)
from backend.api.v1.auths.oauth import get_current_user

career_router = APIRouter(prefix="/careers", tags=["careers"])
qt = QuantileTransformer(output_distribution='normal')
# Loading Model
model = load_model("backend/api/v1/models/model_career_RS.h5")
ss = StandardScaler()

class_names = [
    'BUSINESS','SPORTS AND PHYSICAL TRAIN',
    'ENGINEERING', 'AGRONOMIC, LIVESTOCK ENGINEERING',
    'HUMANITIES AND SOCIAL SCIENCE',
    'MATH AND PHYSICAL SCIENCES',
    'NUTRITION AND DIETETICS', 'HEALTH & MEDICINE',
    'ARTS AND DESIGN', 'BIOLOGICAL SCIENCE',
    'AGRICULTURAL, FOREST ENGINEERING',
    'PLASTIC ARTS, VISUAL ARTS', 'PHISICS'
]


@career_router.get("/", response_class=HTMLResponse)
async def retrieve_careers(
    request: Request,
    # current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Retrieve all the available careers."""
    careers = session.query(Career).all()
    return TEMPLATES.TemplateResponse(
        "careers/careers.html",
        {"request": request, "careers": careers}
    )


@career_router.get(
    "/career_with_skills",
    response_class=HTMLResponse
)
async def list_career_with_skills(
    request: Request,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """List all careers with skills."""
    if current_user:
        careers = session.query(Career).all()
        return TEMPLATES.TemplateResponse(
            "careers/career_with_skill.html",
            {"request": request, "careers": careers}
        )


@career_router.get(
    "/career_with_skills/{career_id}",
    response_class=HTMLResponse
)
async def retrieve_one_career_with_skill(
    request: Request,
    career_id: int, current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Retrieve a career for a given id."""
    if current_user:
        career = session.query(Career).filter(
            Career.id == career_id
        ).one_or_none()
        if not career:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Career does not exist"
            )
        return TEMPLATES.TemplateResponse(
            "careers/career_with_skill_detail.html",
            {"request": request, "careers": career}
        )


@career_router.get("/{career_id}", response_class=HTMLResponse)
async def retrieve_one_career(
    request: Request,
    career_id: int, current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Retrieve a career for a given id."""
    if current_user:
        career = session.query(Career).filter(
            Career.id == career_id
        ).one_or_none()
        if not career:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Career does not exist"
            )
        return TEMPLATES.TemplateResponse(
            "careers/career_detail.html",
            {"request": request, "careers": career}
        )


@career_router.put("/{career_id}/update", response_class=HTMLResponse)
async def update_career(
    career_id: int, career: CareerUpdate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Update a career."""
    if current_user:
        get_career = session.query(Career).filter(Career.id == career_id)
        if get_career.one_or_none().user_id == current_user.id:
            get_career.update(**career.dict())
            session.commit()
            return get_career.one_or_none()
        elif get_career.one_or_none().user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career does not exist"
        )


@career_router.get("/show/update/{career_id}", response_class=HTMLResponse)
async def show_update_career_form(
    request: Request, career_id: int,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Show a form to update career."""
    if current_user.username == "tester":
        career = session.query(Career).filter(Career.id == career_id).first()
        return TEMPLATES.TemplateResponse(
            "careers/career_update.html",
            {"request": request, "course": career}
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


@career_router.delete("/{career_id}/delete", response_class=HTMLResponse)
async def delete_career(
    career_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Delete a career."""
    if current_user:
        career = session.query(Career).filter(Career.id == career_id)
        if career.first().user_id == current_user.id:
            career.delete()
            session.commit()
            return
        elif career.first().user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career does not exist"
        )


@career_router.get("/show/delete/{career_id}", response_class=HTMLResponse)
async def show_delete_career_form(
    request: Request, career_id: int,
    session: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Show a form to delete career."""
    if current_user.username == "tester":
        career = session.query(Career).filter(Career.id == career_id).first()
        return TEMPLATES.TemplateResponse(
            "careers/delete_career.html",
            {"request": request, "course": career}
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied"
    )


@career_router.post("/create", response_class=HTMLResponse)
async def create_career(
    career: CareerCreate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Create a new career."""
    if current_user:
        career.user_id = current_user.id
        new_career = Career(**career.dict())
        session.add(new_career)
        session.commit()
        if new_career:
            session.refresh(new_career)
            return new_career
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not create new career."
        )


@career_router.get("/show/create", response_class=HTMLResponse)
async def show_create_career_form(request: Request):
    """Show a form to create new career."""
    return TEMPLATES.TemplateResponse(
        "careers/create_career.html",
        {"request": request}
    )


@career_router.post(
    "/recommendation",
    response_class=HTMLResponse
)
async def create_recommendation(request: Request):
    """Create a new career recommendation."""
    # get Scores input
    form = await request.form()
    score_language = int(form.get('language'))
    score_mathematics = int(form.get('mathematic'))
    score_biology = int(form.get('biology'))
    score_chemistry = int(form.get('chemistry'))
    score_physics = int(form.get('physics'))
    score_social_science = int(form.get('social_science'))
    score_philosophy = int(form.get('philosophy'))
    score_english = int(form.get('english'))

    # create original output dict
    output_dict = dict()
    output_dict['score_language'] = score_language
    output_dict['score_mathematics'] = score_mathematics
    output_dict['score_biology'] = score_biology
    output_dict['score_chemistry'] = score_chemistry
    output_dict['score_physics'] = score_physics
    output_dict['score_social_science'] = score_social_science
    output_dict['score_philosophy'] = score_philosophy
    output_dict['score_english'] = score_english

    X = [
        score_language, score_mathematics, score_biology,
        score_chemistry, score_physics, score_social_science,
        score_philosophy, score_english
    ]
    # xx = qt.fit_transform(xx)
    # xx= xx.reshape(-1,1)
    print('------this is array data to predict-------')
    print('X = '+str(X))
    print('------------------------------------------')

    # pred = model.predict([x])[0]

    probs = model.predict([X])
    pred_class = np.argmax(probs)

    pred_class_name = class_names[pred_class]
    proba1 = int(probs[0][pred_class]*100)

    result = [pred_class_name, proba1]  # ,proba2,proba3,proba4,proba5]
    res = f'''
    Top Career based on the Career_Recommendation System is {pred_class_name}
    with probability of {int(probs[0][pred_class]*100)}%
    '''
    print(res)
    return TEMPLATES.TemplateResponse(
        "careers/Career_RS.html",
        {
            "request": request,
            "original_input": output_dict,
            "result": result
        }
    )


@career_router.get("/show/recommendation", response_class=HTMLResponse)
async def show_recommendation(request: Request):
    """Show recommendation form."""
    return TEMPLATES.TemplateResponse(
        "careers/Career_RS.html",
        {"request": request}
    )


@career_router.get("/show/report1", response_class=HTMLResponse)
async def show_report1(request: Request):
    """Return major reports."""
    return TEMPLATES.TemplateResponse(
        "careers/report1_major.html",
        {"request": request}
    )


@career_router.get("/show/report2", response_class=HTMLResponse)
async def show_report2(request: Request):
    """Return minor reports."""
    return TEMPLATES.TemplateResponse(
        "careers/report2_minor.html",
        {"request": request}
    )
