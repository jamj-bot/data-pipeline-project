# Nombre del Proyecto

Data Pipeline Project

## Descripción

Proyecto básico pero conceptualmente robusto para una aplicación de análisis de datos que
es una base sólida para posteriormente poder construir aplicaciones más complejas y avanzadas.
Se enfoca en:

    1. Arquitectura Pipers & Filters
    2. Separación de responsabilidades
    3. POO básica pero bien implementada
    4. Tipado
    5. Tests básicos
    6. Estructura de carpetas limpia


    data_pipeline_project/
    ├── data/
    │   └── raw/
    │       └── sales.csv
    │
    ├── src/
    │   └── data_pipeline/
    │       ├── core/
    │       │   ├── filter.py
    │       │   └── pipeline.py
    │       │
    │       ├── filters/
    │       │   ├── load_csv.py
    │       │   ├── clean_data.py
    │       │   └── aggregate_sales.py
    │       │
    │       └── __init__.py
    │
    ├── tests/
    │   └── test_clean_data.py
    │
    ├── scripts/
    │   └── run_pipeline.py
    │
    ├── pyproject.toml
    ├── requirements.txt
    └── README.md


## Características

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

## Requisitos

- Python 3.8+
- pandas
- (otras dependencias)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/tu-proyecto.git

# Entrar al directorio
cd tu-proyecto

# Instalar dependencias
pip install -r requirements.txt


