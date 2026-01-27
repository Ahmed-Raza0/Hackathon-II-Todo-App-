from sqlalchemy import text
from database import engine

def clear_all_users():
    """Delete all users and their associated data from the database"""
    with engine.connect() as conn:
        try:
            # First, delete all tasks (or other related data)
            print("🗑️  Deleting all tasks...")
            result_tasks = conn.execute(text('DELETE FROM "task"'))
            print(f"   Deleted {result_tasks.rowcount} task(s)")
            
            # Delete all messages if they exist
            try:
                result_messages = conn.execute(text('DELETE FROM "message"'))
                print(f"   Deleted {result_messages.rowcount} message(s)")
            except:
                pass
            
            # Delete all conversations if they exist
            try:
                result_conv = conn.execute(text('DELETE FROM "conversation"'))
                print(f"   Deleted {result_conv.rowcount} conversation(s)")
            except:
                pass
            
            # Now delete all users
            print("\n🗑️  Deleting all users...")
            result_users = conn.execute(text('DELETE FROM "user"'))
            print(f"   Deleted {result_users.rowcount} user(s)")
            
            conn.commit()
            print("\n✅ All data cleared successfully!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            conn.rollback()

if __name__ == "__main__":
    confirmation = input("⚠️  Delete ALL users and their data? (yes/no): ")
    if confirmation.lower() == 'yes':
        clear_all_users()
    else:
        print("❌ Cancelled.")