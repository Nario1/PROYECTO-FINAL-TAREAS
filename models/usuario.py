class Usuario:
    def __init__(self, id=None, nombre_usuario=None, contraseña=None):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña  # Ideal: hashear antes de guardar

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre_usuario={self.nombre_usuario})>"
