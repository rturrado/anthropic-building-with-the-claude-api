import base64
import mimetypes
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

_MIME_MAP = {
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".md": "text/plain",
    ".py": "text/plain",
    ".js": "text/plain",
    ".html": "text/plain",
    ".css": "text/plain",
    ".csv": "text/csv",
    ".json": "application/json",
    ".xml": "application/xml",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def _guess_mime(path):
    ext = Path(path).suffix.lower()
    mime = _MIME_MAP.get(ext) or mimetypes.guess_type(str(path))[0]
    if not mime:
        raise ValueError(f"Unknown MIME type for extension: {ext}")
    return mime


def attach_file(path, media_type=None, citations=False, title=None):
    """Return a content block for a user message with the file base64-encoded inline."""
    media_type = media_type or _guess_mime(path)
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    if media_type.startswith("image/"):
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": data},
        }
    block = {
        "type": "document",
        "source": {"type": "base64", "media_type": media_type, "data": data},
    }
    if title:
        block["title"] = title
    if citations:
        block["citations"] = {"enabled": True}
    return block


def upload_file(path):
    """Upload a local file to Anthropic's Files API and return the file metadata."""
    path = Path(path)
    mime = _guess_mime(path)
    with open(path, "rb") as f:
        return client.beta.files.upload(file=(path.name, f, mime))


def list_files():
    return client.beta.files.list()


def get_file_metadata(file_id):
    return client.beta.files.retrieve_metadata(file_id)


def download_file(file_id, filename=None):
    content = client.beta.files.download(file_id)
    if not filename:
        filename = get_file_metadata(file_id).filename
    content.write_to_file(filename)
    return filename


def delete_file(file_id):
    return client.beta.files.delete(file_id)
