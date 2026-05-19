
import tkinter as tk  # importa tkinter
from tkinter import ttk, messagebox  # importa elementos necesarios desde otro modulo
import sys, os  # importa un modulo requerido por el programa
# Importar clases del sistema
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # inserta datos en el control o coleccion
from clases.cliente import Cliente  # importa elementos necesarios desde otro modulo
from clases.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada  # importa elementos necesarios desde otro modulo
from clases.reserva import Reserva  # importa elementos necesarios desde otro modulo
from clases.excepciones import ClienteInvalidoError, ServicioNoDisponibleError, ReservaInvalidaError  # importa elementos necesarios desde otro modulo
from utils.logger import Logger  # importa elementos necesarios desde otro modulo
# ---- Colores y fuentes ----
BG = "#0f1117"  # asigna o actualiza el valor de BG
PANEL = "#1a1d27"  # asigna o actualiza el valor de PANEL
CARD = "#22263a"  # asigna o actualiza el valor de CARD
ACCENT = "#4f8ef7"  # asigna o actualiza el valor de ACCENT
ACCENT2 = "#7c3aed"  # asigna o actualiza el valor de ACCENT2
SUCCESS = "#22c55e"  # asigna o actualiza el valor de SUCCESS
ERROR = "#ef4444"  # asigna o actualiza el valor de ERROR
WARNING = "#f59e0b"  # asigna o actualiza el valor de WARNING
TEXT = "#e2e8f0"  # asigna o actualiza el valor de TEXT
MUTED = "#64748b"  # asigna o actualiza el valor de MUTED
BORDER = "#2d3352"  # asigna o actualiza el valor de BORDER
FONT_TITLE = ("Consolas", 18, "bold")  # asigna o actualiza el valor de FONT TITLE
FONT_SUB = ("Consolas", 11, "bold")  # asigna o actualiza el valor de FONT SUB
FONT_BODY = ("Consolas", 10)  # asigna o actualiza el valor de FONT BODY
FONT_SMALL = ("Consolas", 9)  # asigna o actualiza el valor de FONT SMALL
FONT_BTN = ("Consolas", 10, "bold")  # asigna o actualiza el valor de FONT BTN
logger = Logger("logs/sistema.log")  # asigna o actualiza el valor de logger
# Listas en memoria
clientes = []  # asigna o actualiza el valor de clientes
servicios_lista = []  # asigna o actualiza el valor de servicios lista
reservas = []  # asigna o actualiza el valor de reservas
# ── Helpers ──────────────────────────────────────────────────
def log_msg(widget, msg, color=TEXT):  # define la funcion o metodo log_msg
	widget.config(state="normal")  # ajusta la configuracion del elemento
	widget.insert("end", msg + "\n", color)  # inserta datos en el control o coleccion
	widget.tag_config(color, foreground=color)  # asigna varios valores en la misma instruccion
	widget.see("end")  # ejecuta esta instruccion del programa
	widget.config(state="disabled")  # ajusta la configuracion del elemento

def entry(parent, placeholder="", **kw):  # define la funcion o metodo entry
	var = tk.StringVar()  # asigna o actualiza el valor de var
	e = tk.Entry(parent, textvariable=var, bg=CARD, fg=TEXT,  # asigna o actualiza el valor de e
		insertbackground=TEXT, relief="flat",  # asigna o actualiza el valor de insertbackground
		font=FONT_BODY, bd=0, highlightthickness=1,  # asigna o actualiza el valor de font
		highlightbackground=BORDER, highlightcolor=ACCENT, **kw)  # asigna o actualiza el valor de highlightbackground
	if placeholder:  # evalua una condicion para decidir el flujo
		e.insert(0, placeholder)  # inserta datos en el control o coleccion
		e.config(fg=MUTED)  # ajusta la configuracion del elemento
	def on_focus_in(ev):  # define la funcion o metodo on_focus_in
		if e.get() == placeholder:  # evalua una condicion para decidir el flujo
			e.delete(0, "end")  # elimina contenido del control
			e.config(fg=TEXT)  # ajusta la configuracion del elemento
	def on_focus_out(ev):  # define la funcion o metodo on_focus_out
		if not e.get():  # evalua una condicion para decidir el flujo
			e.insert(0, placeholder)  # inserta datos en el control o coleccion
			e.config(fg=MUTED)  # ajusta la configuracion del elemento
	e.bind("<FocusIn>", on_focus_in)  # conecta un evento de la interfaz con una accion
	e.bind("<FocusOut>", on_focus_out)  # conecta un evento de la interfaz con una accion
	return e, var  # devuelve un valor al llamador

def btn(parent, text, cmd, color=ACCENT, fg=BG, width=22):  # define la funcion o metodo btn
	b = tk.Button(parent, text=text, command=cmd,  # asigna o actualiza el valor de b
		bg=color, fg=fg, font=FONT_BTN,  # asigna o actualiza el valor de bg
		relief="flat", cursor="hand2",  # asigna o actualiza el valor de relief
		padx=10, pady=6, width=width,  # asigna o actualiza el valor de padx
		activebackground=ACCENT2, activeforeground=TEXT)  # asigna o actualiza el valor de activebackground
	b.bind("<Enter>", lambda e: b.config(bg=ACCENT2, fg=TEXT))  # ajusta la configuracion del elemento
	b.bind("<Leave>", lambda e: b.config(bg=color, fg=fg))  # ajusta la configuracion del elemento
	return b  # devuelve un valor al llamador

def label(parent, text, font=FONT_BODY, fg=TEXT, **kw):  # define la funcion o metodo label
	return tk.Label(parent, text=text, font=font, fg=fg, bg=parent["bg"], **kw)  # devuelve un valor al llamador

def section_title(parent, text):  # define la funcion o metodo section_title
	f = tk.Frame(parent, bg=PANEL)  # asigna o actualiza el valor de f
	tk.Label(f, text=text, font=FONT_SUB, fg=ACCENT,  # asigna varios valores en la misma instruccion
		bg=PANEL, anchor="w").pack(side="left")  # ubica el widget dentro de la ventana
	tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=(8,0), pady=10)  # ubica el widget dentro de la ventana
	f.pack(fill="x", pady=(12, 4))  # ubica el widget dentro de la ventana
	return f  # devuelve un valor al llamador

def log_box(parent, height=8):  # define la funcion o metodo log_box
	frm = tk.Frame(parent, bg=CARD, bd=0, highlightthickness=1,  # asigna o actualiza el valor de frm
		highlightbackground=BORDER)  # asigna o actualiza el valor de highlightbackground
	sb = tk.Scrollbar(frm, bg=PANEL, troughcolor=CARD, relief="flat")  # asigna o actualiza el valor de sb
	txt = tk.Text(frm, height=height, bg=CARD, fg=TEXT,  # asigna o actualiza el valor de txt
		font=FONT_SMALL, state="disabled",  # asigna o actualiza el valor de font
		relief="flat", bd=0, padx=8, pady=6,  # asigna o actualiza el valor de relief
		yscrollcommand=sb.set, wrap="word")  # asigna o actualiza el valor de yscrollcommand
	sb.config(command=txt.yview)  # ajusta la configuracion del elemento
	sb.pack(side="right", fill="y")  # ubica el widget dentro de la ventana
	txt.pack(fill="both", expand=True)  # ubica el widget dentro de la ventana
	frm.pack(fill="both", expand=True, pady=4)  # ubica el widget dentro de la ventana
	return txt  # devuelve un valor al llamador

# ── Ventana principal ─────────────────────────────────────────
class App(tk.Tk):  # define la clase App
	def __init__(self):  # define la funcion o metodo __init__
		super().__init__()  # inicializa la clase padre
		self.title(" Software FJ")  # ejecuta esta instruccion del programa
		self.geometry("980x680")  # ejecuta esta instruccion del programa
		self.minsize(900, 600)  # ejecuta esta instruccion del programa
		self.config(bg=BG)  # ajusta la configuracion del elemento
		self._build_header()  # ejecuta esta instruccion del programa
		self._build_notebook()  # ejecuta esta instruccion del programa

	def _build_header(self):  # define la funcion o metodo _build_header
		hdr = tk.Frame(self, bg=PANEL, height=56)  # asigna o actualiza el valor de hdr
		hdr.pack(fill="x")  # ubica el widget dentro de la ventana
		hdr.pack_propagate(False)  # ejecuta esta instruccion del programa
		tk.Label(hdr, text="⬡ SOFTWARE FJ", font=("Consolas", 15, "bold"),  # asigna varios valores en la misma instruccion
			fg=ACCENT, bg=PANEL).pack(side="left", padx=20)  # ubica el widget dentro de la ventana
		tk.Label(hdr, text="Sistema Integral de Gestión · UNAD 213023",  # asigna varios valores en la misma instruccion
			font=FONT_SMALL, fg=MUTED, bg=PANEL).pack(side="left", padx=4)  # ubica el widget dentro de la ventana

	def _build_notebook(self):  # define la funcion o metodo _build_notebook
		style = ttk.Style(self)  # asigna o actualiza el valor de style
		style.theme_use("clam")  # ejecuta esta instruccion del programa
		style.configure("TNotebook", background=BG, borderwidth=0)  # ajusta la configuracion del elemento
		style.configure("TNotebook.Tab", background=PANEL, foreground=MUTED,  # ajusta la configuracion del elemento
			font=FONT_BTN, padding=[16,8], borderwidth=0)  # asigna o actualiza el valor de font
		style.map("TNotebook.Tab",  # continua una llamada o estructura de datos
			background=[("selected", CARD)],  # asigna o actualiza el valor de background
			foreground=[("selected", ACCENT)])  # asigna o actualiza el valor de foreground
		nb = ttk.Notebook(self)  # asigna o actualiza el valor de nb
		nb.pack(fill="both", expand=True, padx=0, pady=0)  # ubica el widget dentro de la ventana
		tabs = [  # asigna o actualiza el valor de tabs
			("👤 Clientes", TabClientes),  # continua una llamada o estructura de datos
			("🛠 Servicios", TabServicios),  # continua una llamada o estructura de datos
			("📋 Reservas", TabReservas),  # continua una llamada o estructura de datos
			("📊 Resumen", TabResumen),  # continua una llamada o estructura de datos
		]  # cierra la llamada o estructura anterior
		for name, cls in tabs:  # recorre una coleccion elemento por elemento
			frame = cls(nb)  # asigna o actualiza el valor de frame
			nb.add(frame, text=name)  # asigna varios valores en la misma instruccion

# ── Tab Clientes ──────────────────────────────────────────────
class TabClientes(tk.Frame):  # define la clase TabClientes
	def __init__(self, master):  # define la funcion o metodo __init__
		super().__init__(master, bg=PANEL)  # inicializa la clase padre
		self._build()  # ejecuta esta instruccion del programa

	def _build(self):  # define la funcion o metodo _build
		# Formulario
		form = tk.Frame(self, bg=PANEL, padx=24, pady=16)  # asigna o actualiza el valor de form
		form.pack(fill="x")  # ubica el widget dentro de la ventana
		section_title(form, "Registrar nuevo cliente")  # ejecuta esta instruccion del programa
		grid = tk.Frame(form, bg=PANEL)  # asigna o actualiza el valor de grid
		grid.pack(fill="x")  # ubica el widget dentro de la ventana
		fields = [("ID", "Ej: 001"), ("Nombre", "Ej: Ana Torres"),  # asigna o actualiza el valor de fields
			("Correo", "Ej: ana@email.com"), ("Teléfono", "Ej: 3001234567")]  # ejecuta esta instruccion del programa
		self.entries = {}  # asigna o actualiza el valor de entries
		for i, (lbl, ph) in enumerate(fields):  # recorre una coleccion elemento por elemento
			r, c = divmod(i, 2)  # asigna varios valores en la misma instruccion
			tk.Label(grid, text=lbl, font=FONT_SMALL, fg=MUTED,  # asigna varios valores en la misma instruccion
				bg=PANEL, anchor="w").grid(row=r*2, column=c, sticky="w", padx=(0,20), pady=(6,2))  # ubica el widget dentro de la ventana
			e, v = entry(grid, ph, width=32)  # asigna varios valores en la misma instruccion
			e.grid(row=r*2+1, column=c, sticky="ew", padx=(0,20), ipady=6)  # ubica el widget dentro de la ventana
			self.entries[lbl] = (e, v)  # asigna o actualiza el valor de entries lbl
		grid.columnconfigure(0, weight=1)  # asigna varios valores en la misma instruccion
		grid.columnconfigure(1, weight=1)  # asigna varios valores en la misma instruccion
		bf = tk.Frame(form, bg=PANEL)  # asigna o actualiza el valor de bf
		bf.pack(fill="x", pady=(14,0))  # ubica el widget dentro de la ventana
		btn(bf, "✚ Registrar cliente", self._registrar, SUCCESS).pack(side="left")  # ubica el widget dentro de la ventana
		btn(bf, "✖ Limpiar", self._limpiar, MUTED, TEXT, 14).pack(side="left", padx=8)  # ubica el widget dentro de la ventana
		# Log
		section_title(form, "Resultado")  # ejecuta esta instruccion del programa
		self.log = log_box(form, 5)  # asigna o actualiza el valor de log
		# Tabla
		section_title(form, "Clientes registrados")  # ejecuta esta instruccion del programa
		self._tabla(form)  # ejecuta esta instruccion del programa

	def _tabla(self, parent):  # define la funcion o metodo _tabla
		cols = ("ID", "Nombre", "Correo", "Teléfono")  # asigna o actualiza el valor de cols
		style = ttk.Style()  # asigna o actualiza el valor de style
		style.configure("Dark.Treeview",  # ajusta la configuracion del elemento
			background=CARD, foreground=TEXT,  # asigna o actualiza el valor de background
			fieldbackground=CARD, rowheight=26,  # asigna o actualiza el valor de fieldbackground
			font=FONT_SMALL, borderwidth=0)  # asigna o actualiza el valor de font
		style.configure("Dark.Treeview.Heading",  # ajusta la configuracion del elemento
			background=PANEL, foreground=ACCENT,  # asigna o actualiza el valor de background
			font=FONT_BTN, borderwidth=0, relief="flat")  # asigna o actualiza el valor de font
		style.map("Dark.Treeview", background=[("selected", ACCENT2)])  # asigna varios valores en la misma instruccion
		self.tree = ttk.Treeview(parent, columns=cols, show="headings",  # asigna o actualiza el valor de tree
			height=5, style="Dark.Treeview")  # asigna o actualiza el valor de height
		widths = [60, 180, 200, 120]  # asigna o actualiza el valor de widths
		for col, w in zip(cols, widths):  # recorre una coleccion elemento por elemento
			self.tree.heading(col, text=col)  # asigna varios valores en la misma instruccion
			self.tree.column(col, width=w, anchor="w")  # asigna varios valores en la misma instruccion
		self.tree.pack(fill="x", pady=4)  # ubica el widget dentro de la ventana

	def _registrar(self):  # define la funcion o metodo _registrar
		vals = {}  # asigna o actualiza el valor de vals
		fields = ["ID", "Nombre", "Correo", "Teléfono"]  # asigna o actualiza el valor de fields
		placeholders = {"ID":"Ej: 001","Nombre":"Ej: Ana Torres",  # asigna o actualiza el valor de placeholders
			"Correo":"Ej: ana@email.com","Teléfono":"Ej: 3001234567"}  # ejecuta esta instruccion del programa
		for f in fields:  # recorre una coleccion elemento por elemento
			v = self.entries[f][1].get().strip()  # asigna o actualiza el valor de v
			if v == placeholders[f]: v = ""  # evalua una condicion para decidir el flujo
			vals[f] = v  # asigna o actualiza el valor de vals f
		try:  # inicia un bloque que puede generar excepciones
			c = Cliente(vals["ID"], vals["Nombre"], vals["Correo"], vals["Teléfono"])  # asigna o actualiza el valor de c
			clientes.append(c)  # agrega un objeto a la lista
			self.tree.insert("", "end", values=(c.get_id(), c.get_nombre(),  # inserta datos en el control o coleccion
				c.get_correo(), c.get_telefono()))  # ejecuta esta instruccion del programa
			log_msg(self.log, f"✅ Cliente registrado: {c.get_nombre()}", SUCCESS)  # ejecuta esta instruccion del programa
			logger.registrar_evento(f"Cliente registrado: {c.get_nombre()}")  # ejecuta esta instruccion del programa
			self._limpiar()  # ejecuta esta instruccion del programa
		except ClienteInvalidoError as e:  # captura y maneja una excepcion
			log_msg(self.log, f"❌ {e}", ERROR)  # ejecuta esta instruccion del programa
			logger.registrar_error(str(e))  # ejecuta esta instruccion del programa

	def _limpiar(self):  # define la funcion o metodo _limpiar
		placeholders = {"ID":"Ej: 001","Nombre":"Ej: Ana Torres",  # asigna o actualiza el valor de placeholders
			"Correo":"Ej: ana@email.com","Teléfono":"Ej: 3001234567"}  # ejecuta esta instruccion del programa
		for f, (e, v) in self.entries.items():  # recorre una coleccion elemento por elemento
			e.delete(0, "end")  # elimina contenido del control
			e.insert(0, placeholders[f])  # inserta datos en el control o coleccion
			e.config(fg=MUTED)  # ajusta la configuracion del elemento

# ── Tab Servicios ─────────────────────────────────────────────
class TabServicios(tk.Frame):  # define la clase TabServicios
	def __init__(self, master):  # define la funcion o metodo __init__
		super().__init__(master, bg=PANEL)  # inicializa la clase padre
		self._build()  # ejecuta esta instruccion del programa

	def _build(self):  # define la funcion o metodo _build
		form = tk.Frame(self, bg=PANEL, padx=24, pady=16)  # asigna o actualiza el valor de form
		form.pack(fill="x")  # ubica el widget dentro de la ventana
		section_title(form, "Crear nuevo servicio")  # ejecuta esta instruccion del programa
		# Tipo de servicio
		tf = tk.Frame(form, bg=PANEL)  # asigna o actualiza el valor de tf
		tf.pack(fill="x", pady=(0,10))  # ubica el widget dentro de la ventana
		tk.Label(tf, text="Tipo de servicio", font=FONT_SMALL, fg=MUTED,  # asigna varios valores en la misma instruccion
			bg=PANEL).pack(anchor="w")  # ubica el widget dentro de la ventana
		self.tipo_var = tk.StringVar(value="ReservaSala")  # asigna o actualiza el valor de tipo var
		for t in ["ReservaSala", "AlquilerEquipo", "AsesoriaEspecializada"]:  # recorre una coleccion elemento por elemento
			rb = tk.Radiobutton(tf, text=t, variable=self.tipo_var, value=t,  # asigna o actualiza el valor de rb
				bg=PANEL, fg=TEXT, selectcolor=CARD,  # asigna o actualiza el valor de bg
				activebackground=PANEL, activeforeground=ACCENT,  # asigna o actualiza el valor de activebackground
				font=FONT_BODY, command=self._actualizar_campos)  # asigna o actualiza el valor de font
			rb.pack(side="left", padx=(0,20))  # ubica el widget dentro de la ventana
		# Campos comunes
		grid = tk.Frame(form, bg=PANEL)  # asigna o actualiza el valor de grid
		grid.pack(fill="x")  # ubica el widget dentro de la ventana
		tk.Label(grid, text="ID", font=FONT_SMALL, fg=MUTED, bg=PANEL, anchor="w").grid(row=0, column=0, sticky="w", pady=(4,2))  # ubica el widget dentro de la ventana
		self.e_id, self.v_id = entry(grid, "Ej: S01", width=20)  # asigna varios valores en la misma instruccion
		self.e_id.grid(row=1, column=0, sticky="ew", padx=(0,20), ipady=6)  # ubica el widget dentro de la ventana
		tk.Label(grid, text="Nombre", font=FONT_SMALL, fg=MUTED, bg=PANEL,  # asigna varios valores en la misma instruccion
			anchor="w").grid(row=0, column=1, sticky="w", pady=(4,2))  # ubica el widget dentro de la ventana
		self.e_nom, self.v_nom = entry(grid, "Ej: Sala Piso 3", width=30)  # asigna varios valores en la misma instruccion
		self.e_nom.grid(row=1, column=1, sticky="ew", padx=(0,20), ipady=6)  # ubica el widget dentro de la ventana
		# Campo extra (capacidad / tipo_equipo / especialidad)
		self.lbl_extra = tk.Label(grid, text="Capacidad", font=FONT_SMALL, fg=MUTED, bg=PANEL,  # asigna o actualiza el valor de lbl extra
			anchor="w")  # asigna o actualiza el valor de anchor
		self.lbl_extra.grid(row=0, column=2, sticky="w", pady=(4,2))  # ubica el widget dentro de la ventana
		self.e_extra, self.v_extra = entry(grid, "Ej: 20", width=20)  # asigna varios valores en la misma instruccion
		self.e_extra.grid(row=1, column=2, sticky="ew", ipady=6)  # ubica el widget dentro de la ventana
		for c in range(3): grid.columnconfigure(c, weight=1)  # recorre una coleccion elemento por elemento
		bf = tk.Frame(form, bg=PANEL)  # asigna o actualiza el valor de bf
		bf.pack(fill="x", pady=(14,0))  # ubica el widget dentro de la ventana
		btn(bf, "✚ Crear servicio", self._crear, SUCCESS).pack(side="left")  # ubica el widget dentro de la ventana
		section_title(form, "Resultado")  # ejecuta esta instruccion del programa
		self.log = log_box(form, 4)  # asigna o actualiza el valor de log
		section_title(form, "Servicios disponibles")  # ejecuta esta instruccion del programa
		cols = ("ID", "Tipo", "Nombre", "Detalle", "Precio/hora")  # asigna o actualiza el valor de cols
		style = ttk.Style()  # asigna o actualiza el valor de style
		style.configure("Dark.Treeview", background=CARD, foreground=TEXT,  # ajusta la configuracion del elemento
			fieldbackground=CARD, rowheight=26, font=FONT_SMALL)  # asigna o actualiza el valor de fieldbackground
		style.configure("Dark.Treeview.Heading", background=PANEL,  # ajusta la configuracion del elemento
			foreground=ACCENT, font=FONT_BTN, relief="flat")  # asigna o actualiza el valor de foreground
		style.map("Dark.Treeview", background=[("selected", ACCENT2)])  # asigna varios valores en la misma instruccion
		self.tree = ttk.Treeview(form, columns=cols, show="headings",  # asigna o actualiza el valor de tree
			height=5, style="Dark.Treeview")  # asigna o actualiza el valor de height
		ws = [60, 150, 200, 160, 110]  # asigna o actualiza el valor de ws
		for col, w in zip(cols, ws):  # recorre una coleccion elemento por elemento
			self.tree.heading(col, text=col)  # asigna varios valores en la misma instruccion
			self.tree.column(col, width=w, anchor="w")  # asigna varios valores en la misma instruccion
		self.tree.pack(fill="x", pady=4)  # ubica el widget dentro de la ventana

	def _actualizar_campos(self):  # define la funcion o metodo _actualizar_campos
		t = self.tipo_var.get()  # asigna o actualiza el valor de t
		hints = {"ReservaSala": ("Capacidad", "Ej: 20 personas"),  # asigna o actualiza el valor de hints
			"AlquilerEquipo": ("Tipo equipo", "laptop/proyector/impresora/otro"),  # continua una llamada o estructura de datos
			"AsesoriaEspecializada": ("Especialidad", "Asesoria de equipos")}  # ejecuta esta instruccion del programa
		lbl, ph = hints[t]  # asigna varios valores en la misma instruccion
		self.lbl_extra.config(text=lbl)  # ajusta la configuracion del elemento
		self.e_extra.delete(0, "end")  # elimina contenido del control
		self.e_extra.insert(0, ph)  # inserta datos en el control o coleccion
		self.e_extra.config(fg=MUTED)  # ajusta la configuracion del elemento

	def _crear(self):  # define la funcion o metodo _crear
		tipo = self.tipo_var.get()  # asigna o actualiza el valor de tipo
		sid = self.v_id.get().strip()  # asigna o actualiza el valor de sid
		nom = self.v_nom.get().strip()  # asigna o actualiza el valor de nom
		ext = self.v_extra.get().strip()  # asigna o actualiza el valor de ext
		# Limpiar placeholders
		for v, ph in [(sid,"Ej: S01"),(nom,"Ej: Sala Piso 3")]:  # recorre una coleccion elemento por elemento
			pass  # mantiene el bloque sin instrucciones adicionales
		if sid in ("Ej: S01","Ej: E01","Ej: A01"): sid=""  # evalua una condicion para decidir el flujo
		if nom in ("Ej: Sala Piso 3","Ej: Laptop HP","Ej: Asesoría Python"): nom=""  # evalua una condicion para decidir el flujo
		try:  # inicia un bloque que puede generar excepciones
			if tipo == "ReservaSala":  # evalua una condicion para decidir el flujo
				cap = int(ext) if ext.isdigit() else -1  # asigna o actualiza el valor de cap
				s = ReservaSala(sid, nom, capacidad=cap)  # asigna o actualiza el valor de s
				detalle = f"Cap: {cap}"  # asigna o actualiza el valor de detalle
			elif tipo == "AlquilerEquipo":  # evalua una condicion alternativa
				s = AlquilerEquipo(sid, nom, tipo_equipo=ext)  # asigna o actualiza el valor de s
				detalle = f"Tipo: {ext}"  # asigna o actualiza el valor de detalle
			else:  # ejecuta el bloque cuando no se cumple la condicion anterior
				s = AsesoriaEspecializada(sid, nom, especialidad=ext)  # asigna o actualiza el valor de s
				detalle = f"Esp: {ext}"  # asigna o actualiza el valor de detalle
			servicios_lista.append(s)  # agrega un objeto a la lista
			self.tree.insert("", "end", values=(  # inserta datos en el control o coleccion
				s.get_id(), tipo, s.get_nombre(),  # continua una llamada o estructura de datos
				detalle, f"${s.get_precio_hora():,.0f}"))  # ejecuta esta instruccion del programa
			log_msg(self.log, f"✅ Servicio creado: {s.get_nombre()}", SUCCESS)  # ejecuta esta instruccion del programa
			logger.registrar_evento(f"Servicio creado: {s.get_nombre()}")  # ejecuta esta instruccion del programa
		except (ServicioNoDisponibleError, ValueError) as e:  # captura y maneja una excepcion
			log_msg(self.log, f"❌ {e}", ERROR)  # ejecuta esta instruccion del programa
			logger.registrar_error(str(e))  # ejecuta esta instruccion del programa

# ── Tab Reservas ──────────────────────────────────────────────
class TabReservas(tk.Frame):  # define la clase TabReservas
	def __init__(self, master):  # define la funcion o metodo __init__
		super().__init__(master, bg=PANEL)  # inicializa la clase padre
		self._build()  # ejecuta esta instruccion del programa

	def _build(self):  # define la funcion o metodo _build
		form = tk.Frame(self, bg=PANEL, padx=24, pady=16)  # asigna o actualiza el valor de form
		form.pack(fill="x")  # ubica el widget dentro de la ventana
		section_title(form, "Nueva reserva")  # ejecuta esta instruccion del programa
		grid = tk.Frame(form, bg=PANEL)  # asigna o actualiza el valor de grid
		grid.pack(fill="x")  # ubica el widget dentro de la ventana
		# ID Reserva
		tk.Label(grid, text="ID Reserva", font=FONT_SMALL, fg=MUTED, bg=PANEL,  # asigna varios valores en la misma instruccion
			anchor="w").grid(row=0, column=0, sticky="w", pady=(4,2))  # ubica el widget dentro de la ventana
		self.e_rid, self.v_rid = entry(grid, "Ej: R001", width=18)  # asigna varios valores en la misma instruccion
		self.e_rid.grid(row=1, column=0, sticky="ew", padx=(0,16), ipady=6)  # ubica el widget dentro de la ventana
		# Duración
		tk.Label(grid, text="Duración (horas)", font=FONT_SMALL, fg=MUTED, bg=PANEL,  # asigna varios valores en la misma instruccion
			anchor="w").grid(row=0, column=1, sticky="w", pady=(4,2))  # ubica el widget dentro de la ventana
		self.e_dur, self.v_dur = entry(grid, "Ej: 3", width=12)  # asigna varios valores en la misma instruccion
		self.e_dur.grid(row=1, column=1, sticky="ew", padx=(0,16), ipady=6)  # ubica el widget dentro de la ventana
		grid.columnconfigure(0, weight=1)  # asigna varios valores en la misma instruccion
		grid.columnconfigure(1, weight=1)  # asigna varios valores en la misma instruccion
		# Selectores
		sf = tk.Frame(form, bg=PANEL)  # asigna o actualiza el valor de sf
		sf.pack(fill="x", pady=(10,0))  # ubica el widget dentro de la ventana
		tk.Label(sf, text="Cliente", font=FONT_SMALL, fg=MUTED, bg=PANEL).grid(row=0, column=0, sticky="w", pady=(4,2))  # ubica el widget dentro de la ventana
		self.cb_cliente = ttk.Combobox(sf, font=FONT_BODY, width=28, state="readonly")  # asigna o actualiza el valor de cb cliente
		self.cb_cliente.grid(row=1, column=0, sticky="ew", padx=(0,16), ipady=4)  # ubica el widget dentro de la ventana
		tk.Label(sf, text="Servicio", font=FONT_SMALL, fg=MUTED, bg=PANEL).grid(row=0, column=1, sticky="w", pady=(4,2))  # ubica el widget dentro de la ventana
		self.cb_servicio = ttk.Combobox(sf, font=FONT_BODY, width=28, state="readonly")  # asigna o actualiza el valor de cb servicio
		self.cb_servicio.grid(row=1, column=1, sticky="ew", ipady=4)  # ubica el widget dentro de la ventana
		sf.columnconfigure(0, weight=1)  # asigna varios valores en la misma instruccion
		sf.columnconfigure(1, weight=1)  # asigna varios valores en la misma instruccion
		# Estilo combobox
		style = ttk.Style()  # asigna o actualiza el valor de style
		style.configure("TCombobox", fieldbackground=CARD, background=CARD,  # ajusta la configuracion del elemento
			foreground=TEXT, arrowcolor=ACCENT)  # asigna o actualiza el valor de foreground
		bf = tk.Frame(form, bg=PANEL)  # asigna o actualiza el valor de bf
		bf.pack(fill="x", pady=(14,0))  # ubica el widget dentro de la ventana
		btn(bf, "🔄 Actualizar listas", self._actualizar, MUTED, TEXT, 20).pack(side="left", padx=(0,8))  # ubica el widget dentro de la ventana
		btn(bf, "✚ Crear reserva", self._crear, SUCCESS).pack(side="left", padx=(0,8))  # ubica el widget dentro de la ventana
		btn(bf, "✖ Cancelar reserva", self._cancelar, ERROR, TEXT).pack(side="left")  # ubica el widget dentro de la ventana
		section_title(form, "Resultado")  # ejecuta esta instruccion del programa
		self.log = log_box(form, 4)  # asigna o actualiza el valor de log
		section_title(form, "Reservas")  # ejecuta esta instruccion del programa
		cols = ("ID", "Cliente", "Servicio", "Horas", "Estado", "Costo")  # asigna o actualiza el valor de cols
		style.configure("Dark.Treeview", background=CARD, foreground=TEXT,  # ajusta la configuracion del elemento
			fieldbackground=CARD, rowheight=26, font=FONT_SMALL)  # asigna o actualiza el valor de fieldbackground
		style.configure("Dark.Treeview.Heading", background=PANEL,  # ajusta la configuracion del elemento
			foreground=ACCENT, font=FONT_BTN, relief="flat")  # asigna o actualiza el valor de foreground
		style.map("Dark.Treeview", background=[("selected", ACCENT2)])  # asigna varios valores en la misma instruccion
		self.tree = ttk.Treeview(form, columns=cols, show="headings",  # asigna o actualiza el valor de tree
			height=5, style="Dark.Treeview")  # asigna o actualiza el valor de height
		ws = [70, 160, 180, 60, 110, 120]  # asigna o actualiza el valor de ws
		for col, w in zip(cols, ws):  # recorre una coleccion elemento por elemento
			self.tree.heading(col, text=col)  # asigna varios valores en la misma instruccion
			self.tree.column(col, width=w, anchor="w")  # asigna varios valores en la misma instruccion
		self.tree.pack(fill="x", pady=4)  # ubica el widget dentro de la ventana

	def _actualizar(self):  # define la funcion o metodo _actualizar
		self.cb_cliente["values"] = [f"{c.get_id()} - {c.get_nombre()}" for c in clientes]  # asigna o actualiza el valor de cb cliente values
		self.cb_servicio["values"] = [f"{s.get_id()} - {s.get_nombre()}" for s in servicios_lista]  # asigna o actualiza el valor de cb servicio values
		log_msg(self.log, f"🔄 Listas actualizadas: {len(clientes)} clientes, {len(servicios_lista)} servicios.", MUTED)  # ejecuta esta instruccion del programa

	def _crear(self):  # define la funcion o metodo _crear
		rid = self.v_rid.get().strip()  # asigna o actualiza el valor de rid
		dur = self.v_dur.get().strip()  # asigna o actualiza el valor de dur
		ci = self.cb_cliente.current()  # asigna o actualiza el valor de ci
		si = self.cb_servicio.current()  # asigna o actualiza el valor de si
		if ci < 0 or si < 0:  # evalua una condicion para decidir el flujo
			log_msg(self.log, "❌ Selecciona un cliente y un servicio.", ERROR)  # ejecuta esta instruccion del programa
			return  # termina la funcion actual
		try:  # inicia un bloque que puede generar excepciones
			horas = int(dur)  # asigna o actualiza el valor de horas
			r = Reserva(rid, clientes[ci], servicios_lista[si], horas)  # asigna o actualiza el valor de r
			r.confirmar()  # ejecuta esta instruccion del programa
			reservas.append(r)  # agrega un objeto a la lista
			self.tree.insert("", "end", values=(  # inserta datos en el control o coleccion
				r.get_id(),  # continua una llamada o estructura de datos
				clientes[ci].get_nombre(),  # continua una llamada o estructura de datos
				servicios_lista[si].get_nombre(),  # continua una llamada o estructura de datos
				horas, r.get_estado(),  # continua una llamada o estructura de datos
				f"${r.get_costo_total():,.0f}"))  # ejecuta esta instruccion del programa
			log_msg(self.log, f"✅ Reserva {rid} confirmada. Costo: ${r.get_costo_total():,.0f} COP", SUCCESS)  # ejecuta esta instruccion del programa
			logger.registrar_evento(f"Reserva {rid} confirmada.")  # ejecuta esta instruccion del programa
		except (ReservaInvalidaError, ValueError) as e:  # captura y maneja una excepcion
			log_msg(self.log, f"❌ {e}", ERROR)  # ejecuta esta instruccion del programa
			logger.registrar_error(str(e))  # ejecuta esta instruccion del programa

	def _cancelar(self):  # define la funcion o metodo _cancelar
		sel = self.tree.selection()  # asigna o actualiza el valor de sel
		if not sel:  # evalua una condicion para decidir el flujo
			log_msg(self.log, "⚠ Selecciona una reserva de la tabla.", WARNING)  # ejecuta esta instruccion del programa
			return  # termina la funcion actual
		idx = self.tree.index(sel[0])  # asigna o actualiza el valor de idx
		try:  # inicia un bloque que puede generar excepciones
			reservas[idx].cancelar()  # ejecuta esta instruccion del programa
			self.tree.set(sel[0], "Estado", "CANCELADA")  # ejecuta esta instruccion del programa
			self.tree.set(sel[0], "Costo", "$0")  # ejecuta esta instruccion del programa
			log_msg(self.log, f"✖ Reserva {reservas[idx].get_id()} cancelada.", WARNING)  # ejecuta esta instruccion del programa
			logger.registrar_evento(f"Reserva {reservas[idx].get_id()} cancelada.")  # ejecuta esta instruccion del programa
		except ReservaInvalidaError as e:  # captura y maneja una excepcion
			log_msg(self.log, f"❌ {e}", ERROR)  # ejecuta esta instruccion del programa

# ── Tab Resumen ───────────────────────────────────────────────
class TabResumen(tk.Frame):  # define la clase TabResumen
	def __init__(self, master):  # define la funcion o metodo __init__
		super().__init__(master, bg=PANEL)  # inicializa la clase padre
		self._build()  # ejecuta esta instruccion del programa

	def _build(self):  # define la funcion o metodo _build
		form = tk.Frame(self, bg=PANEL, padx=24, pady=16)  # asigna o actualiza el valor de form
		form.pack(fill="both", expand=True)  # ubica el widget dentro de la ventana
		section_title(form, "Resumen del sistema")  # ejecuta esta instruccion del programa
		btn(form, "🔄 Actualizar resumen", self._actualizar, ACCENT).pack(anchor="w", pady=(0,12))  # ubica el widget dentro de la ventana
		# Tarjetas de estadísticas
		cf = tk.Frame(form, bg=PANEL)  # asigna o actualiza el valor de cf
		cf.pack(fill="x", pady=(0,16))  # ubica el widget dentro de la ventana
		self.cards = {}  # asigna o actualiza el valor de cards
		stats = [("👤 Clientes", "0", ACCENT),  # asigna o actualiza el valor de stats
			("🛠 Servicios", "0", ACCENT2),  # continua una llamada o estructura de datos
			("📋 Reservas", "0", SUCCESS),  # continua una llamada o estructura de datos
			("✖ Canceladas", "0", ERROR)]  # ejecuta esta instruccion del programa
		for i, (lbl, val, color) in enumerate(stats):  # recorre una coleccion elemento por elemento
			c = tk.Frame(cf, bg=CARD, padx=20, pady=14,  # asigna o actualiza el valor de c
				highlightthickness=1, highlightbackground=color)  # asigna o actualiza el valor de highlightthickness
			c.grid(row=0, column=i, padx=8, sticky="ew")  # ubica el widget dentro de la ventana
			tk.Label(c, text=lbl, font=FONT_SMALL, fg=MUTED, bg=CARD).pack(anchor="w")  # ubica el widget dentro de la ventana
			num = tk.Label(c, text=val, font=("Consolas",26,"bold"), fg=color, bg=CARD)  # asigna o actualiza el valor de num
			num.pack(anchor="w")  # ubica el widget dentro de la ventana
			self.cards[lbl] = num  # asigna o actualiza el valor de cards lbl
		cf.columnconfigure(i, weight=1)  # asigna varios valores en la misma instruccion
		section_title(form, "Log de eventos")  # ejecuta esta instruccion del programa
		self.log = log_box(form, 12)  # asigna o actualiza el valor de log
		self._cargar_log()  # ejecuta esta instruccion del programa

	def _actualizar(self):  # define la funcion o metodo _actualizar
		confirmadas = sum(1 for r in reservas if r.get_estado() == "CONFIRMADA")  # ejecuta esta instruccion del programa
		canceladas = sum(1 for r in reservas if r.get_estado() == "CANCELADA")  # ejecuta esta instruccion del programa
		self.cards["👤 Clientes"].config(text=str(len(clientes)))  # ajusta la configuracion del elemento
		self.cards["🛠 Servicios"].config(text=str(len(servicios_lista)))  # ajusta la configuracion del elemento
		self.cards["📋 Reservas"].config(text=str(confirmadas))  # ajusta la configuracion del elemento
		self.cards["✖ Canceladas"].config(text=str(canceladas))  # ajusta la configuracion del elemento
		self._cargar_log()  # ejecuta esta instruccion del programa

	def _cargar_log(self):  # define la funcion o metodo _cargar_log
		self.log.config(state="normal")  # ajusta la configuracion del elemento
		self.log.delete("1.0", "end")  # elimina contenido del control
		try:  # inicia un bloque que puede generar excepciones
			with open("logs/sistema.log", "r", encoding="utf-8") as f:  # abre y administra un recurso temporal
				contenido = f.read()  # asigna o actualiza el valor de contenido
			self.log.insert("end", contenido)  # inserta datos en el control o coleccion
		except FileNotFoundError:  # captura y maneja una excepcion
			self.log.insert("end", "El archivo de log aún no existe.\n", MUTED)  # inserta datos en el control o coleccion
		self.log.config(state="disabled")  # ajusta la configuracion del elemento
		self.log.see("end")  # ejecuta esta instruccion del programa

# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":  # evalua una condicion para decidir el flujo
	app = App()  # asigna o actualiza el valor de app
	app.mainloop()  # ejecuta esta instruccion del programa
