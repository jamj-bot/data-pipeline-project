from data_pipeline.core.pipeline import DataPipeline
from data_pipeline.core.filter_factory import create_filter
from data_pipeline.utils.config_loader import load_config

def main() -> None:
    # Recupera la configuración desde el archivo YAML
    config = load_config("config/pipeline.yaml")

    # Usar create_filter de factory_filter para crear un diccionario de filtros
        # P. ej. LoadCSVFilter(filepath="data.csv")
    filters = [
        create_filter(
            item["name"],
            item.get("params")
        )
        for item in config["pipeline"]["filters"]
    ]

    # Pasa el diccionarios de filtros al pipeline
    pipeline = DataPipeline(filters)

    result = pipeline.run()

    print(result.head(10))

if __name__ == "__main__":
    main()

