"""CLI commands for end-to-end pipeline execution."""

import typer

pipeline_app = typer.Typer(help="End-to-end pipeline")


@pipeline_app.command("run")
def pipeline_run(
    source_dir: str = typer.Argument(..., help="Source directory with WSI files"),
    study: str = typer.Option(..., "--study", help="Study identifier"),
    parallel: int = typer.Option(4, "--parallel", help="Number of parallel workers"),
) -> None:
    """Run full pipeline: ingest → deid → QA → register."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig
    from wsi_py_ai.deid.deidentifier import WSIDeidentifier
    from wsi_py_ai.ingest.ingester import WSIIngester
    from wsi_py_ai.qa.runner import QARunner

    config = WSIPipelineConfig()
    backends = get_backends(config)

    typer.echo(f"Pipeline started for {source_dir} → study {study}")

    ingester = WSIIngester(backends=backends)
    ingest_results = ingester.batch_ingest(source_dir, study, parallelism=parallel)
    typer.echo(f"  Ingested: {len(ingest_results)} slides")

    deid = WSIDeidentifier(backends=backends, salt=config.deid_salt)
    deid_results = deid.batch_deidentify(study)
    typer.echo(f"  De-identified: {len(deid_results)} slides")

    qa = QARunner(backends=backends)
    qa_results = qa.batch_assess(study)
    passed = sum(1 for r in qa_results if r.passed)
    typer.echo(f"  QA: {passed}/{len(qa_results)} passed")

    typer.echo("Pipeline complete.")


@pipeline_app.command("status")
def pipeline_status(
    study: str = typer.Option(..., "--study", help="Study identifier"),
) -> None:
    """Show pipeline status for a study."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig

    config = WSIPipelineConfig()
    backends = get_backends(config)
    slides = backends["registry"].query({"study_id": study})
    typer.echo(f"Study: {study}")
    typer.echo(f"  Total slides: {len(slides)}")
    deid_count = sum(1 for s in slides if s.get("deidentified"))
    qa_count = sum(1 for s in slides if s.get("qa_passed"))
    typer.echo(f"  De-identified: {deid_count}")
    typer.echo(f"  QA passed: {qa_count}")
