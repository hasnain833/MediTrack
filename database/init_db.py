from database.connection import Database
import os

def init_db():
    db = Database()
    schema_path = os.path.join('database', 'schema.sql')
    
    if not os.path.exists(schema_path):
        print(f"Error: {schema_path} not found.")
        return

    with open(schema_path, 'r') as f:
        sql = f.read()

    # Split by semicolon but ignore ones inside quotes/enums if any
    # A simple split is usually fine for schema files
    statements = sql.split(';')
    
    for statement in statements:
        cmd = statement.strip()
        if not cmd:
            continue
            
        print(f"Executing: {cmd[:60]}...")
        try:
            db.execute_query(cmd)
        except Exception as e:
            # Ignore errors for "USE database" if it's already used or "CREATE DATABASE" if it exists
            # though execute_query should handle them or they are 'IF NOT EXISTS'
            print(f"Statement failed: {e}")

    print("\nDatabase initialization complete.")

if __name__ == "__main__":
    init_db()
