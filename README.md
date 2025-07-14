# Sistema de Gestión de Seguridad Laboral

Sistema automatizado para registrar y calcular indicadores de seguridad laboral en Google Sheets.

## 🚀 Características

- ✅ Registro automático de datos mensuales
- ✅ Cálculo automático de índices de seguridad
- ✅ Integración con Google Sheets
- ✅ Ejecución automatizada en GitHub Actions
- ✅ Acumulado de actividades PASST

## 📊 Datos que registra

- Mes y número de mes
- Sede
- Incidentes y accidentes
- Índice de frecuencia, severidad y accidentabilidad
- Actos y condiciones inseguras (reportados/cerrados)
- Capacitaciones e inspecciones (programadas/ejecutadas)
- Actividades PASST (programadas/ejecutadas/acumuladas)

## 🔧 Configuración

### 1. Variables de entorno requeridas:
- `GOOGLE_CREDENTIALS`: JSON completo de service account de Google
- `SHEET_ID`: ID de la hoja de Google Sheets

### 2. Configuración de datos:
Edita el archivo `main.py` en la sección `datos_mes` para actualizar los valores mensuales.

## 📈 Fórmulas utilizadas

- **Índice de Frecuencia**: `(N° accidentes × 200,000) / Horas hombre trabajadas`
- **Índice de Severidad**: `(N° días perdidos × 200,000) / Horas hombre trabajadas`
- **Índice de Accidentabilidad**: `(IF × IS) / 1,000`

## 🏢 Configuración de empresa

- **Trabajadores**: 25
- **Horas por día**: 8
- **Días laborales por mes**: 22
- **Factor de cálculo**: 200,000

## 🔄 Ejecución

### Automática:
- Se ejecuta el primer día de cada mes a las 9:00 AM
- Se ejecuta en cada push a la rama main

### Manual:
1. Ve a la pestaña "Actions" en GitHub
2. Selecciona "Sistema Seguridad Laboral"
3. Clic en "Run workflow"

## 📝 Cómo usar

1. **Cada mes**: Edita los valores en `datos_mes` del archivo `main.py`
2. **Commit y push**: Los cambios se procesarán automáticamente
3. **Verificar**: Revisa los datos en tu Google Sheet

## 🛠️ Ejemplo de uso mensual

```python
datos_mes = {
    'sede': 'Bertello',  # o 'Facuccet'
    'incidentes': 2,
    'accidentes': 0,
    'dias_perdidos': 0,
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
```

## 🔍 Solución de problemas

### Error de credenciales:
- Verifica que `GOOGLE_CREDENTIALS` contenga el JSON completo
- Asegúrate de que la service account tenga permisos en la hoja

### Error de Sheet ID:
- Verifica que `SHEET_ID` sea correcto
- Confirma que la hoja esté compartida con la service account

### Error de cálculos:
- Revisa que los datos de entrada sean números válidos
- Verifica la configuración de horas trabajadas

## 📞 Soporte

Para reportar problemas o solicitar mejoras, crea un issue en este repositorio.
