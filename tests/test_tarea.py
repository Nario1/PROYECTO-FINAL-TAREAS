from services.tarea_service import TareaService
from models.tarea import Tarea

def test_agregar_tarea(db_session):
    service = TareaService(db_session)
    nueva = Tarea(titulo="Estudiar", descripcion="Repasar para el examen", id_usuario_creador=1)
    tarea_creada = service.agregar_tarea(nueva)
    assert tarea_creada.id is not None
    assert tarea_creada.titulo == "Estudiar"

def test_listar_tareas(db_session):
    service = TareaService(db_session)
    t1 = Tarea(titulo="Tarea A", descripcion="A", id_usuario_creador=1)
    t2 = Tarea(titulo="Tarea B", descripcion="B", id_usuario_creador=1)
    service.agregar_tarea(t1)
    service.agregar_tarea(t2)
    tareas = service.listar_tareas(1)
    assert len(tareas) == 2
