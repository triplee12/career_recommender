#!/usr/bin/python3
"""Database migration."""
from backend.api.db_config import engine
from .models.user_models import Base as User_Base
from .models.careers import Base as Career_Base
from .models.courses import Base as Courses_Base
from .models.enrollments import Base as Enrollments_Base
from .models.ratings import Base as Ratings_Base

User_Base.metadata.create_all(bind=engine)
Career_Base.metadata.create_all(bind=engine)
Courses_Base.metadata.create_all(bind=engine)
Enrollments_Base.metadata.create_all(bind=engine)
Ratings_Base.metadata.create_all(bind=engine)
