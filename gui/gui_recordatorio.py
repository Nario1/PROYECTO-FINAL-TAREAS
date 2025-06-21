import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from models.recordatorio import Recordatorio
from services.recordatorio_service import RecordatorioService


class RecordatorioGUI:
    """
    Interfaz gráfica para gestionar recordatorios vinculados a una tarea específica.
    Permite agregar, actualizar, eliminar y visualizar recordatorios.
    """

    def __init__(self, master, session, tarea_service, usuario_logueado, id_tarea):
        self.master = master
        self.session = session
        self.tarea_service = tarea_service
        self.usuario_logueado = usuario_logueado
        self.id_tarea = id_tarea
        self.recordatorio_service = RecordatorioService(session)
        self.recordatorios = []
        self.recordatorio_seleccionado = None

        self.tarea = self.tarea_service.obtener_por_id(self.id_tarea)

        self._construir_ui()
        self._cargar_lista()

    def _construir_ui(self):
        self.master.title("Gestor de Recordatorios")

        frm = ttk.Frame(self.master)
        frm.pack(padx=10, pady=10, fill='both', expand=True)

        ttk.Label(frm, text=f"Programar recordatorio de la tarea: {self.tarea.titulo}",
                  font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 10))

        self.btn_nuevo = ttk.Button(frm, text="Agregar nuevo recordatorio", command=self._limpiar)
        self.btn_nuevo.grid(row=1, column=0, columnspan=4, pady=5)

        ttk.Label(frm, text="Mensaje:").grid(row=2, column=0, sticky='e')
        self.entry_mensaje = ttk.Entry(frm, width=40)
        self.entry_mensaje.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frm, text="Fecha:").grid(row=3, column=0, sticky='e')
        self.date_fecha = DateEntry(frm, date_pattern='yyyy-mm-dd')
        self.date_fecha.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(frm, text="Hora (HH:MM):").grid(row=4, column=0, sticky='e')
        self.entry_hora = ttk.Entry(frm, width=10)
        self.entry_hora.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        frm_botones = ttk.Frame(frm)
        frm_botones.grid(row=5, column=0, columnspan=4, pady=10)

        self.btn_agregar = ttk.Button(frm_botones, text="Agregar", command=self._agregar)
        self.btn_agregar.pack(side='left', padx=5)

        self.btn_actualizar = ttk.Button(frm_botones, text="Actualizar", command=self._actualizar, state=tk.DISABLED)
        self.btn_actualizar.pack(side='left', padx=5)

        self.btn_eliminar = ttk.Button(frm_botones, text="Eliminar", command=self._eliminar, state=tk.DISABLED)
        self.btn_eliminar.pack(side='left', padx=5)

        self.btn_limpiar = ttk.Button(frm_botones, text="Limpiar", command=self._limpiar)
        self.btn_limpiar.pack(side='left', padx=5)

        self.tree = ttk.Treeview(frm, columns=("ID", "Mensaje", "FechaHora", "Mostrado"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Mensaje", text="Mensaje")
        self.tree.heading("FechaHora", text="Fecha y Hora")
        self.tree.heading("Mostrado", text="Mostrado")
        self.tree.column("ID", width=40)
        self.tree.column("Mensaje", width=200)
        self.tree.column("FechaHora", width=140)
        self.tree.column("Mostrado", width=80)
        self.tree.grid(row=6, column=0, columnspan=4, sticky='nsew')

        scrollbar = ttk.Scrollbar(frm, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=4, sticky='ns')

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _cargar_lista(self):
        self.tree.delete(*self.tree.get_children())
        self.recordatorios = self.recordatorio_service.obtener_por_tarea(self.id_tarea)
        for r in self.recordatorios:
            fecha_str = r.fecha_hora.strftime('%Y-%m-%d %H:%M') if r.fecha_hora else ''
            mostrado_str = "Sí" if r.mostrado else "No"
            self.tree.insert('', 'end', values=(r.id, r.mensaje, fecha_str, mostrado_str))

    def _validar_form(self):
        mensaje = self.entry_mensaje.get().strip()
        fecha = self.date_fecha.get()
        hora = self.entry_hora.get().strip()

        if not mensaje or not fecha or not hora:
            messagebox.showwarning("Validación", "Todos los campos son obligatorios.")
            return None
        try:
            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            if fecha_hora < datetime.now():
                messagebox.showwarning("Advertencia", "La fecha y hora deben ser futuras.")
                return None
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM en formato 24h.")
            return None

        return {
            "mensaje": mensaje,
            "fecha_hora": fecha_hora,
            "id_tarea": self.id_tarea
        }

    def _agregar(self):
        datos = self._validar_form()
        if not datos:
            return
        try:
            nuevo = Recordatorio(**datos)
            self.recordatorio_service.agregar(nuevo)
            messagebox.showinfo("Éxito", "Recordatorio agregado.")
            self._cargar_lista()
            self._limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")

    def _actualizar(self):
        if not self.recordatorio_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un recordatorio.")
            return
        datos = self._validar_form()
        if not datos:
            return
        try:
            for k, v in datos.items():
                setattr(self.recordatorio_seleccionado, k, v)
            self.recordatorio_service.editar(self.recordatorio_seleccionado)
            messagebox.showinfo("Éxito", "Recordatorio actualizado.")
            self._cargar_lista()
            self._limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def _eliminar(self):
        if not self.recordatorio_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un recordatorio.")
            return
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este recordatorio?"):
            try:
                self.recordatorio_service.eliminar(self.recordatorio_seleccionado.id)
                messagebox.showinfo("Éxito", "Recordatorio eliminado.")
                self._cargar_lista()
                self._limpiar()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def _on_select(self, _):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        item = self.tree.item(seleccion[0])
        rid = item["values"][0]
        recordatorio = next((r for r in self.recordatorios if r.id == rid), None)
        if not recordatorio:
            return
        self.recordatorio_seleccionado = recordatorio
        self.entry_mensaje.delete(0, tk.END)
        self.entry_mensaje.insert(0, recordatorio.mensaje)
        try:
            self.date_fecha.set_date(recordatorio.fecha_hora.date())
            self.entry_hora.delete(0, tk.END)
            self.entry_hora.insert(0, recordatorio.fecha_hora.strftime('%H:%M'))
        except Exception:
            pass

        self.btn_agregar.config(state=tk.DISABLED)
        self.btn_actualizar.config(state=tk.NORMAL)
        self.btn_eliminar.config(state=tk.NORMAL)

    def _limpiar(self):
        self.entry_mensaje.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.date_fecha.set_date(datetime.today())
        self.recordatorio_seleccionado = None
        self.btn_agregar.config(state=tk.NORMAL)
        self.btn_actualizar.config(state=tk.DISABLED)
        self.btn_eliminar.config(state=tk.DISABLED)
        self.tree.selection_remove(self.tree.selection())
        self.entry_mensaje.focus()
