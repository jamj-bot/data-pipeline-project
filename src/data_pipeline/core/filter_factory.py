from data_pipeline.filters.load_csv import LoadCSVFilter
from data_pipeline.filters.load_csv_chunks import ChunkedCSVFilter
from data_pipeline.filters.clean_data import CleanDataFilter
from data_pipeline.filters.deduplicate import DeduplicateFilter
from data_pipeline.filters.data_quality_metrics import DataQualityMetricsFilter
from data_pipeline.filters.data_type_converter import DataTypeConverterFilter
from data_pipeline.filters.validation import ValidationFilter
from data_pipeline.filters.filter_by_date import FilterByDateRange
from data_pipeline.filters.save_csv import SaveCSVFilter

from data_pipeline.core.filter import DataFilter
from data_pipeline.core.data_source import DataSource


FILTER_REGISTRY: dict[str, type] = {
    "LoadCSVFilter": LoadCSVFilter,
    "ChunkedCSVFilter": ChunkedCSVFilter,
    "CleanDataFilter": CleanDataFilter,
    "DeduplicateFilter": DeduplicateFilter,
    "DataQualityMetricsFilter": DataQualityMetricsFilter,
    "ValidationFilter": ValidationFilter,
    "DataTypeConverterFilter": DataTypeConverterFilter,
    "FilterByDateRange": FilterByDateRange,
    "SaveCSVFilter": SaveCSVFilter,
}

def create_component(name: str, params: dict | None = None):

    # Verifica que el filtro exista en el diccionario
    if name not in FILTER_REGISTRY:
        raise ValueError(f"Componente no registrado: {name}")

    # Recupera la clase correspondiente
    component_class = FILTER_REGISTRY[name]

    # Crea el objeto, en caso de requerirlo usa los **params
    return component_class(**(params or {}))
