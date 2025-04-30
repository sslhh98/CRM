from extensions import db
db.engine.execute("DROP TABLE IF EXISTS _alembic_tmp_customer")
print("Temporary table dropped.")
