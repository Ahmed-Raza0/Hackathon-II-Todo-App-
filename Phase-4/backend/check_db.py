from sqlalchemy import inspect
from database import engine

inspector = inspect(engine)

# Get all tables
tables = inspector.get_table_names()
print("Tables:", tables)

# Get columns for user table
if 'user' in tables:
    columns = inspector.get_columns('user')
    print("\nUser table columns:")
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")