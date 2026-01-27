from sqlalchemy import text
from database import engine

def list_all_users():
    """List all users in the database"""
    with engine.connect() as conn:
        result = conn.execute(text('SELECT id, email, name, created_at FROM "user"'))
        users = result.fetchall()
        
        if users:
            print(f"\n📋 Found {len(users)} user(s):\n")
            for user in users:
                print(f"  ID: {user[0]}")
                print(f"  Email: {user[1]}")
                print(f"  Name: {user[2]}")
                print(f"  Created: {user[3]}")
                print("-" * 50)
        else:
            print("No users found in database.")

if __name__ == "__main__":
    list_all_users()