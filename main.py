import os
import json
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

class SeguridadLaboral:
    def __init__(self):
        self.factor = 200000
        self.trabajadores = 25
        self.horas_dia = 8
        self.dias_mes = 22  # Días laborales promedio por mes
        self.horas_mes = self.trabajadores * self.horas_dia * self.dias_mes
        
        # Configurar Google Sheets
        self.setup_google_sheets()
        
    def setup_google_sheets(self):
        """Configura la conexión con Google Sheets"""
        try:
            # Obtener credenciales desde variable de entorno
            creds_json = os.getenv('GOOGLE_CREDENTIALS')
            if not creds_json:
                raise ValueError("No se encontraron las credenciales de Google")
            
            creds_dict = json.loads(creds_json)
            
            # Configurar scopes
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Crear credenciales
            creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
            
            # Conectar con Google Sheets
            self.gc = gspread.authorize(creds)
            
            # Abrir hoja
            sheet_id = os.getenv('SHEET_ID')
            if not sheet_id:
                raise ValueError("No se encontró el ID de la hoja")
            
            self.sheet = self.gc.open_by_key(sheet_id).sheet1
            
            # Configurar encabezados si es necesario
            self.setup_headers()
            
        except Exception as e:
            print(f"Error configurando Google Sheets: {e}")
            raise
    
    def setup_headers(self):
        """Configura los encabezados de la hoja si están vacíos"""
        try:
            # Verificar si ya hay encabezados
            first_row = self.sheet.row_values(1)
            if not first_row:
                headers = [
                    'Mes', 'Mes Numero', 'Sede', 'Incidentes', 'Accidentes',
                    'Indice de Frecuencia', 'Indice de Severidad', 'Indice de Accidentabilidad',
                    'Actos Inseguros Reportados', 'Actos Inseguros Cerrados',
                    'Condiciones Inseguras Reportadas', 'Condiciones Inseguras Cerradas',
                    'Capacitaciones Programadas', 'Capacitaciones Ejecutadas',
                    'Inspecciones Programadas', 'Inspecciones Ejecutadas',
                    'Actividades PASST Programadas', 'Actividades PASST Ejecutadas',
                    'Actividades PASST Ejecutadas Acumuladas'
                ]
                self.sheet.append_row(headers)
                print("Encabezados configurados correctamente")
        except Exception as e:
            print(f"Error configurando encabezados: {e}")
    
    def calcular_indices(self, accidentes, dias_perdidos=0):
        """Calcula los índices de seguridad"""
        # Índice de Frecuencia
        if_value = (accidentes * self.factor) / self.horas_mes if self.horas_mes > 0 else 0
        
        # Índice de Severidad
        is_value = (dias_perdidos * self.factor) / self.horas_mes if self.horas_mes > 0 else 0
        
        # Índice de Accidentabilidad
        ia_value = (if_value * is_value) / 1000 if if_value > 0 and is_value > 0 else 0
        
        return if_value, is_value, ia_value
    
    def obtener_acumulado_passt(self, mes_actual):
        """Obtiene el acumulado de actividades PASST hasta el mes anterior"""
        try:
            all_records = self.sheet.get_all_records()
            acumulado = 0
            
            for record in all_records:
                mes_numero = record.get('Mes Numero', 0)
                if isinstance(mes_numero, int) and mes_numero < mes_actual:
                    actividades = record.get('Actividades PASST Ejecutadas', 0)
                    if isinstance(actividades, (int, float)):
                        acumulado += actividades
            
            return acumulado
        except Exception as e:
            print(f"Error calculando acumulado: {e}")
            return 0
    
    def registrar_datos(self, datos):
        """Registra los datos en Google Sheets"""
        try:
            # Obtener mes actual
            mes_actual = datetime.now().month
            nombre_mes = datetime.now().strftime('%B')
            
            # Calcular índices
            if_val, is_val, ia_val = self.calcular_indices(
                datos['accidentes'], 
                datos.get('dias_perdidos', 0)
            )
            
            # Obtener acumulado PASST
            acumulado_passt = self.obtener_acumulado_passt(mes_actual)
            nuevo_acumulado = acumulado_passt + datos['actividades_passt_ejecutadas']
            
            # Preparar fila de datos
            fila = [
                nombre_mes,  # Mes
                mes_actual,  # Mes Numero
                datos['sede'],  # Sede
                datos['incidentes'],  # Incidentes
                datos['accidentes'],  # Accidentes
                round(if_val, 2),  # Indice de Frecuencia
                round(is_val, 2),  # Indice de Severidad
                round(ia_val, 2),  # Indice de Accidentabilidad
                datos['actos_inseguros_reportados'],  # Actos Inseguros Reportados
                datos['actos_inseguros_cerrados'],  # Actos Inseguros Cerrados
                datos['condiciones_inseguras_reportadas'],  # Condiciones Inseguras Reportadas
                datos['condiciones_inseguras_cerradas'],  # Condiciones Inseguras Cerradas
                datos['capacitaciones_programadas'],  # Capacitaciones Programadas
                datos['capacitaciones_ejecutadas'],  # Capacitaciones Ejecutadas
                datos['inspecciones_programadas'],  # Inspecciones Programadas
                datos['inspecciones_ejecutadas'],  # Inspecciones Ejecutadas
                datos['actividades_passt_programadas'],  # Actividades PASST Programadas
                datos['actividades_passt_ejecutadas'],  # Actividades PASST Ejecutadas
                nuevo_acumulado  # Actividades PASST Ejecutadas Acumuladas
            ]
            
            # Insertar fila
            self.sheet.append_row(fila)
            print(f"Datos registrados correctamente para {nombre_mes}")
            
            # Mostrar resumen
            self.mostrar_resumen(datos, if_val, is_val, ia_val, nuevo_acumulado)
            
        except Exception as e:
            print(f"Error registrando datos: {e}")
            raise
    
    def mostrar_resumen(self, datos, if_val, is_val, ia_val, acumulado):
        """Muestra un resumen de los datos registrados"""
        print("\n" + "="*50)
        print("RESUMEN DE DATOS REGISTRADOS")
        print("="*50)
        print(f"Sede: {datos['sede']}")
        print(f"Mes: {datetime.now().strftime('%B %Y')}")
        print(f"Horas hombre trabajadas: {self.horas_mes}")
        print(f"Incidentes: {datos['incidentes']}")
        print(f"Accidentes: {datos['accidentes']}")
        print(f"Índice de Frecuencia: {if_val:.2f}")
        print(f"Índice de Severidad: {is_val:.2f}")
        print(f"Índice de Accidentabilidad: {ia_val:.2f}")
        print(f"Actividades PASST Acumuladas: {acumulado}")
        print("="*50)

def main():
    """Función principal - Aquí defines los datos del mes"""
    
    # Crear instancia del sistema
    sistema = SeguridadLaboral()
    
    # DATOS DEL MES ACTUAL
    # Modifica estos valores según los datos reales del mes
    datos_mes = {
        'sede': 'Bertello',  # Cambia por: 'Bertello', 'Facuccet', u otra
        'incidentes': 2,
        'accidentes': 0,
        'dias_perdidos': 0,  # Solo si hay accidentes
        'actos_inseguros_reportados': 5,
        'actos_inseguros_cerrados': 3,
        'condiciones_inseguras_reportadas': 8,
        'condiciones_inseguras_cerradas': 6,
        'capacitaciones_programadas': 4,
        'capacitaciones_ejecutadas': 4,
        'inspecciones_programadas': 12,
        'inspecciones_ejecutadas': 10,
        'actividades_passt_programadas': 6,
        'actividades_passt_ejecutadas': 5
    }
    
    # Registrar datos
    try:
        sistema.registrar_datos(datos_mes)
        print("✅ Proceso completado exitosamente")
    except Exception as e:
        print(f"❌ Error en el proceso: {e}")

if __name__ == "__main__":
    main()
