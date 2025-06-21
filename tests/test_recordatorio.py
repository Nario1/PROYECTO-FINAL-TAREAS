from services.tarea_service import TareaService
from services.recordatorio_service import RecordatorioService
from models.tarea import Tarea
from models.recordatorio import Recordatorio
from datetime import datetime, timedelta

def test_agregar_recordatorio(db_session):
    tarea_service = TareaService(db_session)
    recordatorio_service = RecordatorioService(db_session)

    tarea = Tarea(titulo="Prueba", descripcion="...", id_usuario_creador=1)
    tarea_creada = tarea_service.agregar_tarea(tarea)

    rec = Recordatorio(mensaje="No olvidar", fecha_hora=datetime.now() + timedelta(hours=1), id_tarea=tarea_creada.id)
    nuevo = recordatorio_service.agregar(rec)
    assert nuevo.id is not None
    assert nuevo.mensaje == "No olvidar"

def test_listar_recordatorios(db_session):
    tarea_service = TareaService(db_session)
    recordatorio_service = RecordatorioService(db_session)

    tarea = Tarea(titulo="Revisar", descripcion="...", id_usuario_creador=1)
    tarea_creada = tarea_service.agregar_tarea(tarea)

    rec1 = Recordatorio(mensaje="R1", fecha_hora=datetime.now() + timedelta(hours=2), id_tarea=tarea_creada.id)
    rec2 = Recordatorio(mensaje="R2", fecha_hora=datetime.now() + timedelta(hours=3), id_tarea=tarea_creada.id)
    recordatorio_service.agregar(rec1)
    recordatorio_service.agregar(rec2)

    recordatorios = recordatorio_service.obtener_por_tarea(tarea_creada.id)
    assert len(recordatorios) == 2
