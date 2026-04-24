import pytest
import pandas as pd
import tempfile
from pathlib import Path


@pytest.fixture
def sample_df():
    """DataFrame básico para tests."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "age": [25, 30, 35, 40, 45],
        "salary": [50000.0, 60000.0, 70000.0, 80000.0, 90000.0],
    })


@pytest.fixture
def sample_df_with_nulls():
    """DataFrame con valores nulos."""
    return pd.DataFrame({
        "id": [1, 2, None, 4, 5],
        "name": ["Alice", None, "Charlie", "David", None],
        "age": [25, 30, 35, None, 45],
        "salary": [50000.0, None, 70000.0, 80000.0, 90000.0],
    })


@pytest.fixture
def sample_df_with_duplicates():
    """DataFrame con filas duplicadas."""
    return pd.DataFrame({
        "id": [1, 1, 2, 2, 3],
        "name": ["Alice", "Alice", "Bob", "Bob", "Charlie"],
        "value": [100, 100, 200, 200, 300],
    })


@pytest.fixture
def sample_df_with_all_nulls_row():
    """DataFrame con una fila completamente nula."""
    return pd.DataFrame({
        "A": [1, None, 3],
        "B": [4, None, 6],
        "C": ["x", None, "z"],
    })


@pytest.fixture
def sample_df_numeric():
    """DataFrame con valores numéricos para tests de rango."""
    return pd.DataFrame({
        "product_id": [1, 2, 3, 4, 5],
        "price": [10.0, 20.0, 30.0, 40.0, 50.0],
        "quantity": [5, 10, 15, 20, 25],
        "discount": [0, 5, 10, 15, 20],
    })


@pytest.fixture
def sample_df_categories():
    """DataFrame con categorías para tests de valores permitidos."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "status": ["active", "inactive", "pending", "active", "inactive"],
        "region": ["US", "EU", "ASIA", "US", "EU"],
        "category": ["A", "B", "C", "A", "B"],
    })


@pytest.fixture
def temp_csv_file(tmp_path, sample_df):
    """Crea un archivo CSV temporal."""
    file_path = tmp_path / "data.csv"
    sample_df.to_csv(file_path, index=False)
    return file_path


@pytest.fixture
def mock_logger(mocker):
    """Mock para el logger."""
    return mocker.patch("data_pipeline.core.logger.get_logger")

