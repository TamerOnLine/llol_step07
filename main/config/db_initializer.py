import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config.config_loader import load_env_config

# تحميل الإعدادات من ملف .env
config = load_env_config()
DB_NAME = config["DB_NAME"]
DB_USER = config["DB_USER"]
DB_PASSWORD = config["DB_PASSWORD"]
DB_HOST = config["DB_HOST"]

def ensure_database_exists():
    try:
        print(f"🧪 Connecting to default admin database 'postgres' to check/create '{DB_NAME}'...")
        conn = psycopg2.connect(
            dbname="postgres",  # ← قاعدة التحكم
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"✅ Database '{DB_NAME}' created successfully.")
        else:
            print(f"✅ Database '{DB_NAME}' already exists.")

        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Failed to verify or create the database:")
        print(e)
