import os


def get_env(var_name: str, default: str):
    return default if (env_var := os.getenv(var_name)) is None else env_var


DB_NAME = "skagit60"
TEST_DB_NAME = "skagit60_test_db"
DB_SERVER = get_env("DB_SERVER", "localhost")

MAX_DB_QUERY = 100
SECRET_KEY = get_env("SECRET_KEY", "testing_key")
