"""PostgreSQL registry backend using SQLAlchemy.

Requires the 'postgres' optional dependency group:
    pip install wsi-py-ai[postgres]
"""

from __future__ import annotations

from typing import Any

import structlog

from wsi_py_ai.backends.base import RegistryBackend

logger: structlog.stdlib.BoundLogger = structlog.get_logger("wsi_py_ai.backends.postgres")


class PostgresRegistryBackend(RegistryBackend):
    """PostgreSQL-based registry backend for production multi-user deployments.

    Uses SQLAlchemy Core for connection management and query building.

    Attributes:
        connection_url: PostgreSQL connection string.
    """

    def __init__(self, connection_url: str) -> None:
        """Initialize PostgreSQL registry.

        Args:
            connection_url: SQLAlchemy connection URL
                (e.g., postgresql://user:pass@host:5432/dbname).
        """
        from sqlalchemy import (
            Column,
            DateTime,
            MetaData,
            String,
            Table,
            Text,
            create_engine,
            func,
        )

        self._engine = create_engine(connection_url)
        self._metadata = MetaData()
        self._slides = Table(
            "slides",
            self._metadata,
            Column("slide_id", String(255), primary_key=True),
            Column("metadata_json", Text, nullable=False),
            Column("created_at", DateTime, server_default=func.now()),
            Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
        )
        self._metadata.create_all(self._engine)
        logger.info("postgres.initialized", url=connection_url.split("@")[-1])

    def register_slide(self, slide_id: str, metadata: dict[str, Any]) -> None:
        """Register a slide in PostgreSQL.

        Uses upsert semantics — updates if slide_id already exists.

        Args:
            slide_id: Unique slide identifier.
            metadata: Slide metadata to store as JSON.
        """
        import json

        from sqlalchemy.dialects.postgresql import insert

        stmt = insert(self._slides).values(
            slide_id=slide_id,
            metadata_json=json.dumps(metadata),
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["slide_id"],
            set_={"metadata_json": json.dumps(metadata)},
        )
        with self._engine.begin() as conn:
            conn.execute(stmt)
        logger.info("postgres.registered", slide_id=slide_id)

    def query(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        """Query slides from PostgreSQL by metadata filters.

        Uses PostgreSQL JSON operators to filter on metadata fields.

        Args:
            filters: Key-value pairs to match against stored metadata JSON.

        Returns:
            List of matching slide metadata dictionaries.
        """
        import json

        from sqlalchemy import select, text

        stmt = select(self._slides.c.slide_id, self._slides.c.metadata_json)

        for key, value in filters.items():
            stmt = stmt.where(
                text(f"metadata_json::jsonb @> :filter_{key}").bindparams(**{f"filter_{key}": json.dumps({key: value})})
            )

        with self._engine.connect() as conn:
            result = conn.execute(stmt)
            rows: list[dict[str, Any]] = []
            for row in result:
                meta: dict[str, Any] = json.loads(row.metadata_json)
                rows.append({"slide_id": row.slide_id, **meta})
            return rows

    def update(self, slide_id: str, fields: dict[str, Any]) -> None:
        """Update metadata fields for a slide.

        Merges new fields into existing metadata JSON using PostgreSQL jsonb_set.

        Args:
            slide_id: Slide to update.
            fields: Fields to merge into existing metadata.

        Raises:
            ValueError: If slide_id not found.
        """
        import json

        from sqlalchemy import select, update

        with self._engine.begin() as conn:
            stmt = select(self._slides.c.metadata_json).where(self._slides.c.slide_id == slide_id)
            row = conn.execute(stmt).fetchone()
            if row is None:
                msg = f"Slide {slide_id} not found in PostgreSQL"
                raise ValueError(msg)

            meta: dict[str, Any] = json.loads(row.metadata_json)
            meta.update(fields)

            upd = update(self._slides).where(self._slides.c.slide_id == slide_id).values(metadata_json=json.dumps(meta))
            conn.execute(upd)
        logger.info("postgres.updated", slide_id=slide_id, fields=list(fields.keys()))
