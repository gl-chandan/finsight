from dataclasses import dataclass


@dataclass
class DocumentChunk:

    text: str
    document_name: str
    page_number: int | None = None