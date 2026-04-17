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

- **Schema Validation**
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
data-pipeline-project/
├── config/
│   └── pipeline.yaml
├── scripts/
│   └── run_pipeline.py
├── src/data_pipeline/
│   ├── core/
│   │   ├── data_source.py
│   │   ├── filter.py
│   │   ├── filter_factory.py
│   │   ├── logger.py
│   │   └── pipeline.py
│   ├── filters/
│   ├── validation/
│   │   ├── engine/
│   │   ├── rules/
│   │   │   ├── schema/
│   │   │   └── business/
│   │   ├── result.py
│   │   └── validation_report.py
│   └── utils/
│       └── config_loader.py
├── tests/
├── requirements.txt
└── README.md
```

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

    - name: SchemaValidationFilter
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
pytest tests/
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
