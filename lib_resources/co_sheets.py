import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import sys

def conectar_sheet():
    """Conecta a Google Sheets y devuelve el objeto de la hoja."""
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ruta_json = os.path.join(BASE_DIR, "..", "credentials", "credentials.json")
        
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(ruta_json, scope)
        client = gspread.authorize(creds)

        # Conexión específica a tu hoja
        sheet = client.open("rimac 24-25 ULTIMO").worksheet("2024")
        return sheet
    except Exception as e:
        print(f"Error conectando a Sheets: {e}")
        return None