import pymysql

def conexion():
	try:
		conexion = pymysql.connect(
			host = 'localhost',
			user = 'root',
			password = '',
			db = 'data_peoples'
		)

		return conexion

	except Exception as er:

		print(er)
		return false