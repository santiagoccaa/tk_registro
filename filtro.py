from conexion import conexion
import subprocess
from tkinter import messagebox

def filtro_all(self):
	try:
		conn = conexion()

		cursor = conn.cursor()

		query=("SELECT nombre, apellidos, correo, telefono, profesion, edad FROM datos")
		cursor.execute(query)
		self.resultado =cursor.fetchall()

		return self.resultado

	except Exception as er:
		messagebox.showwarning('ERROR', er)

def filtro_edad(self, edad):

	try:
		conn = conexion()

		cursor = conn.cursor()

		query=("SELECT nombre, apellidos, correo, telefono, profesion, edad FROM datos WHERE edad ={}".format(edad))
		cursor.execute(query)
		self.resultado =cursor.fetchall()

		return self.datos_db(self.resultado)

	except Exception as er:
		messagebox.showwarning('ERROR', er)

def filtro_profesion(self, data):

	try:
		conn = conexion()

		cursor = conn.cursor()
		query=("SELECT nombre, apellidos, correo, telefono, profesion, edad FROM datos WHERE profesion = '{}'".format(data))

		cursor.execute(query)
		self.resultado =cursor.fetchall()

		return self.datos_db(self.resultado)

	except Exception as er:
		messagebox.showwarning('ERROR', er)


def openpdf(dato):

	if dato == "":
		messagebox.showwarning("ERROR", "DEBE INGREAR UN NOMBRE")
	else:
		conn = conexion()
		cursor = conn.cursor()

		query = "SELECT archivo FROM datos WHERE nombre = '{}'".format(dato)
		cursor.execute(query)
		resultado = cursor.fetchone()

		with open('temp.pdf', 'wb') as archivo_temporal:
		    archivo_temporal.write(resultado[0])

		subprocess.run(['start', '', 'temp.pdf'], shell=True)
