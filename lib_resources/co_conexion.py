import pyodbc
print(pyodbc.drivers())
class DataBase:
    def __init__(self):
        try:
            # CONFIGURACIÓN (Ajusta estos datos)
            self.server = '10.7.3.20' # <--- Pon la IP completa
            self.database = 'ghq_crp_pro'
            self.username = 'crp_bi'
            self.password = 'AUCnv6TJXE3gSm4'
            self.port = '9801' # OJO: ¿El puerto es 01? SQL Server suele usar 1433. Confirma esto.
            
            # CADENA DE CONEXIÓN (Connection String)
            # Intentamos usar el driver más común. Si falla, prueba con 'SQL Server'
            self.connection_string = (
                f'DRIVER={{SQL Server}};'
                f'SERVER={self.server},{self.port};' # Nota la coma entre server y puerto
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
            # Tip: A veces ayuda imprimir los drivers disponibles si falla
            print("Drivers disponibles:", pyodbc.drivers())

    def ConsultaBoletas(self, ids_formateados):
        # El query sigue siendo el mismo SQL estándar
        sql = f"select fvh_numero, fvh_estado_doc from fas_factura_venta where fvh_numero in ({ids_formateados});"
        try:
            self.cursor.execute(sql)
            info = self.cursor.fetchall()
            
            # CONVERTIR A DICCIONARIO (Para que tu código siga funcionando igual)
            # pyodbc devuelve tuplas [(dato1, dato2), ...]
            # Lo transformamos a diccionario: {'F421-001': 'E', ...}
            resultados_dict = {}
            for row in info:
                # row[0] es fvh_numero, row[1] es fvh_estado_doc
                resultados_dict[row[0]] = row[1]
                
            return resultados_dict
            
        except Exception as e:
            print(f"Error al ejecutar ConsultaBoletas: {str(e)}")
            return {}
            
    def cerrar(self):
        self.connection.close()