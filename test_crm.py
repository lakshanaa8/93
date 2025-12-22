import psycopg2

def test_crm():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="crm_db",
            user="postgres",
            password="abcd"  # replace with your PostgreSQL password
        )
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()
        print("Tables in crm_db:", tables)
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_crm()
