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
- [Estado actual del sistema](#estado-actual-del-sistema)
- [Hoja de ruta](#hoja-de-ruta)
- [Testing](#testing)

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
   - reglas estructurales
   - reglas de negocio

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

| Tipo            | Ejemplo              | Row-level |
|-----------------|---------------------|----------|
| estructural     | required_columns    | No        |
| semántica       | value_range         | Si        |

### Capacidades

- errores vs warnings
- invalid_rows tracking
- fail strategies:
  - `pre`
  - `post`
  - `threshold`

---

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
- No todos los rules soportan `invalid_rows` (por diseño)
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
