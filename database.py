import sqlite3

def crear_bd_y_tablas(db_path="database.db"):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                fecha_vencimiento TEXT,
                estado TEXT DEFAULT 'pendiente',
                prioridad TEXT DEFAULT 'media',
                recurrente INTEGER DEFAULT 0,
                frecuencia_recurrencia TEXT,
                id_usuario_creador INTEGER NOT NULL,
                FOREIGN KEY(id_usuario_creador) REFERENCES usuarios(id)
            )
        ''')
        conn.commit()
