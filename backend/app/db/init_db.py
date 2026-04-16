from app.db.database import engine
from app.models.review_models import Base


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
