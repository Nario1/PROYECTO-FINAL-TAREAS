# utils/recordatorio_notificador.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class RecordatorioNotificador:
    def __init__(self, master, session, recordatorio_service, tarea_service, usuario_logueado):
        self.master = master
        self.session = session
        self.recordatorio_service = recordatorio_service
        self.tarea_service = tarea_service
        self.usuario_logueado = usuario_logueado
        self._iniciar_revision()

    def _iniciar_revision(self):
        def revisar():
            ahora = datetime.now()
            recordatorios = self.recordatorio_service.obtener_no_mostrados_por_usuario(self.usuario_logueado.id)
            for r in recordatorios:
                if r.fecha_hora <= ahora:
                    tarea = self.tarea_service.obtener_por_id(r.id_tarea)
                    messagebox.showinfo("🔔 Recordatorio", f"Tarea: {tarea.titulo}\n\n{r.mensaje}")
                    r.mostrado = True
                    self.session.commit()
            self.master.after(60000, revisar)  # Revisa cada minuto

        self.master.after(1000, revisar)
