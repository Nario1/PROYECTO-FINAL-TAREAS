# tests/test_usuario.py
from services.usuario_service import UsuarioService
from models.usuario import Usuario

def test_registrar_usuario(db_session):
    service = UsuarioService(db_session)
    success, message = service.registrar_usuario("testuser", "123")
    assert success
    assert message == "Usuario registrado exitosamente."

def test_login_valido(db_session):
    service = UsuarioService(db_session)
    service.registrar_usuario("testuser2", "123")
    assert service.validar_login("testuser2", "123") is True

def test_login_invalido(db_session):
    service = UsuarioService(db_session)
    service.registrar_usuario("testuser3", "123")
    assert service.validar_login("testuser3", "wrongpass") is False
