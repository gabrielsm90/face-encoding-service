import os


os.environ["POSTGRES_ROOT_PASSWORD"] = "integration-tests"
os.environ["POSTGRES_DB_NAME"] = "face-encoding-it"
os.environ["POSTGRES_PORT"] = "5433"
os.environ["POSTGRES_HOST"] = "localhost"
