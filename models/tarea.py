class Tarea:
    def __init__(self, id=None, titulo=None, descripcion=None, fecha_vencimiento=None,
                 estado='pendiente', prioridad='media', recurrente=0, frecuencia_recurrencia=None,
                 id_usuario_creador=None):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento  # 'YYYY-MM-DD'
        self.estado = estado  # 'pendiente', 'completada', 'archivada'
        self.prioridad = prioridad  # 'baja', 'media', 'alta'
        self.recurrente = recurrente  # 0 o 1
        self.frecuencia_recurrencia = frecuencia_recurrencia
        self.id_usuario_creador = id_usuario_creador

    def __repr__(self):
        return f"<Tarea(id={self.id}, titulo={self.titulo}, estado={self.estado})>"
