# Data Pipeline Project

Arquitectura modular de procesamiento de datos basada en el patrón **Pipes & Filters**, 
diseñada para construir pipelines robustos, configurables y extensibles en Python.

---

## Tabla de contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Configuración (pipeline.yaml)](#configuración-pipelineyaml)
- [Flujo del pipeline](#flujo-del-pipeline)
- [Sistema de validación](#sistema-de-validación)
- [Semántica de validación](#semántica-de-validación)
- [Estado actual del sistema](#estado-actual-del-sistema)
- [Hoja de ruta](#hoja-de-ruta)
- [Testing](#testing)
- [Notas de diseño importantes](#notas-de-diseño-importantes)
- [Filosofía del proyecto](#filosofía-del-proyecto)

---

## Características

### Implementado

- **Data Sources**
  - `LoadCSVFilter` (fuente de datos)
  - `ChunkedCSVFilter` (base para escalabilidad)

- **Validation System**
  - `ValidationFilter` (entry point del subsistema de validación)
  - Reglas disponibles:
    - `required_columns`
    - `column_types`
    - `allowed_values`
    - `value_range`
  - Soporte para:
    - errores vs warnings
    - estrategias de fallo (`pre`, `post`, `threshold`)
    - manejo de filas inválidas (drop, separate)
  - Modelo de resultado consistente:
    - `is_row_level`
    - `invalid_rows` siempre lista

- **Cleaning**
  - `CleanDataFilter`
  - `DeduplicateFilter`

- **Type Conversion**
  - `DataTypeConverterFilter`
  - Soporte para:
    - datetime
    - timedelta con unidad
    - tipos nullable de pandas

- **Data Quality**
  - `DataQualityMetricsFilter`

- **Persistence**
  - `SaveCSVFilter`

---

## Arquitectura

Este proyecto implementa el patrón **Pipes & Filters** con una mejora clave:

### Separación explícita de responsabilidades

| Componente     | Responsabilidad |
|----------------|----------------|
| `DataSource`   | Generar datos (NO recibe entrada) |
| `DataFilter`   | Transformar datos |
| `DataPipeline` | Orquestar ejecución |

### Flujo:

```
DataSource → Filter → Filter → ... → Output
```

---

## Estructura del proyecto

```
.
├── config
│   └── pipeline.yaml
├── pyproject.toml
├── README.md
├── requirements.txt
├── scripts
│   └── run_pipeline.py
├── src
│   ├── data_pipeline
│   │   ├── core
│   │   │   ├── data_source.py
│   │   │   ├── filter_factory.py
│   │   │   ├── filter.py
│   │   │   ├── logger.py
│   │   │   └── pipeline.py
│   │   ├── filters
│   │   │   ├── aggregate_sales.py
│   │   │   ├── clean_data.py
│   │   │   ├── data_quality_metrics.py
│   │   │   ├── data_type_converter.py
│   │   │   ├── deduplicate.py
│   │   │   ├── filter_by_date.py
│   │   │   ├── load_csv_chunks.py
│   │   │   ├── load_csv.py
│   │   │   ├── save_csv.py
│   │   │   └── validation.py
│   │   ├── __init__.py
│   │   ├── utils
│   │   │   └── config_loader.py
│   │   └── validation
│   │       ├── engine
│   │       │   └── engine.py
│   │       ├── result.py
│   │       ├── rules
│   │       │   ├── base.py
│   │       │   ├── business
│   │       │   ├── rule_factory.py
│   │       │   └── schema
│   │       │       ├── allowed_values.py
│   │       │       ├── column_types.py
│   │       │       ├── required_columns.py
│   │       │       └── value_range.py
│   │       └── validation_report.py
│   └── data_pipeline.egg-info
│       ├── dependency_links.txt
│       ├── PKG-INFO
│       ├── SOURCES.txt
│       └── top_level.txt
└── tests
    ├── conftest.py
    ├── filters
    │   ├── test_clean_data_filter.py
    │   ├── test_data_quality_metrics_filter.py
    │   ├── test_deduplicate_filter.py
    │   ├── test_filter_by_date_filter.py
    │   └── test_save_csv_filter.py
    └── validation
        ├── rules
        │   ├── test_allowed_values_rule.py
        │   ├── test_column_types_rule.py
        │   ├── test_required_columns_rule.py
        │   └── test_value_range_rule.py
        ├── test_rule_engine.py
        ├── test_validation_report.py
        └── test_validation_result.py

```
> Nota: Las carpetas `schema/` y `business/` son solo una organización lógica.
> Ambas contienen reglas que implementan el mismo contrato (`ValidationRule`).
---

## Requisitos

- Python 3.8+
- pandas
- PyYAML
- pytest

---

## Instalación

```bash
git clone https://github.com/jamj-bot/data-pipeline-project.git
cd data-pipeline-project
pip install -r requirements.txt
```

Modo desarrollo:

```bash
pip install -e .
```

---

## Uso

### Ejecutar pipeline

```bash
python scripts/run_pipeline.py
```

---

## Configuración (pipeline.yaml)

La pipeline es **declarativa** y se define en YAML:

```yaml
pipeline:
  filters:
    - name: LoadCSVFilter
      params:
        file_path: data/raw/limited_dataset.csv

    - name: DataTypeConverterFilter
      params:
        dtype_mapping:
          DEP_DELAY: Int16

    - name: ValidationFilter
      params:
        rules:
          - type: required_columns
            columns: [DEP_DELAY]
```

---

## Flujo del pipeline

1. **Data Source**
   - Carga datos desde origen (CSV, DB, etc.)

2. **Transformaciones**
   - limpieza
   - conversión de tipos
   - filtros

3. **Validación**
   - reglas estructurales (dataset-level)
   - reglas semánticas (row-level)

4. **Salida**
   - persistencia
   - métricas

---

## Sistema de validación

### Unificación del sistema de validación

El sistema NO distingue entre validación de esquema y validación de negocio a nivel de ejecución.

Todas las reglas:

- implementan `ValidationRule`
- se ejecutan a través de `RuleEngine`
- devuelven `ValidationResult`

La distinción entre reglas (estructurales vs negocio) es únicamente organizacional, no arquitectónica.

### Punto de entrada

El sistema de validación es ejecutado a través de un único filtro:

- `ValidationFilter`

Este filtro actúa como punto de contacto entre el pipeline y el subsistema de validación.

No existe distinción a nivel de ejecución entre:

- validación de esquema
- validación de negocio

Ambos tipos de reglas son procesados de forma uniforme.

### Componentes

- `RuleEngine`
- `ValidationRule`
- `ValidationResult`
- `ValidationReport`

### Tipos de reglas

El sistema distingue explícitamente entre dos tipos de reglas:

| Tipo            | Ejemplo              | is_row_level | invalid_rows |
|-----------------|---------------------|-------------|--------------|
| estructural     | required_columns    | False        | []           |
| semántica       | value_range         | True         | [indices]    |

---

### Modelo de resultado (`ValidationResult`)

Cada regla devuelve un objeto con semántica explícita:

- `is_row_level`
  - Indica si la regla opera a nivel fila
- `invalid_rows`
  - Siempre es una lista (nunca `None`)
  - Solo tiene valores si `is_row_level = True`

Esto elimina ambigüedad y permite un manejo consistente en todo el sistema.

### Capacidades

- errores vs warnings
- row-level tracking (`invalid_rows`)
- diferenciación explícita entre reglas estructurales y row-level
- fail strategies:
  - `pre`
  - `post`
  - `threshold`

---

## Semántica de validación

El sistema separa explícitamente dos niveles de validación:

### 1. Dataset-level (estructural)
- Validan la estructura del DataFrame
- Ejemplos:
  - columnas requeridas
  - tipos de datos
- No operan sobre filas individuales

### 2. Row-level (semántica)
- Validan valores dentro de las filas
- Ejemplos:
  - rangos numéricos
  - valores permitidos
- Permiten:
  - drop de filas
  - separación de registros inválidos

---

### Implicación clave

Solo las reglas **row-level** afectan:

- `invalid_rows`
- acciones como `drop` o `separate`
- estrategias `threshold`

Las reglas estructurales solo afectan el estado global de validación.

## Estado actual del sistema

### Estable

- Pipeline core
- Configuración YAML
- Sistema de validación base
- Type conversion

### Parcial

- Cleaning avanzado
- Deduplicación
- Data quality metrics

### Pendiente

- Enrichment
- Aggregation
- Persistencia avanzada
- Streaming real

---

## Hoja de ruta

### Próximos módulos

- Feature Engineering
- Enrichment (joins externos)
- Aggregation
- Persistencia en Parquet / DB

### Validación avanzada

- integridad referencial
- reglas cross-column
- reglas dependientes

### Escalabilidad

- soporte real para chunking
- streaming pipeline

---

## Testing

Ejecutar tests:

```bash
# Instalar pytest si no está instalado
pip install pytest pytest-mock

# Ejecutar todos los tests
pytest tests/

# Ejecutar con cobertura
pytest tests/ --cov=src/data_pipeline --cov-report=html

# Ejecutar categoría específica
pytest tests/validation/
pytest tests/filters/

# Ejecutar con verbose
pytest tests/ -v

# Ejecutar un test específico
pytest tests/validation/test_validation_result.py::TestValidationResult::test_creation_valid_result

```

### Cobertura actual

- filtros básicos

### Pendiente

- validation engine
- rules
- pipeline end-to-end

---

## Notas de diseño importantes

- El primer componente **NO es un filtro**, es un `DataSource`
- Todas las reglas devuelven `invalid_rows`, pero:
  - reglas estructurales → siempre `[]`
  - reglas row-level → lista de índices inválidos
- El flag `is_row_level` define cómo debe interpretarse el resultado
- Los filtros trabajan sobre `pandas.DataFrame`
- El sistema es **config-driven** (YAML)

---

## Filosofía del proyecto

Este proyecto busca evolucionar hacia:

- un **framework de pipelines**
- altamente configurable
- extensible
- con validación robusta
- y separación clara de responsabilidades

---
