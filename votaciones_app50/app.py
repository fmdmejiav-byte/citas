
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import *

# --- Crear tablas y datos iniciales si no existen ---
def init_db():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS puestos_votacion (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre_puesto VARCHAR(100),
        direccion VARCHAR(100)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ciudadanos (
        identificacion VARCHAR(20) PRIMARY KEY,
        nombre VARCHAR(100),
        puesto_id INT,
        FOREIGN KEY (puesto_id) REFERENCES puestos_votacion(id)
    )''')
    # Insertar datos solo si la tabla está vacía
    cursor.execute('SELECT COUNT(*) FROM puestos_votacion')
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            'INSERT INTO puestos_votacion (nombre_puesto, direccion) VALUES (%s, %s)',
            [
                ('Colegio Central','Calle 10 #15-20'),
                ('Escuela Nacional','Carrera 8 #20-30'),
                ('Universidad Publica','Avenida 30 #45-10')
            ]
        )
    conn.commit()
    cursor.close()
    conn.close()



app = Flask(__name__)
init_db()

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, nombre_puesto FROM puestos_votacion')
    puestos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('registro.html', puestos=puestos)

@app.route('/consulta')
def consulta():
    return render_template('consulta.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form.get('nombre')
    doc = request.form.get('numeroDocumento')
    puesto_id = request.form.get('puesto_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ciudadanos (identificacion, nombre, puesto_id) VALUES (%s, %s, %s)",
        (doc, nombre, puesto_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/buscar', methods=['POST'])
def buscar():
    doc = request.form.get('numeroDocumento')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT c.nombre, c.identificacion, p.nombre_puesto, p.direccion 
        FROM ciudadanos c 
        JOIN puestos_votacion p ON c.puesto_id = p.id 
        WHERE c.identificacion = %s
    """
    cursor.execute(query, (doc,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if usuario:
        return render_template('resultado.html', ciudadano=usuario)
    return "<h2>Usuario no encontrado</h2><a href='/consulta'>Volver</a>"

if __name__ == '__main__':
    app.run(debug=True, port=5500, host='127.0.0.1')