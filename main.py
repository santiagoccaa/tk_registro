import tkinter as tk
from tkinter import ttk
import tkinter.constants as tk_constants
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

from Styles import styles
from conexion import conexion
from filtro import *

class Person():
	def __init__(self, nombre, apellidos, correo, telefono, profesion, edad, archivo):
		self.nombre    = nombre
		self.apellidos = apellidos
		self.correo    = correo
		self.telefono  = telefono
		self.profesion = profesion
		self.edad      = edad
		self.archivo   = archivo

		if(self.nombre == "" or self.apellidos == "" or self.correo == "" or self.telefono == 0 or self.profesion == "" or self.edad == 0):
			messagebox.showwarning("aviso","Debe llenar todos los campos")

		else:
			try:
				with open(self.archivo, 'rb') as f:
					self.archivo = f.read()

				self.conexion = conexion()
				self.cursor = self.conexion.cursor()

				sql =("INSERT INTO datos (nombre, apellidos, correo, telefono, profesion, edad, archivo) VALUES (%s,%s,%s,%s,%s,%s,%s)")
				datos = self.nombre, self.apellidos, self.correo, self.telefono, self.profesion, self.edad, self.archivo

				self.cursor.execute(sql, datos)

				messagebox.showinfo("Aviso","La persona fue registrada con exito")

				self.cursor.close()
				self.conexion.close()

			except Exception as er:
				messagebox.showwarning("aviso","Seleccione el archivo")
				print("Error al insertar: ", er)

#-------------------------- INSERTAR- ---------------------------------------------

class App():
	def __init__(self, master):
		self.master = master
		master.title("Registro")
		master.resizable(0,0)

		#-----------VARIABLES-----------------------------------------------------
		self.nombre_var = tk.StringVar()
		self.apellidos_var = tk.StringVar()
		self.correo_var = tk.StringVar()
		self.telefono_var = tk.IntVar()
		self.profesion_var = tk.StringVar()
		self.edad_var = tk.IntVar()

		#-------------------- VENTANA CENTRADA --------------------------------------
		self.ancho_ventana = 950
		self.alto_ventana = 680

		self.x_ventana = self.master.winfo_screenwidth() // 2 - self.ancho_ventana // 2
		self.y_ventana = self.master.winfo_screenheight() // 2 - self.alto_ventana // 2

		self.posicion = str(self.ancho_ventana) + "x" + str(self.alto_ventana) + "+" + str(self.x_ventana) + "+" + str(self.y_ventana)
		self.master.geometry(self.posicion)

		#------------ CIRCULO DE FONDO ---------------------------------------------
		self.canvas = tk.Canvas(master, width=950, height=680,bg="#258FF9")
		self.canvas.pack()

		self.x = 50
		self.y = 50
		self.r = 500
		self.canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill="#0272E1", outline="")
		#---------------- FRAMES ---------------------------------------------------
		self.frame = tk.Frame(bg='#3398FC', width=890, height=590,
		 borderwidth=1, relief="raised").place(x=40, y=35)

		self.frameButtons = tk.Frame(bg='#E5E7EA', width=320, height=500,
		 borderwidth=1, relief="groove").place(x=45, y=50)

		self.frameData = tk.Frame(bg='#F2F2F2', width=320, height=500,
		 borderwidth=1, relief="flat").place(x=45, y=100)

		#-------------- IMAGEN -----------------------------------------------------
		self.image = Image.open("img/datos.png")
		self.image = self.image.resize((500,500),Image.LANCZOS)

		self.img = ImageTk.PhotoImage(self.image)
		tk.Label(self.frame, image = self.img, bg="#3398FC").place(x=390,y=100)

		#---------------- ENTRY ----------------------------------------------------
		tk.Label(text="Nombres", **styles.STYLE_Label).place(x=55, y=100)
		tk.Entry(master, self.frame, **styles.STYLE_Entry, textvariable = self.nombre_var).place(x=60, y=130)

		tk.Label(text="Apellidos", **styles.STYLE_Label).place(x=55, y=170)
		tk.Entry(master, self.frame, **styles.STYLE_Entry,textvariable = self.apellidos_var).place(x=60, y=200)

		tk.Label(text="Correo", **styles.STYLE_Label).place(x=55, y=240)
		tk.Entry(master, self.frame, **styles.STYLE_Entry,textvariable = self.correo_var).place(x=60, y=270)

		tk.Label(text="Telefono", **styles.STYLE_Label).place(x=55, y=310)
		tk.Entry(master, self.frame, **styles.STYLE_Entry,textvariable = self.telefono_var).place(x=60, y=340)

		tk.Label(text="Profesión", **styles.STYLE_Label).place(x=55, y=380)
		tk.Entry(master, self.frame, **styles.STYLE_Entry,textvariable = self.profesion_var).place(x=60, y=410)

		tk.Label(text="Edad", **styles.STYLE_Label).place(x=55, y=450)
		tk.Entry(master, self.frame, **styles.STYLE_Entry,textvariable = self.edad_var).place(x=60, y=480)

		#------------------- BOTONES ---------------------------------------------

		tk.Button(master, self.frame, text="Anexar Documentos",font=("poppins 10 bold"), bg="#F2F2F2", fg="#F10101", bd=0, command=self.archivo).place(x=50, y=520)

		tk.Button(master, self.frame, text="Añadir",**styles.STYLE_Boton, command=self.guardar_datos).place(x=50, y=555)

		tk.Button(self.frameButtons, text="Filtro    ",**styles.STYLE_Botons, command=self.filtro).place(x=48, y=54)
		tk.Button(self.frameButtons, text="Mas Datos",**styles.STYLE_Botons, command=self.more_data).place(x=210, y=54)

	#-------------------------FUNCIONES--------------------------------------------
		self.current_person = None

	#------------------------- ABRIR ARCHIVO---------------------------------------
	def archivo(self):
		self.archivo = filedialog.askopenfilename(title="buscar", initialdir="C:/", filetypes=(("pdf","*.pdf"),("excel","*xlxs")))
		return self.archivo
	#-------------------------MAS DATOS---------------------------------------
	def more_data(self):

		ventana = tk.Toplevel()
		ventana.title("Mas Datos")
		ventana.config(bg="#3398FC")

		ancho = 400
		alto  = 600

		x_ventana = ventana.winfo_screenwidth() // 2 - ancho // 2
		y_ventana = ventana.winfo_screenheight() // 2 - alto // 2

		posicion = str(ancho) + "x" + str(alto) + "+" + str(x_ventana) + "+" + str(y_ventana)
		ventana.geometry(posicion)

		tk.Label(ventana, text="Mensajes", fg="red").pack(pady=20)

		tk.Entry(ventana, fg="red").pack(pady=20)

		tk.Button(ventana, text="Boton", fg="red").pack(pady=20)

		tk.Entry(ventana).pack()
		tk.Label(ventana, text="Hola rosa").pack()


	#------------------------------------------------------------------------------
	def limpiarfiltro(self):
		self.listado.delete(*self.listado.get_children())

	#------------------------- FILTRAR LOS DATOS-----------------------------------

	def filtro(self):

		self.ventana = tk.Toplevel()
		self.ventana.title("Filtro")
		self.ventana.config(bg="#3398FC")
		self.ventana.resizable(0,0)

		ancho = 1200
		alto  = 600

		x_ventana = self.ventana.winfo_screenwidth() // 2 - ancho // 2
		y_ventana = self.ventana.winfo_screenheight() // 2 - alto // 2

		posicion = str(ancho) + "x" + str(alto) + "+" + str(x_ventana) + "+" + str(y_ventana)
		self.ventana.geometry(posicion)
		#------------------ FILTRO ------------------------------------------------

		self.listado = ttk.Treeview(self.ventana, columns=(1,2,3,4,5,6), show="headings", height="20")
		stilo= ttk.Style()
		stilo.theme_use("clam")

		stilo.configure("Treeview.Heading", background="#3398FC", relief="solid", foreground="#000", bd=1)
		self.listado.heading(1, text="Nombre")
		self.listado.heading(2, text="Apellidos")
		self.listado.heading(3, text="Correo")
		self.listado.heading(4, text="Telefono")
		self.listado.heading(5, text="Profesión")
		self.listado.heading(6, text="Edad")
		self.listado.column(1, anchor=tk_constants.CENTER)
		self.listado.column(2, anchor=tk_constants.CENTER)
		self.listado.column(3, anchor=tk_constants.CENTER)
		self.listado.column(4, anchor=tk_constants.CENTER)
		self.listado.column(5, anchor=tk_constants.CENTER)
		self.listado.column(6, anchor=tk_constants.CENTER)

		self.entry_edad = tk.IntVar()
		e_edad= tk.Entry(self.ventana, **styles.STYLE_Entry_V, textvariable=self.entry_edad).place(x=220, y=505)
		b_edad= tk.Button(self.ventana,**styles.STYLE_Boton_V_2 , text="Filtro Por Edad", command=lambda:filtro_edad(self, self.entry_edad.get())).place(x=20, y=500)

		self.entry_profesion = tk.StringVar()
		e_prof= tk.Entry(self.ventana, **styles.STYLE_Entry_V, textvariable=self.entry_profesion).place(x=220, y=555)
		b_prof= tk.Button(self.ventana,**styles.STYLE_Boton_V_2 , text="Filtro Por Profesión", command=lambda:filtro_profesion(self, self.entry_profesion.get())).place(x=20, y=550)

		self.entry_archivo = tk.StringVar()
		e_archivo= tk.Entry(self.ventana, **styles.STYLE_Entry_V, textvariable=self.entry_archivo).place(x=650, y=545)
		b_archivo= tk.Button(self.ventana, text="Buscar Archivo",**styles.STYLE_Boton_V, command=lambda:openpdf(self.entry_archivo.get())).place(x=840, y=540)
		tk.Label(self.ventana, text="Nombre",font=('poppins 14'), bg="#3398FC").place(x=650, y=515)

		for i in filtro_all(self): 
				self.listado.insert('', 'end', values=(i))
		self.listado.place(x=0,y=2)

	#------------------------- LIMPIAR LA LISTA--------------------------------------
	def datos_db(self, lista):

		self.limpiarfiltro()

		for i in lista: 
			self.listado.insert('', 'end', values=(i))


#-------------------- GUARDAR DATOS---------------------------------------------------
	def guardar_datos(self):

		if not self.current_person:
			self.current_person = Person(self.nombre_var.get(), 
			self.apellidos_var.get(), self.correo_var.get(), 
			self.telefono_var.get(), self.profesion_var.get(),
			self.edad_var.get(), self.archivo)	

		self.current_person = None

#--------------------------------------------------------------------------------------

root = tk.Tk()
app = App(root)
root.mainloop()