# Data Pipeline Project

Arquitectura robusta de pipeline de datos basada en el patrón **Pipes & Filters**, 
diseñada para procesar, limpiar y transformar datos en Python.

## Tabla de contenidos
- [Características](#características)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Uso](#arquitectura)
- [Hoja de ruta](#hoja-de-ruta)
- [Contribución y testing](#contribucion-y-testing)

## Características

**Implementado:**
- Ingestion: LoadCSVFilter, ChunkedCSVFilter
- Schema Validation: validación de columnas, tipos y valores permitidos
- Cleaning: deduplicación, manejo de valores faltantes
- Type Conversion: soporte para datetime, int nullable, timedelta
- Data Quality Metrics: cálculo de proporción de nulls, estadísticas

**En desarrollo / Roadmap:**
- Advanced validation (rangos, integridad referencial)
- Feature Engineering
- Enrichment (lookups, joins externos)
- Aggregation
- Persistence (Parquet, bases de datos)

## Estructura del proyecto
data_pipeline_project/ 
├── data/ 
│ └── raw/ # Datos de entrada 
│   └── sales.csv 
├── src/data_pipeline/ 
│ ├── core/ 
│ │ ├── filter.py # Clase base Filter 
│ │ └── pipeline.py # Orquestador del pipeline 
│ └── filters/ # Filtros específicos 
│   ├── load_csv.py 
│   ├── clean_data.py 
│   └── aggregate_sales.py 
├── tests/ # Suite de tests 
├── scripts/ 
│ └── run_pipeline.py # Script de ejecución 
└── pyproject.toml

## Requisitos

- Python 3.8+
- pandas >= 1.0
- pytest (para tests)

*Ver `requirements.txt` para todas las dependencias*

## Instalación

1. Clonar el repositorio:
bash
git clone https://github.com/jamj-bot/data-pipeline-project.git
cd data-pipeline-project

2. Instalar dependencias:
pip install -r requirements.txt

3. (Opcional) Instalar en modo desarrollo:
pip install -e .

### **7. Uso / Ejemplo rápido**
from src.data_pipeline.pipeline import Pipeline
from src.data_pipeline.filters import LoadCSVFilter, CleanDataFilter

pipeline = Pipeline()
pipeline.add_filter(LoadCSVFilter('data/raw/sales.csv'))
pipeline.add_filter(CleanDataFilter())
result = pipeline.execute()

### **8. Arquitectura del patrón Pipes & Filters**
Este proyecto implementa el patrón Pipes & Filters:

Filters: Cada componente es responsable de una única tarea
Pipes: El Pipeline orquesta el flujo de datos entre filtros
Ventajas:
Modularidad y testabilidad
Fácil de extender con nuevos filtros
Separación clara de responsabilidades

### **9. Hoja de ruta / Roadmap**
Agregar OutlierRemovalFilter (IQR, Z-score)
Implementar FeatureEngineeringFilter
Agregar persistencia en Parquet
Validación de rangos y integridad referencial
Metrics de drift detection

### **10. Contribución y testing**
pytest tests/

- 1. INGESTION: cargar datos desde fuentes externas.

    - Filtros existentes:
        * LoadCSVFilter → carga el CSV completo en memoria.
        * ChunkedCSVFilter → carga CSV por bloques (escalable, aunque actualmente comentado).

    - Filtros faltantes recomendados:
        * LoadParquetFilter → para datasets grandes optimizados.
        * DatabaseIngestionFilter → ingestión desde bases de datos.
        * APIIngestionFilter → ingestión desde servicios externos.

    - Estado general: BIEN

- 2. SCHEMA VALIDATION: validar que los datos cumplen el contrato estructural.

    - Filtros existentes:
        * SchemaValidationFilter
            - required_columns → valida columnas requeridas.
            - column_types → valida tipos de datos esperados.
            - allowed_values → valida que los datos pertenezcan a un conjunto definido por el esquema.

    - Filtros faltantes recomendados:
        * ColumnRangeValidationFilter → valida rangos lógicos (ej. AIR_TIME >= 0).
        * ReferentialIntegrityFilter → valida relaciones entre datasets.

    - Estado general: BÁSICO

- 3. CLEANING: limpiar datos inconsistentes o problemáticos.

    - 3.1 Null Handling: manejar valores faltantes.

        - Filtros existentes:
            * CleanDataFilter (probablemente cubre parcialmente esta función).

        - Filtros faltantes recomendados:
            * MissingValueHandlerFilter
                - Operaciones típicas:
                    - eliminar filas con nulls
                    - imputación
                    - rellenado con valores por defecto

        - Estado: PARCIAL

    - 3.2 Deduplication: eliminar duplicados.

        - Filtros existentes:
            * DeduplicateFilter

        - Estado: COMPLETO

    - 3.3 Invalid Values Handling: eliminar o corregir valores lógicamente inválidos.

        - Filtros faltantes:
          * InvalidValueFilter
            - Ejemplos:
                * AIR_TIME negativo
                * DISTANCE <= 0
                * DEP_DELAY fuera de rangos válidos

        - Estado: FALTANTE

    - 3.4 Outlier Handling: controlar valores extremos estadísticos.

        - Filtros faltantes:
            * OutlierRemovalFilter
            * OutlierCappingFilter

        - Métodos comunes:
            * IQR
            * Z-score
            * Percentiles

        - Estado: FALTANTE

4. TRANSFORMATION: transformar estructura o semántica de los datos.

    - 4.1 Type Conversion

        - Filtros existentes:
            * DataTypeConverterFilter
                Soporta:
                - datetime
                - tipos enteros nullable
                - timedelta con metadata de unidad

        - Estado: BIEN IMPLEMENTADO

        - 4.2 Feature Engineering: crear nuevas columnas derivadas.

            - Filtros faltantes:
                * DerivedColumnsFilter
                * FeatureEngineeringFilter

            - Ejemplos:
                - velocidad = DISTANCE / AIR_TIME
                - categoría de retraso
                - duración del vuelo

            - Estado: FALTANTE

5. ENRICHMENT: agregar información externa o contextual.

    - Filtros faltantes:
        * LookupEnrichmentFilter
        * MetadataJoinFilter
        * GeoEnrichmentFilter

    - Ejemplos:
        - unir con tabla de aeropuertos
        - unir con zonas horarias
        - unir con datos climatológicos

    - Estado: NO IMPLEMENTADO

6. QUALITY METRICS / PROFILING: monitoreo y observabilidad del dataset.

    - Filtros existentes:
        * DataQualityMetricsFilter
        * Normalmente calcula:
            - proporción de nulls
            - estadísticas descriptivas
            - distribución de valores

    - Filtros faltantes:
        * DriftDetectionFilter (comparación entre ejecuciones)

    - Estado: PRESENTE PERO EXPANDIBLE

7. AGGREGATION: generar datasets resumidos o analíticos.

    - Filtros faltantes:
        * AggregationFilter

    - Ejemplos:
        * retraso promedio por aeropuerto
        * tiempo promedio por aerolínea
        * WindowAggregationFilter
        * Métricas temporales o por ventana

    - Estado: NO IMPLEMENTADO

8. PERSISTENCE: guardar resultados del pipeline.

    - Filtros existentes:
        * SaveCSVFilter

    - Filtros faltantes:
        * SaveParquetFilter
        * DatabaseWriterFilter

    - Estado: PARCIAL

