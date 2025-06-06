from repositories.tarea_repo import TareaRepo
from models.tarea import Tarea

class TareaService:
    def __init__(self, db_path):
        self.tarea_repo = TareaRepo(db_path)

    def agregar_tarea(self, tarea: Tarea):
        return self.tarea_repo.crear_tarea(tarea)

    def editar_tarea(self, tarea: Tarea):
        self.tarea_repo.actualizar_tarea(tarea)

    def eliminar_tarea(self, id_tarea):
        self.tarea_repo.eliminar_tarea(id_tarea)

    def listar_tareas(self, id_usuario):
        return self.tarea_repo.obtener_tareas_por_usuario(id_usuario)

    def buscar_tareas(self, id_usuario, titulo):
        return self.tarea_repo.buscar_tarea_por_titulo(id_usuario, titulo)

    def marcar_completada(self, id_tarea):
        self.tarea_repo.marcar_completada(id_tarea)
