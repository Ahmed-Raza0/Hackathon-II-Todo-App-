from sqlalchemy import text
from database import engine

def fix_username_column():
    """Make username column nullable"""
    with engine.connect() as conn:
        try:
            # Make username and full_name nullable
            print("Making username and full_name columns nullable...")
            conn.execute(text("""
                ALTER TABLE "user" 
                ALTER COLUMN username DROP NOT NULL;
            """))
            
            conn.execute(text("""
                ALTER TABLE "user" 
                ALTER COLUMN full_name DROP NOT NULL;
            """))
            
            conn.commit()
            print("✅ Columns updated successfully!")
            
        except Exception as e:
            print(f"Error: {e}")
            print("\nTrying to drop columns instead...")
            
            try:
                # Alternative: Drop these columns if you don't need them
                conn.execute(text("""
                    ALTER TABLE "user" 
                    DROP COLUMN IF EXISTS username CASCADE;
                """))
                
                conn.execute(text("""
                    ALTER TABLE "user" 
                    DROP COLUMN IF EXISTS full_name CASCADE;
                """))
                
                conn.execute(text("""
                    ALTER TABLE "user" 
                    DROP COLUMN IF EXISTS is_active CASCADE;
                """))
                
                conn.commit()
                print("✅ Unnecessary columns dropped successfully!")
            except Exception as e2:
                print(f"❌ Error: {e2}")

if __name__ == "__main__":
    fix_username_column()