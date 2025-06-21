from services.usuario_service import UsuarioService
from services.tarea_service import TareaService
from services.recordatorio_service import RecordatorioService
from models.usuario import Usuario
from models.tarea import Tarea
from models.recordatorio import Recordatorio
from datetime import datetime, timedelta

def test_flujo_completo(db_session):
    # Registro e inicio de sesión
    usuario_service = UsuarioService(db_session)
    exito, _ = usuario_service.registrar_usuario("aceptacion", "clave")
    assert exito

    usuario = db_session.query(Usuario).filter_by(nombre_usuario="aceptacion").first()

    # Crear tarea
    tarea_service = TareaService(db_session)
    tarea = Tarea(titulo="Tarea de prueba", descripcion="Desc", id_usuario_creador=usuario.id)
    tarea_creada = tarea_service.agregar_tarea(tarea)
    assert tarea_creada.id is not None

    # Crear recordatorio
    recordatorio_service = RecordatorioService(db_session)
    rec = Recordatorio(mensaje="¡Hazlo ya!", fecha_hora=datetime.now() + timedelta(minutes=30), id_tarea=tarea_creada.id)
    recordatorio_creado = recordatorio_service.agregar(rec)
    assert recordatorio_creado.id is not None

    # Verificar recordatorios por tarea
    r_list = recordatorio_service.obtener_por_tarea(tarea_creada.id)
    assert len(r_list) == 1
    assert r_list[0].mensaje == "¡Hazlo ya!"
