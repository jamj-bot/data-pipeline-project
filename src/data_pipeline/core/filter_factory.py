from data_pipeline.filters.load_csv import LoadCSVFilter
from data_pipeline.filters.load_csv_chunks import ChunkedCSVFilter
from data_pipeline.filters.clean_data import CleanDataFilter
from data_pipeline.filters.deduplicate import DeduplicateFilter
from data_pipeline.filters.data_quality_metrics import DataQualityMetricsFilter
from data_pipeline.filters.data_type_converter import DataTypeConverterFilter
from data_pipeline.filters.schema_validation import SchemaValidationFilter
from data_pipeline.filters.business_validation import BusinessValidationFilter
from data_pipeline.filters.filter_by_date import FilterByDateRange
from data_pipeline.filters.save_csv import SaveCSVFilter
from data_pipeline.core.filter import DataFilter

""" Diccionario que mapea nombres (strings) a clases  """
FILTER_REGISTRY: dict[str, type[DataFilter]] = {
    "LoadCSVFilter": LoadCSVFilter,
    "ChunkedCSVFilter": ChunkedCSVFilter,
    "CleanDataFilter": CleanDataFilter,
    "DeduplicateFilter": DeduplicateFilter,
    "DataQualityMetricsFilter": DataQualityMetricsFilter,
    "SchemaValidationFilter": SchemaValidationFilter,
    "BusinessValidationFilter": BusinessValidationFilter,
    "DataTypeConverterFilter": DataTypeConverterFilter,
    "FilterByDateRange": FilterByDateRange,
    "SaveCSVFilter": SaveCSVFilter,
}


def create_filter(name: str, params: dict | None = None) -> DataFilter:

    # Verifica que el filtro exista en el diccionario
    if name not in FILTER_REGISTRY:
        raise ValueError(f"Filtro no registrado: {name}")

    # Recupera la clase correspondiente, p. ej. LoadCSVFilter
    filter_class = FILTER_REGISTRY[name]

    # Crea el objeto, en caso de requerirlo usa los **params
        # P. ej. LoadCSVFilter(filepath="data.csv")
    return filter_class(**(params or {}))
