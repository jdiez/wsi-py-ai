"""Agno tool wrappers for WSI pipeline operations.

Tool functions require the 'agentic' optional dependency group:
    uv pip install wsi-py-ai[agentic]
"""

__all__ = [
    "dataloader_pretile",
    "dataloader_stream",
    "deid_batch",
    "deid_run",
    "ingest_batch",
    "ingest_file",
    "qa_assess",
    "qa_batch",
    "registry_query",
    "registry_register",
    "registry_version_create",
]


def __getattr__(name: str) -> object:
    """Lazy-load tool functions that depend on agno."""
    _tool_map = {
        "dataloader_pretile": "wsi_py_ai.tools.dataloader_tools",
        "dataloader_stream": "wsi_py_ai.tools.dataloader_tools",
        "deid_batch": "wsi_py_ai.tools.deid_tools",
        "deid_run": "wsi_py_ai.tools.deid_tools",
        "ingest_batch": "wsi_py_ai.tools.ingest_tools",
        "ingest_file": "wsi_py_ai.tools.ingest_tools",
        "qa_assess": "wsi_py_ai.tools.qa_tools",
        "qa_batch": "wsi_py_ai.tools.qa_tools",
        "registry_query": "wsi_py_ai.tools.registry_tools",
        "registry_register": "wsi_py_ai.tools.registry_tools",
        "registry_version_create": "wsi_py_ai.tools.registry_tools",
    }
    if name in _tool_map:
        import importlib

        module = importlib.import_module(_tool_map[name])
        return getattr(module, name)
    msg = f"module 'wsi_py_ai.tools' has no attribute {name!r}"
    raise AttributeError(msg)
