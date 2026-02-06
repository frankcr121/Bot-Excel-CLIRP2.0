import pyodbc
print(pyodbc.drivers())
class DataBase:
    def __init__(self):
        try:
        
            self.server = '' 
            self.database = ''
            self.username = ''
            self.password = ''
            self.port = '' 
            
            self.connection_string = (
                f'DRIVER={{SQL Server}};'
                f'SERVER={self.server},{self.port};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password};'
                'Encrypt=yes;'                
                'TrustServerCertificate=yes;'
            )
            
            self.connection = pyodbc.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            print(">>> ¡Conexión ODBC a base de datos exitosa!")
            
        except Exception as e:
            print(f"Error fatal conectando a BD: {e}")
        
            print("Drivers disponibles:", pyodbc.drivers())

    def ConsultaBoletas(self, ids_formateados):
        sql = f"select fvh_numero, fvh_estado_doc from fas_factura_venta where fvh_numero in ({ids_formateados});"
        try:
            self.cursor.execute(sql)
            info = self.cursor.fetchall()
            resultados_dict = {}
            for row in info:
                resultados_dict[row[0]] = row[1]  
            return resultados_dict
        except Exception as e:
            print(f"Error al ejecutar ConsultaBoletas: {str(e)}")
            return {}
            
    def cerrar(self):

        self.connection.close()
