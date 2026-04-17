from data_pipeline.core.pipeline import DataPipeline
from data_pipeline.core.filter_factory import create_component
from data_pipeline.utils.config_loader import load_config
from data_pipeline.core.data_source import DataSource
from data_pipeline.core.filter import DataFilter


def main() -> None:
    config = load_config("config/pipeline.yaml")

    components = [
        create_component(item["name"], item.get("params"))
        for item in config["pipeline"]["filters"]
    ]

    source = None
    filters: list[DataFilter] = []

    for comp in components:
        if isinstance(comp, DataSource):
            if source is not None:
                raise ValueError("Solo se permite una fuente de datos")
            source = comp
        else:
            filters.append(comp)

    if source is None:
        raise ValueError("La pipeline requiere una fuente de datos")

    pipeline = DataPipeline(source, filters)

    result = pipeline.run()

    print(result.head(10))


if __name__ == "__main__":
    main()

