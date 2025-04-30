import sqlite3
import os

# Eğer veritabanınız instance klasöründeyse:
db_path = os.path.join("instance", "crm.db")
# Ya da doğrudan:
# db_path = "C:\\Users\\ssonk\\OneDrive\\Masaüstü\\crm_project\\instance\\crm.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("DELETE FROM alembic_version;")
conn.commit()
conn.close()

print(f"'{db_path}' içindeki alembic_version kaydı temizlendi.")
