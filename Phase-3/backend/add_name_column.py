from sqlalchemy import text
from database import engine

def add_name_column():
    with engine.connect() as conn:
        try:
            # Add the name column
            conn.execute(text('ALTER TABLE "user" ADD COLUMN name VARCHAR NOT NULL DEFAULT \'\''))
            conn.commit()
            print("Column 'name' added successfully!")
        except Exception as e:
            print(f"Error: {e}")
            print("Column might already exist or there's another issue.")

if __name__ == "__main__":
    add_name_column()