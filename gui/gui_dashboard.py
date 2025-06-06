import tkinter as tk
from tkinter import messagebox, ttk
from models.tarea import Tarea
from services.tarea_service import TareaService
from datetime import datetime

class DashboardGUI:
    def __init__(self, master, db_path, usuario_logueado):
        self.master = master
        self.master.title(f"Dashboard - Usuario: {usuario_logueado}")
        self.tarea_service = TareaService(db_path)
        self.usuario_logueado = usuario_logueado

        self.id_usuario = None  # Lo debes obtener a partir del usuario_logueado
        # Para simplificar, aquí solo el nombre del usuario; en producción, usar el id real
        # Para eso tendrías que pasar el id desde login o hacer consulta.

        self.frame_form = tk.Frame(self.master)
        self.frame_form.pack(padx=10, pady=10, fill='x')

        # Campos del formulario
        tk.Label(self.frame_form, text="Título:").grid(row=0, column=0, sticky="e")
        self.entry_titulo = tk.Entry(self.frame_form)
        self.entry_titulo.grid(row=0, column=1, sticky="we")

        tk.Label(self.frame_form, text="Descripción:").grid(row=1, column=0, sticky="e")
        self.entry_descripcion = tk.Entry(self.frame_form)
        self.entry_descripcion.grid(row=1, column=1, sticky="we")

        tk.Label(self.frame_form, text="Fecha Vencimiento (YYYY-MM-DD):").grid(row=2, column=0, sticky="e")
        self.entry_fecha = tk.Entry(self.frame_form)
        self.entry_fecha.grid(row=2, column=1, sticky="we")

        tk.Label(self.frame_form, text="Prioridad:").grid(row=3, column=0, sticky="e")
        self.combo_prioridad = ttk.Combobox(self.frame_form, values=['baja', 'media', 'alta'], state="readonly")
        self.combo_prioridad.current(1)
        self.combo_prioridad.grid(row=3, column=1, sticky="we")

        tk.Label(self.frame_form, text="Estado:").grid(row=4, column=0, sticky="e")
        self.combo_estado = ttk.Combobox(self.frame_form, values=['pendiente', 'completada', 'archivada'], state="readonly")
        self.combo_estado.current(0)
        self.combo_estado.grid(row=4, column=1, sticky="we")

        tk.Label(self.frame_form, text="Recurrente:").grid(row=5, column=0, sticky="e")
        self.var_recurrente = tk.IntVar()
        self.check_recurrente = tk.Checkbutton(self.frame_form, variable=self.var_recurrente)
        self.check_recurrente.grid(row=5, column=1, sticky="w")

        tk.Label(self.frame_form, text="Frecuencia (dias):").grid(row=6, column=0, sticky="e")
        self.entry_frecuencia = tk.Entry(self.frame_form)
        self.entry_frecuencia.grid(row=6, column=1, sticky="we")

        # Botones
        self.btn_agregar = tk.Button(self.frame_form, text="Agregar", command=self.agregar_tarea)
        self.btn_agregar.grid(row=7, column=0, pady=5)

        self.btn_actualizar = tk.Button(self.frame_form, text="Actualizar", command=self.actualizar_tarea, state=tk.DISABLED)
        self.btn_actualizar.grid(row=7, column=1, pady=5)

        self.btn_eliminar = tk.Button(self.frame_form, text="Eliminar", command=self.eliminar_tarea, state=tk.DISABLED)
        self.btn_eliminar.grid(row=8, column=0, pady=5)

        self.btn_limpiar = tk.Button(self.frame_form, text="Limpiar", command=self.limpiar_formulario)
        self.btn_limpiar.grid(row=8, column=1, pady=5)

        # Lista de tareas
        self.tree = ttk.Treeview(self.master, columns=("id", "titulo", "estado", "prioridad", "fecha"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("prioridad", text="Prioridad")
        self.tree.heading("fecha", text="Fecha Vencimiento")
        self.tree.column("id", width=30)
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.cargar_tarea_seleccionada)

        self.tareas = []
        self.tarea_seleccionada = None

        # Inicializar: cargar usuario y tareas
        self.cargar_id_usuario()
        self.cargar_tareas()

    def cargar_id_usuario(self):
        # Aquí debes cargar el id real del usuario a partir del nombre
        # Ejemplo simplificado: usar un repo para obtener id
        from repositories.usuario_repo import UsuarioRepo
        repo = UsuarioRepo(self.tarea_service.tarea_repo.db_path)
        usuario = repo.obtener_por_nombre(self.usuario_logueado)
        if usuario:
            self.id_usuario = usuario.id
        else:
            messagebox.showerror("Error", "Usuario no encontrado en la base de datos.")
            self.master.destroy()

    def cargar_tareas(self):
        if self.id_usuario:
            self.tareas = self.tarea_service.listar_tareas(self.id_usuario)
            self._llenar_treeview()

    def _llenar_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for tarea in self.tareas:
            self.tree.insert('', 'end', values=(
                tarea.id, tarea.titulo, tarea.estado, tarea.prioridad, tarea.fecha_vencimiento
            ))

    def agregar_tarea(self):
        titulo = self.entry_titulo.get().strip()
        if not titulo:
            messagebox.showwarning("Validación", "El título es obligatorio.")
            return
        descripcion = self.entry_descripcion.get().strip()
        fecha = self.entry_fecha.get().strip()
        if fecha:
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Validación", "Formato de fecha inválido (YYYY-MM-DD).")
                return
        prioridad = self.combo_prioridad.get()
        estado = self.combo_estado.get()
        recurrente = self.var_recurrente.get()
        frecuencia = self.entry_frecuencia.get().strip() if recurrente else None

        tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_vencimiento=fecha,
            estado=estado,
            prioridad=prioridad,
            recurrente=recurrente,
            frecuencia_recurrencia=frecuencia,
            id_usuario_creador=self.id_usuario
        )
        self.tarea_service.agregar_tarea(tarea)
        messagebox.showinfo("Éxito", "Tarea agregada correctamente.")
        self.cargar_tareas()
        self.limpiar_formulario()

    def cargar_tarea_seleccionada(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        tarea_id = item['values'][0]
        tarea = next((t for t in self.tareas if t.id == tarea_id), None)
        if tarea:
            self.tarea_seleccionada = tarea
            self.entry_titulo.delete(0, tk.END)
            self.entry_titulo.insert(0, tarea.titulo)

            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, tarea.descripcion or '')

            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, tarea.fecha_vencimiento or '')

            self.combo_prioridad.set(tarea.prioridad)
            self.combo_estado.set(tarea.estado)

            self.var_recurrente.set(tarea.recurrente)
            self.entry_frecuencia.delete(0, tk.END)
            self.entry_frecuencia.insert(0, tarea.frecuencia_recurrencia or '')

            self.btn_actualizar.config(state=tk.NORMAL)
            self.btn_eliminar.config(state=tk.NORMAL)
            self.btn_agregar.config(state=tk.DISABLED)

    def actualizar_tarea(self):
        if not self.tarea_seleccionada:
            return

        titulo = self.entry_titulo.get().strip()
        if not titulo:
            messagebox.showwarning("Validación", "El título es obligatorio.")
            return
        descripcion = self.entry_descripcion.get().strip()
        fecha = self.entry_fecha.get().strip()
        if fecha:
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Validación", "Formato de fecha inválido (YYYY-MM-DD).")
                return
        prioridad = self.combo_prioridad.get()
        estado = self.combo_estado.get()
        recurrente = self.var_recurrente.get()
        frecuencia = self.entry_frecuencia.get().strip() if recurrente else None

        tarea = self.tarea_seleccionada
        tarea.titulo = titulo
        tarea.descripcion = descripcion
        tarea.fecha_vencimiento = fecha
        tarea.prioridad = prioridad
        tarea.estado = estado
        tarea.recurrente = recurrente
        tarea.frecuencia_recurrencia = frecuencia

        self.tarea_service.editar_tarea(tarea)
        messagebox.showinfo("Éxito", "Tarea actualizada correctamente.")
        self.cargar_tareas()
        self.limpiar_formulario()

    def eliminar_tarea(self):
        if not self.tarea_seleccionada:
            return
        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta tarea?")
        if confirm:
            self.tarea_service.eliminar_tarea(self.tarea_seleccionada.id)
            messagebox.showinfo("Éxito", "Tarea eliminada correctamente.")
            self.cargar_tareas()
            self.limpiar_formulario()

    def limpiar_formulario(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.combo_prioridad.current(1)
        self.combo_estado.current(0)
        self.var_recurrente.set(0)
        self.entry_frecuencia.delete(0, tk.END)
        self.btn_actualizar.config(state=tk.DISABLED)
        self.btn_eliminar.config(state=tk.DISABLED)
        self.btn_agregar.config(state=tk.NORMAL)
        self.tarea_seleccionada = None
