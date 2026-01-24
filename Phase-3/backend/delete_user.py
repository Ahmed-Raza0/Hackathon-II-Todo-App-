from sqlalchemy import text
from database import engine

def delete_user_by_email(email: str):
    """Delete a user by email"""
    with engine.connect() as conn:
        try:
            result = conn.execute(
                text('DELETE FROM "user" WHERE email = :email'),
                {"email": email}
            )
            conn.commit()
            print(f"✅ Deleted user with email: {email}")
            print(f"   Rows affected: {result.rowcount}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    email = input("Enter email to delete: ")
    delete_user_by_email(email)