"""Transcriptを取得するController."""
import urllib.parse
from enum import Enum
from typing import Self

from youtube_transcript_api import YouTubeTranscriptApi

from .entities import Transcript, Transcripts


class YouTubeLanguage(Enum):
    """ダウンロードする言語."""

    JA = "ja"  # 日本語
    EN = "en"  # 英語


class YouTubeTranscript:
    """YouTubeからTranscriptを取得するController."""

    def __init__(self: Self, video_url: str, language: YouTubeLanguage) -> None:
        """YouTubeTranscriptオブジェクトを初期化する.

        Parameters
        ----------
        video_url : str
            YouTubeのURL.
            e.g. <https://www.youtube.com/watch?v=XXXXXXXXXXX>
        language : YouTubeLanguage
            YouTubeから取得するTranscriptの言語.
        """
        self._video_url = video_url
        self._language = language

        self._video_id: str | None = None

    def get_transcript(self: Self) -> Transcripts:
        """YouTubeからTranscriptを取得する."""
        response = YouTubeTranscriptApi.get_transcript(
            video_id=self.video_id, languages=[self._language.value]
        )

        return Transcripts(
            root=[
                Transcript(
                    text=item["text"], start=item["start"], duration=item["duration"]
                )
                for item in response
            ]
        )

    @property
    def video_id(self: Self) -> str:
        """URLから抽出した動画IDを返す."""
        if self._video_id is not None:
            return self._video_id

        parsed_url = urllib.parse.urlparse(self._video_url)
        query = urllib.parse.parse_qs(parsed_url.query)
        video_ids = query.get("v", [])
        if len(video_ids) != 1:
            message = "Invalid video URL"
            raise ValueError(message)
        self._video_id = video_ids[0]

        return self._video_id
