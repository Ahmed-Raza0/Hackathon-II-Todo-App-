from database import engine
from sqlmodel import SQLModel
from sqlalchemy import text

# Import ALL your models
from models.user import User

def reset_database():
    """Drop all tables and recreate them with the correct schema"""
    print("🗑️  Dropping all existing tables...")
    
    # Drop specific tables
    with engine.connect() as conn:
        try:
            conn.execute(text('DROP TABLE IF EXISTS "message" CASCADE;'))
            conn.execute(text('DROP TABLE IF EXISTS "conversation" CASCADE;'))
            conn.execute(text('DROP TABLE IF EXISTS "task" CASCADE;'))
            conn.execute(text('DROP TABLE IF EXISTS "tasks" CASCADE;'))
            conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE;'))
            conn.execute(text('DROP TABLE IF EXISTS "users" CASCADE;'))
            conn.execute(text('DROP TABLE IF EXISTS "alembic_version" CASCADE;'))
            conn.commit()
            print("✅ All tables dropped!")
        except Exception as e:
            print(f"Note: {e}")
    
    print("\n✅ Creating all tables with correct schema...")
    SQLModel.metadata.create_all(engine)
    
    print("\n🎉 Database reset complete!")
    
    # Verify
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\n📋 Tables created: {tables}")
    
    if 'user' in tables:
        columns = inspector.get_columns('user')
        print("\n👤 User table columns:")
        for col in columns:
            nullable = "NULL" if col.get('nullable', True) else "NOT NULL"
            print(f"  - {col['name']:<20} {str(col['type']):<20} {nullable}")

if __name__ == "__main__":
    confirmation = input("⚠️  WARNING: This will delete ALL data. Continue? (yes/no): ")
    if confirmation.lower() == 'yes':
        reset_database()
    else:
        print("❌ Cancelled.")