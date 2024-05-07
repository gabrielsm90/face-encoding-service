import uvicorn

from src.app import app
from src.db import engine, Base


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8001)
