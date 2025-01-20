import psycopg2
def get_db_connection():
    conexion = psycopg2.connect(
        host="localhost",
        database="BELLKYCOSMETIC",
        user="postgres",
        password="76133609"
        )
    try:
        conection = psycopg2.connect(conexion)
        return conection
    except Exception as e:
        print(f"Error al conectar a la basededatos:{e}")

    return conexion 

