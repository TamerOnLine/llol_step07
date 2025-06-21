# run.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from config.config_loader import load_env_config
from config.db_initializer import ensure_database_exists

from main import create_app
from main.extensions import db

# ✅ تحميل الإعدادات والتحقق من قاعدة البيانات
config = load_env_config()
ensure_database_exists()

# ✅ تهيئة التطبيق
app = create_app()

with app.app_context():
    db.create_all()
    print("✔️ Tables created (if not exist).")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=40514, debug=True)
