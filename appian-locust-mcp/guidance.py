"""Loads and searches the Appian Locust steering document."""

from pathlib import Path
from typing import List

STEERING_PATH = Path.home() / ".kiro" / "steering" / "appian-locust-steering.md"


def load_steering() -> str:
    if STEERING_PATH.exists():
        return STEERING_PATH.read_text()
    return (
        f"Steering document not found at {STEERING_PATH}\n"
        "Copy it there: cp appian-locust-steering.md ~/.kiro/steering/\n"
    )


def search_steering(topic: str) -> str:
    content = load_steering()
    if not topic:
        return content

    lines = content.split("\n")
    sections: List[str] = []
    current: List[str] = []
    matched = False

    for line in lines:
        if line.startswith("#"):
            if matched and current:
                sections.append("\n".join(current))
            matched = any(kw in line.lower() for kw in topic.lower().split())
            current = [line] if matched else []
        elif matched:
            current.append(line)

    if matched and current:
        sections.append("\n".join(current))

    if sections:
        return "\n\n---\n\n".join(sections)

    # Fallback: grep-style context search
    matches = []
    for i, line in enumerate(lines):
        if topic.lower() in line.lower():
            start = max(0, i - 5)
            end = min(len(lines), i + 6)
            matches.append("\n".join(lines[start:end]))
    return "\n\n---\n\n".join(matches[:5]) if matches else content[:2000]
