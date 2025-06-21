from sqlalchemy.orm import Session, joinedload
from models.recordatorio import Recordatorio
from typing import Optional, List

class RecordatorioRepo:
    """
    Repositorio para operaciones CRUD sobre recordatorios.
    """

    def __init__(self, session: Session):
        self.session = session

    def crear_recordatorio(self, rec: Recordatorio) -> Recordatorio:
        self.session.add(rec)
        self.session.commit()
        self.session.refresh(rec)
        return rec

    def actualizar_recordatorio(self, rec: Recordatorio) -> Recordatorio:
        self.session.merge(rec)
        self.session.commit()
        return rec

    def eliminar_recordatorio(self, id_rec: int) -> None:
        rec = self.session.get(Recordatorio, id_rec)
        if rec:
            self.session.delete(rec)
            self.session.commit()

    def obtener_primero_por_tarea(self, id_tarea: int) -> Optional[Recordatorio]:
        return self.session.query(Recordatorio).filter_by(id_tarea=id_tarea).first()

    def obtener_por_tarea(self, id_tarea: int) -> List[Recordatorio]:
        return self.session.query(Recordatorio).filter_by(id_tarea=id_tarea).all()

    def listar_por_tarea(self, id_tarea: int) -> List[Recordatorio]:
        return self.session.query(Recordatorio) \
            .options(joinedload(Recordatorio.tarea)) \
            .filter_by(id_tarea=id_tarea).all()
