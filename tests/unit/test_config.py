from rag_myflow.config import AppConfig, OcrPolicy


def test_default_workspace_and_ocr_policy() -> None:
    config = AppConfig()

    assert config.workspace_slug == "local"
    assert config.workspace_name == "My Workspace"
    assert config.ocr_policy is OcrPolicy.REJECT
