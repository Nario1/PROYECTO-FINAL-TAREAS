import sqlite3
from models.tarea import Tarea

class TareaRepo:
    def __init__(self, db_path):
        self.db_path = db_path
        self._crear_tabla()

    def _crear_tabla(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
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

    def crear_tarea(self, tarea: Tarea):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tareas (titulo, descripcion, fecha_vencimiento, estado, prioridad,
                recurrente, frecuencia_recurrencia, id_usuario_creador)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tarea.titulo, tarea.descripcion, tarea.fecha_vencimiento, tarea.estado,
                tarea.prioridad, tarea.recurrente, tarea.frecuencia_recurrencia, tarea.id_usuario_creador
            ))
            conn.commit()
            tarea.id = cursor.lastrowid
            return tarea

    def actualizar_tarea(self, tarea: Tarea):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tareas SET titulo=?, descripcion=?, fecha_vencimiento=?, estado=?,
                prioridad=?, recurrente=?, frecuencia_recurrencia=? WHERE id=?
            ''', (
                tarea.titulo, tarea.descripcion, tarea.fecha_vencimiento, tarea.estado,
                tarea.prioridad, tarea.recurrente, tarea.frecuencia_recurrencia, tarea.id
            ))
            conn.commit()

    def eliminar_tarea(self, id_tarea):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tareas WHERE id=?', (id_tarea,))
            conn.commit()

    def obtener_tareas_por_usuario(self, id_usuario):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tareas WHERE id_usuario_creador=?', (id_usuario,))
            rows = cursor.fetchall()
            tareas = []
            for row in rows:
                tarea = Tarea(
                    id=row[0], titulo=row[1], descripcion=row[2], fecha_vencimiento=row[3],
                    estado=row[4], prioridad=row[5], recurrente=row[6], frecuencia_recurrencia=row[7],
                    id_usuario_creador=row[8]
                )
                tareas.append(tarea)
            return tareas

    def buscar_tarea_por_titulo(self, id_usuario, titulo):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM tareas WHERE id_usuario_creador=? AND titulo LIKE ?
            ''', (id_usuario, f'%{titulo}%'))
            rows = cursor.fetchall()
            tareas = []
            for row in rows:
                tarea = Tarea(
                    id=row[0], titulo=row[1], descripcion=row[2], fecha_vencimiento=row[3],
                    estado=row[4], prioridad=row[5], recurrente=row[6], frecuencia_recurrencia=row[7],
                    id_usuario_creador=row[8]
                )
                tareas.append(tarea)
            return tareas

    def marcar_completada(self, id_tarea):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE tareas SET estado="completada" WHERE id=?', (id_tarea,))
            conn.commit()
