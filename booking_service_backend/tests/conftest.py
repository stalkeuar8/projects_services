# import os
# import sys
# from pathlib import Path

# # Ensure the project root is on sys.path when running tests.
# # This makes it possible to import the `app` package from tests.
# ROOT_DIR = Path(__file__).resolve().parents[1]
# if str(ROOT_DIR) not in sys.path:
#     sys.path.insert(0, str(ROOT_DIR))

# # Prefer using a real Postgres database if provided via environment variable.
# # Example: TEST_DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db
# os.environ.setdefault(
#     "TEST_DATABASE_URL",
#     "postgresql+asyncpg://user:pass@localhost:5432/db",
# )
