from typing import List
from sqlalchemy.orm import Session
from repositories.tarea_repo import TareaRepo
from repositories.recordatorio_repo import RecordatorioRepo
from models.tarea import Tarea
from models.recordatorio import Recordatorio

class TareaService:
    """
    Servicio que gestiona la lógica de negocio relacionada con tareas y recordatorios.
    """

    def __init__(self, session: Session):
        self.session = session
        self.repo = TareaRepo(session)
        self.recordatorio_repo = RecordatorioRepo(session)

    # --- Métodos para TAREAS ---

    def agregar_tarea(self, tarea: Tarea) -> Tarea:
        return self.repo.crear_tarea(tarea)

    def editar_tarea(self, tarea: Tarea) -> None:
        self.repo.actualizar_tarea(tarea)

    def eliminar_tarea(self, id_tarea: int) -> None:
        self.repo.eliminar_tarea(id_tarea)

    def listar_tareas(self, id_usuario: int) -> List[Tarea]:
        return self.repo.obtener_tareas_por_usuario(id_usuario)

    def buscar_tareas(self, id_usuario: int, titulo: str) -> List[Tarea]:
        return self.repo.buscar_tarea_por_titulo(id_usuario, titulo)

    def marcar_completada(self, id_tarea: int) -> None:
        self.repo.marcar_completada(id_tarea)

    def obtener_por_id(self, id_tarea: int) -> Tarea:
        return self.session.query(Tarea).filter_by(id=id_tarea).first()

    # --- Métodos para RECORDATORIOS ---

    def agregar_recordatorio(self, recordatorio: Recordatorio) -> Recordatorio:
        return self.recordatorio_repo.crear_recordatorio(recordatorio)

    def eliminar_recordatorio(self, recordatorio_id: int) -> None:
        self.recordatorio_repo.eliminar_recordatorio(recordatorio_id)

    def obtener_recordatorios_por_tarea(self, tarea_id: int) -> List[Recordatorio]:
        return self.recordatorio_repo.obtener_por_tarea(tarea_id)
