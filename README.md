# Data Pipeline Project

Arquitectura modular de procesamiento de datos basada en el patrón **Pipes & Filters**,
diseñada para construir pipelines robustos, configurables y extensibles en Python.

---

## Tabla de contenidos

* [Características](#características)
* [Arquitectura](#arquitectura)
* [Estructura del proyecto](#estructura-del-proyecto)
* [Requisitos](#requisitos)
* [Instalación](#instalación)
* [Uso](#uso)
* [Configuración (pipeline.yaml)](#configuración-pipelineyaml)
* [Flujo del pipeline](#flujo-del-pipeline)
* [Sistema de validación](#sistema-de-validación)
* [Semántica de validación](#semántica-de-validación)
* [Sistema de tipos y conversiones](#sistema-de-tipos-y-conversiones)
* [Testing](#testing)
* [Estado actual del sistema](#estado-actual-del-sistema)
* [Hoja de ruta](#hoja-de-ruta)
* [Notas de diseño importantes](#notas-de-diseño-importantes)
* [Filosofía del proyecto](#filosofía-del-proyecto)

---

## Características

### Implementado

* **Data Sources**

  * `LoadCSVPump`

* **Data Sinks**

  * `SaveCSVSink`

* **Validation System**

  * `ValidationFilter` (entry point del subsistema de validación)
  * `RuleEngine`
  * `ValidationReport`
  * `ValidationResult`

* **Reglas disponibles**

  * `required_columns`
  * `column_types`
  * `allowed_values`
  * `value_range`

* **Soporte de validación**

  * errores vs warnings
  * estrategias de fallo:

    * `pre`
    * `post`
    * `threshold`
  * manejo de filas inválidas:

    * `keep`
    * `drop`
    * `separate`
  * persistencia opcional de reportes JSON
  * persistencia opcional de filas inválidas
  * tracking row-level mediante `invalid_rows`

* **Cleaning**

  * `CleanDataFilter`
  * `DeduplicateFilter`

* **Filtering**

  * `FilterByDateRange`

* **Type Conversion**

  * `DataTypeConverterFilter`
  * Soporte para:

    * datetime
    * timedelta con unidad
    * tipos nullable de pandas
    * coerción numérica
    * boolean nullable

* **Data Quality**

  * `DataQualityMetricsFilter`

* **Configuración global**

  * pandas Copy-on-Write habilitado globalmente

---

## Arquitectura

Este proyecto implementa el patrón **Pipes & Filters** con separación explícita de responsabilidades.

### Componentes principales

| Componente     | Responsabilidad                   |
| -------------- | --------------------------------- |
| `DataSource`   | Generar datos (NO recibe entrada) |
| `DataFilter`   | Transformar o validar datos       |
| `DataSink`     | Persistir datos                   |
| `DataPipeline` | Orquestar ejecución               |

### Flujo

```text
DataSource → Filter → Filter → ... → DataSink
```

### Principios arquitectónicos actuales

* separación estricta entre source/filter/sink
* pipeline declarativo basado en YAML
* reglas desacopladas del pipeline
* validación uniforme mediante `RuleEngine`
* diseño orientado a composición
* Copy-on-Write habilitado para reducir mutabilidad accidental

---

## Estructura del proyecto

```text
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
│   │   │   ├── data_sink.py
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
│   │   │   └── validation.py
│   │   ├── __init__.py
│   │   ├── sinks
│   │   │   ├── __init__.py
│   │   │   └── save_csv.py
│   │   ├── sources
│   │   │   ├── __init__.py
│   │   │   └── load_csv.py
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
    │   ├── sinks
    │   ├── test_clean_data_filter.py
    │   ├── test_data_quality_metrics_filter.py
    │   ├── test_deduplicate_filter.py
    │   ├── test_filter_by_date_filter.py
    │   └── test_validation_filter.py
    ├── sinks
    │   └── test_save_csv_filter.py
    ├── sources
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

> Nota: Las carpetas `schema/` y `business/` son una organización lógica.
> Todas las reglas implementan el mismo contrato (`ValidationRule`).

---

## Requisitos

* Python 3.10+
* pandas
* PyYAML
* pytest
* pytest-mock

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

La pipeline es declarativa y se define mediante YAML.

```yaml
pipeline:
  filters:
    - name: LoadCSVPump
      params:
        file_path: data/raw/dataset.csv

    - name: DataTypeConverterFilter
      params:
        dtype_mapping:
          DEP_DELAY:
            dtype: Int16

          ARRIVAL_TIME:
            dtype: datetime
            utc: true

          DURATION:
            dtype: timedelta
            unit: minutes

    - name: ValidationFilter
      params:
        rules:
          - type: required_columns
            columns: [DEP_DELAY]

          - type: value_range
            schema:
              DEP_DELAY:
                min: 0
                max: 500

        fail_on:
          error:
            strategy: threshold
            threshold: 0.10

        row_actions:
          error: separate

        invalid_rows_path: data/invalid

    - name: SaveCSVSink
      params:
        output_path: data/output/clean.csv
```

---

## Flujo del pipeline

1. **Data Source**

   * carga datos desde CSV

2. **Transformaciones**

   * limpieza
   * deduplicación
   * conversión de tipos
   * filtros temporales

3. **Validación**

   * reglas estructurales (dataset-level)
   * reglas semánticas (row-level)

4. **Persistencia**

   * exportación CSV
   * reportes de validación
   * persistencia de filas inválidas

---

## Sistema de validación

### Unificación del sistema

El sistema NO distingue entre validación estructural y validación de negocio a nivel de ejecución.

Todas las reglas:

* implementan `ValidationRule`
* son ejecutadas por `RuleEngine`
* producen `ValidationResult`

La separación entre reglas estructurales y de negocio es únicamente organizacional.

### Punto de entrada

El subsistema de validación se integra al pipeline mediante:

* `ValidationFilter`

Este filtro:

* ejecuta reglas
* genera reportes
* maneja estrategias de fallo
* aplica acciones row-level
* puede persistir filas inválidas

### Componentes

| Componente         | Responsabilidad      |
| ------------------ | -------------------- |
| `RuleEngine`       | Ejecutar reglas      |
| `ValidationRule`   | Contrato base        |
| `ValidationResult` | Resultado individual |
| `ValidationReport` | Resultado agregado   |

### Tipos de reglas

| Tipo        | Ejemplo          | is_row_level | invalid_rows |
| ----------- | ---------------- | ------------ | ------------ |
| estructural | required_columns | False        | []           |
| semántica   | value_range      | True         | [indices]    |

---

### Modelo de resultado (`ValidationResult`)

Cada regla devuelve un objeto con semántica explícita:

* `is_row_level`

  * indica si la regla opera a nivel fila

* `invalid_rows`

  * siempre es una lista
  * nunca `None`
  * solo contiene valores si `is_row_level=True`

Esto elimina ambigüedad y permite un manejo uniforme dentro del engine.

---

### Estrategias de fallo

| Estrategia  | Descripción                                 |
| ----------- | ------------------------------------------- |
| `pre`       | falla antes de aplicar acciones row-level   |
| `post`      | falla después de aplicar acciones row-level |
| `threshold` | falla si el ratio inválido excede el umbral |

---

### Row actions

| Acción     | Descripción                                 |
| ---------- | ------------------------------------------- |
| `keep`     | conserva filas inválidas                    |
| `drop`     | elimina filas inválidas                     |
| `separate` | exporta filas inválidas y luego las elimina |

---

## Semántica de validación

El sistema separa explícitamente dos niveles de validación.

### 1. Dataset-level (estructural)

Validan estructura global del DataFrame.

Ejemplos:

* columnas requeridas
* tipos de datos

Características:

* no operan por fila
* no generan `invalid_rows`
* afectan el estado global del dataset

### 2. Row-level (semántica)

Validan valores dentro de las filas.

Ejemplos:

* rangos numéricos
* valores permitidos

Características:

* identifican filas inválidas
* permiten `drop` y `separate`
* habilitan estrategias `threshold`

---

## Sistema de tipos y conversiones

`DataTypeConverterFilter` soporta:

| Tipo              | Soporte                           |
| ----------------- | --------------------------------- |
| integers nullable | `Int8`, `Int16`, `Int32`, `Int64` |
| floats nullable   | `Float32`, `Float64`              |
| string            | `string`                          |
| boolean nullable  | `boolean`                         |
| datetime          | `datetime`                        |
| timedelta         | `timedelta` + `unit`              |

### Unidades soportadas para timedelta

| Unidad  | Alias |
| ------- | ----- |
| seconds | `s`   |
| minutes | `m`   |
| hours   | `h`   |
| days    | `d`   |

---

## Testing

Ejecutar tests:

```bash
# Instalar dependencias de testing
pip install pytest pytest-mock pytest-cov

# Ejecutar todos los tests
pytest tests/

# Ejecutar con cobertura
pytest tests/ --cov=src/data_pipeline --cov-report=html

# Ejecutar módulos específicos
pytest tests/validation/
pytest tests/filters/
pytest tests/sinks/

# Ejecutar con verbose
pytest tests/ -v

# Ejecutar test específico
pytest tests/validation/test_validation_result.py::TestValidationResult::test_creation_valid_result
```

### Cobertura actual

Incluye tests para:

* filtros
* sinks
* validation engine
* validation rules
* validation report
* validation result
* estrategias de fallo
* row actions
* persistencia de reportes

---

## Estado actual del sistema

### Estable

* pipeline core
* validation engine
* validation rules
* type conversion
* CSV source/sink
* filtros básicos
* Copy-on-Write global
* testing base

### Parcial

* cleaning avanzado
* métricas avanzadas de calidad
* agregaciones

### Pendiente

* enrichment
* aggregation real
* persistencia avanzada
* streaming real
* chunk processing real
* sinks adicionales

---

## Hoja de ruta

### Próximos módulos

* Feature Engineering
* Enrichment
* Aggregation
* Persistencia en Parquet
* Persistencia en bases de datos

### Validación avanzada

* integridad referencial
* reglas cross-column
* reglas dependientes
* reglas dinámicas

### Escalabilidad

* chunk processing real
* streaming pipeline
* procesamiento distribuido

---

## Notas de diseño importantes

* El primer componente NO es un filtro, es un `DataSource`
* El último componente puede ser un `DataSink`
* Todas las reglas devuelven `invalid_rows`, pero:

  * reglas estructurales → siempre `[]`
  * reglas row-level → índices inválidos
* `is_row_level` define cómo interpretar el resultado
* Los filtros trabajan sobre `pandas.DataFrame`
* El sistema es config-driven (YAML)
* Ownership semantics:

  * el DataFrame de entrada es caller-owned
  * los filters NO deben mutar el DataFrame recibido
  * toda operación de escritura debe trabajar sobre copias defensivas
  * `inplace=True` está prohibido arquitectónicamente
* Copy-on-Write se habilita globalmente desde:

```python
pd.options.mode.copy_on_write = True
```

* Los filtros que transforman datos deben trabajar sobre copias explícitas cuando exista mutación

---

## Filosofía del proyecto

Este proyecto busca evolucionar hacia:

* un framework de pipelines
* altamente configurable
* extensible
* con validación robusta
* desacoplado
* orientado a composición
* con separación clara de responsabilidades

---
