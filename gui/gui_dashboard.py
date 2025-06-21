import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from tkcalendar import DateEntry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.tarea import Tarea
from services.tarea_service import TareaService
from services.recordatorio_service import RecordatorioService
from repositories.usuario_repo import UsuarioRepo
from gui.gui_recordatorio import RecordatorioGUI


class DashboardGUI:
    def __init__(self, master, db_path, usuario_logueado):
        self.master = master
        self.master.title(f"Dashboard — {usuario_logueado}")

        engine = create_engine(f"sqlite:///{db_path}")
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.tarea_service = TareaService(self.session)
        self.recordatorio_service = RecordatorioService(self.session)
        self.recordatorios_notificados = set()
        self.usuario_logueado = usuario_logueado
        self.db_path = db_path

        self.id_usuario = None
        self.usuario_logueado_obj = None
        self.tareas = []
        self.tarea_seleccionada = None

        self._construir_ui()
        self._cargar_id_usuario()
        self._actualizar_lista()
        self._verificar_recordatorios()

    def _verificar_recordatorios(self):
        ahora = datetime.now()
        if not self.usuario_logueado_obj:
            return

        recordatorios = self.recordatorio_service.obtener_por_usuario(self.usuario_logueado_obj.id)
        for r in recordatorios:
            if r.fecha_hora <= ahora and r.id not in self.recordatorios_notificados:
                self._mostrar_popup_recordatorio(r.tarea.titulo, r.mensaje)
                r.mostrado = True
                self.recordatorio_service.actualizar_recordatorio(r)
                self.recordatorios_notificados.add(r.id)

        self.master.after(5000, self._verificar_recordatorios)

    def _mostrar_popup_recordatorio(self, titulo_tarea, mensaje):
        popup = tk.Toplevel(self.master)
        popup.title("¡Recordatorio!")
        popup.attributes('-topmost', True)
        popup.geometry("300x150")
        popup.resizable(False, False)
        ttk.Label(popup, text=f"Tarea: {titulo_tarea}", font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Label(popup, text=mensaje, wraplength=280).pack(pady=10)
        ttk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)

    from tkcalendar import DateEntry  # Asegúrate de tener esta importación arriba en tu archivo

    def _construir_ui(self):
        frm_top = ttk.Frame(self.master)
        frm_top.pack(fill='x', padx=10, pady=5)

        self.entry_buscar = ttk.Entry(frm_top)
        self.entry_buscar.pack(side='left', expand=True, fill='x')
        ttk.Button(frm_top, text="Buscar", command=self._buscar).pack(side='left', padx=5)
        ttk.Button(frm_top, text="Mostrar todas", command=self._actualizar_lista).pack(side='left')

        cols = ("TareaID", "Titulo", "Estado", "Prioridad", "FechaVencimiento")
        self.tree = ttk.Treeview(self.master, columns=cols, show='headings', height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100)
        self.tree.column("TareaID", width=40)
        self.tree.pack(fill='both', expand=True, padx=10)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        frm_acciones_superior = ttk.Frame(self.master)
        frm_acciones_superior.pack(fill='x', padx=10, pady=(5, 0))
        self.btn_añadir_nueva = ttk.Button(frm_acciones_superior, text="Añadir nueva tarea", command=self._limpiar)
        self.btn_añadir_nueva.pack(side='left', padx=5)

        frm_form = ttk.LabelFrame(self.master, text="Tarea")
        frm_form.pack(fill='x', padx=10, pady=5)

        labels = ["Titulo*", "Descripcion", "FechaVencimiento (YYYY‑MM‑DD)", "Prioridad", "Estado", "Recurrente"]
        self.vars = {}
        for i, text in enumerate(labels):
            ttk.Label(frm_form, text=text).grid(row=i, column=0, sticky='e', pady=2)
            if text == "Prioridad":
                cb = ttk.Combobox(frm_form, values=['baja', 'media', 'alta'], state="readonly")
                cb.current(1)
                cb.grid(row=i, column=1, sticky='we', pady=2)
                self.vars[text] = cb
            elif text == "Estado":
                cb2 = ttk.Combobox(frm_form, values=['pendiente', 'completada', 'archivada'], state="readonly")
                cb2.current(0)
                cb2.grid(row=i, column=1, sticky='we', pady=2)
                self.vars[text] = cb2
            elif text == "Recurrente":
                var = tk.IntVar()
                ttk.Checkbutton(frm_form, variable=var).grid(row=i, column=1, sticky='w')
                self.vars[text] = var
            elif text == "FechaVencimiento (YYYY‑MM‑DD)":
                date_entry = DateEntry(frm_form, date_pattern='yyyy-mm-dd')
                date_entry.grid(row=i, column=1, sticky='we', pady=2)
                self.vars[text] = date_entry
            else:
                e = ttk.Entry(frm_form)
                e.grid(row=i, column=1, sticky='we', pady=2)
                self.vars[text] = e

        frm_botones = ttk.Frame(self.master)
        frm_botones.pack(padx=10, pady=5, fill='x')
        btns = [
            ("Agregar", self._agregar, tk.NORMAL),
            ("Actualizar", self._actualizar, tk.DISABLED),
            ("Eliminar", self._eliminar, tk.DISABLED),
            ("Marcar completada", self._marcar_completada, tk.DISABLED),
            ("Limpiar", self._limpiar, tk.NORMAL),
            ("Programar recordatorio", self._abrir_gestor_recordatorios, tk.DISABLED)

        ]
        self.btns = {}
        for text, cmd, st in btns:
            b = ttk.Button(frm_botones, text=text, command=cmd, state=st)
            b.pack(side='left', padx=5)
            self.btns[text] = b

    def _abrir_gestor_recordatorios(self):
        if not self.tarea_seleccionada:
            messagebox.showwarning("Advertencia", "Debes seleccionar una tarea primero.")
            return
        try:
            top = tk.Toplevel(self.master)
            top.title("Gestor de Recordatorios")
            RecordatorioGUI(top, self.session, self.tarea_service, self.usuario_logueado, self.tarea_seleccionada.id)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el gestor de recordatorios:\n{e}")

    def _cargar_id_usuario(self):
        repo = UsuarioRepo(self.session)
        usuario = repo.obtener_por_nombre(self.usuario_logueado)
        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado.")
            self.master.destroy()
        else:
            self.id_usuario = usuario.id
            self.usuario_logueado_obj = usuario

    def _get_tareas(self):
        return self.tarea_service.listar_tareas(self.id_usuario)

    def _llenar_tree(self, tareas):
        self.tree.delete(*self.tree.get_children())
        for t in tareas:
            self.tree.insert('', 'end', values=(
                t.id,
                t.titulo,
                t.estado,
                t.prioridad,
                t.fecha_vencimiento.strftime('%Y-%m-%d') if t.fecha_vencimiento else ''
            ))

    def _actualizar_lista(self):
        self.tareas = self._get_tareas()
        self._llenar_tree(self.tareas)
        self.entry_buscar.delete(0, tk.END)

    def _buscar(self):
        txt = self.entry_buscar.get().strip().lower()
        if not txt:
            self._actualizar_lista()
        else:
            filtradas = [t for t in self.tareas if txt in (t.titulo or '').lower()]
            self._llenar_tree(filtradas)

    def _on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        tid = self.tree.item(sel[0])['values'][0]
        t = next((x for x in self.tareas if x.id == tid), None)
        if not t:
            return
        self.tarea_seleccionada = t
        self.vars["Titulo*"].delete(0, tk.END)
        self.vars["Titulo*"].insert(0, t.titulo)
        self.vars["Descripcion"].delete(0, tk.END)
        self.vars["Descripcion"].insert(0, t.descripcion or "")
        self.vars["FechaVencimiento (YYYY‑MM‑DD)"].delete(0, tk.END)
        self.vars["FechaVencimiento (YYYY‑MM‑DD)"].insert(0, t.fecha_vencimiento.strftime('%Y-%m-%d') if t.fecha_vencimiento else "")
        self.vars["Prioridad"].set(t.prioridad)
        self.vars["Estado"].set(t.estado)
        self.vars["Recurrente"].set(int(t.recurrente))

        for key in ["Actualizar", "Eliminar", "Marcar completada", "Programar recordatorio"]:
            self.btns[key].config(state=tk.NORMAL)
        self.btns["Agregar"].config(state=tk.DISABLED)

    def _validar_form(self):
        try:
            titulo = self.vars["Titulo*"].get().strip()
            if not titulo:
                raise ValueError("El título es obligatorio")
            des = self.vars["Descripcion"].get().strip()
            fec = self.vars["FechaVencimiento (YYYY‑MM‑DD)"].get().strip()
            fecha_obj = None
            if fec:
                try:
                    fecha_obj = datetime.strptime(fec, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD.")
            pri = self.vars["Prioridad"].get()
            est = self.vars["Estado"].get()
            rec = bool(self.vars["Recurrente"].get())
            return {
                "titulo": titulo,
                "descripcion": des,
                "fecha_vencimiento": fecha_obj,
                "prioridad": pri,
                "estado": est,
                "recurrente": int(rec),
                "frecuencia_recurrencia": None,
                "id_usuario_creador": self.id_usuario
            }
        except ValueError as ve:
            messagebox.showwarning("Validación", str(ve))
            return None

    def _obtener_tarea_seleccionada(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona una tarea.")
            return None
        item = self.tree.item(seleccion[0])
        tarea_id = item['values'][0]
        return next((t for t in self.tareas if t.id == tarea_id), None)

    def _agregar(self):
        datos = self._validar_form()
        if not datos:
            return
        try:
            tarea = Tarea(**datos)
            self.tarea_service.agregar_tarea(tarea)
            messagebox.showinfo("Éxito", "Se agregó la tarea.")
            self._actualizar_lista()
            self._limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")

    def _actualizar(self):
        tarea = self._obtener_tarea_seleccionada()
        if not tarea:
            return
        datos = self._validar_form()
        if not datos:
            return
        for k, v in datos.items():
            setattr(tarea, k, v)
        try:
            self.tarea_service.editar_tarea(tarea)
            messagebox.showinfo("Éxito", "Tarea actualizada.")
            self._actualizar_lista()
            self._limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def _eliminar(self):
        tarea = self._obtener_tarea_seleccionada()
        if not tarea:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar tarea?"):
            try:
                self.tarea_service.eliminar_tarea(tarea.id)
                messagebox.showinfo("Éxito", "Tarea eliminada.")
                self._actualizar_lista()
                self._limpiar()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def _marcar_completada(self):
        tarea = self._obtener_tarea_seleccionada()
        if not tarea:
            return
        tarea.estado = 'completada'
        try:
            self.tarea_service.editar_tarea(tarea)
            messagebox.showinfo("Éxito", "Tarea marcada como completada.")
            self._actualizar_lista()
            self._limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo marcar: {e}")

    def _limpiar(self):
        for v in self.vars.values():
            if isinstance(v, (ttk.Entry, tk.Entry)):
                v.delete(0, tk.END)
            elif isinstance(v, ttk.Combobox):
                v.current(0)
            elif isinstance(v, tk.IntVar):
                v.set(0)

        self.tree.selection_remove(self.tree.selection())
        self.tarea_seleccionada = None
        for key in ["Agregar", "Actualizar", "Eliminar", "Marcar completada", "Programar recordatorio"]:
            self.btns[key].config(state=tk.NORMAL if key == "Agregar" else tk.DISABLED)

        self.vars["Titulo*"].focus_set()
