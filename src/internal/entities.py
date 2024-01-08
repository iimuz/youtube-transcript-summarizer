"""Entityをまとめておくモジュール."""
from pydantic import BaseModel, RootModel


class Transcript(BaseModel):
    """Transcript."""

    text: str
    start: float
    duration: float


class Transcripts(RootModel[list[Transcript]]):
    """Transcriptの集合."""
