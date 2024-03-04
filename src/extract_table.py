import os
import mlflow

from src.ca_extract.extraction.table_transformer.detector import (
    TableTransformerDetector,
)
from src.ca_extract.extraction.table_transformer.extractor import (
    TableTransformerExtractor,
)
from src.ca_extract.page_selection.page_selector import PageSelector


def get_detector() -> TableTransformerDetector:
    """
    Load table detector model.

    Returns:
        TableTransformerDetector: detector.
    """
    detector = TableTransformerDetector(
        padding_factor=1.02,
        crop_padding_factor=1.02,
    )
    print("TableTransformerDetector loaded.")
    return detector


def get_extractor() -> TableTransformerExtractor:
    """
    Load table extractor model.

    Returns:
        TableTransformerExtractor: detector.
    """
    extractor = TableTransformerExtractor()
    print("TableTransformerExtractor loaded.")
    return extractor


def get_page_selector() -> PageSelector:
    """
    Load page selector.

    Returns:
    """
    model_name = "page_selection"
    stage = "Staging"
    clf = mlflow.pyfunc.load_model(f"models:/{model_name}/{stage}")
    page_selector = PageSelector(clf=clf)
    print("Page selector loaded.")
    return page_selector
