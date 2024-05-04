import uvicorn

from src.app import app
from src.models import Base
from src.db import engine


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
