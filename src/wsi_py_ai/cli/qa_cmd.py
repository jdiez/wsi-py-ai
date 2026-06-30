"""CLI commands for quality assurance."""

import typer

qa_app = typer.Typer(help="Quality assurance")


@qa_app.command("run")
def qa_run(
    slide_id: str = typer.Argument(..., help="Slide ID to assess"),
) -> None:
    """QA a single slide."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig
    from wsi_py_ai.qa.runner import QARunner

    config = WSIPipelineConfig()
    backends = get_backends(config)
    qa = QARunner(backends=backends)
    report = qa.assess(slide_id)
    status = "PASSED" if report.passed else "FAILED"
    typer.echo(f"QA {status}: focus={report.focus_score:.2f} coverage={report.tissue_coverage:.2f}")


@qa_app.command("batch")
def qa_batch(
    study: str = typer.Option(..., "--study", help="Study identifier"),
    parallel: int = typer.Option(4, "--parallel", help="Number of parallel workers"),
) -> None:
    """Batch QA for a study."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig
    from wsi_py_ai.qa.runner import QARunner

    config = WSIPipelineConfig()
    backends = get_backends(config)
    qa = QARunner(backends=backends)
    results = qa.batch_assess(study, parallel)
    passed = sum(1 for r in results if r.passed)
    typer.echo(f"QA complete: {passed}/{len(results)} passed")


@qa_app.command("report")
def qa_report(
    study: str = typer.Option(..., "--study", help="Study identifier"),
    output_format: str = typer.Option("table", "--format", help="Output format"),
) -> None:
    """Show QA results for a study."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig

    config = WSIPipelineConfig()
    backends = get_backends(config)
    registry = backends["registry"]
    slides = registry.query({"study_id": study})
    typer.echo(f"QA Report for {study} ({len(slides)} slides, format={output_format})")
