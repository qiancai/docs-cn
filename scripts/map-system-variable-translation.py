#!/usr/bin/env python3
"""
Replace English ### sections in system-variables_v2.md with their Chinese
translations from system-variables.md.

Rules:
  - Replacement unit is a ### section (from one ### heading to the next).
  - Sections are matched by variable name (ignoring <span> content and backticks).
  - A v2 section is kept in English (skipped) if it contains any of:
      "TiDB Cloud", "TiDB Self-Managed", or "CustomContent".
  - Sections in v2 with no matching Chinese section are also kept as-is.
  - Everything before the first ### heading (preamble) is kept from v2 as-is.
"""

import re
import sys
from pathlib import Path

SKIP_KEYWORDS = ["TiDB Cloud", "TiDB Self-Managed", "CustomContent"]

REPO_ROOT = Path(__file__).resolve().parent.parent
V2_PATH = REPO_ROOT / "system-variables_v2.md"
ZH_PATH = REPO_ROOT / "system-variables.md"

SECTION_RE = re.compile(r"^### ", re.MULTILINE)


def extract_var_name(heading_line: str) -> str:
    """Extract the bare variable name from a ### heading line."""
    text = heading_line.lstrip("#").strip()
    text = text.strip("`")
    text = re.split(r"\s*<", text, maxsplit=1)[0]
    return text.strip().strip("`")


def split_sections(content: str) -> tuple[str, list[tuple[str, str]]]:
    """Split markdown into (preamble, [(var_name, section_text), ...])."""
    positions = [m.start() for m in SECTION_RE.finditer(content)]

    if not positions:
        return content, []

    preamble = content[: positions[0]]
    sections = []
    for i, start in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(content)
        section_text = content[start:end]
        heading_line = section_text.split("\n", 1)[0]
        var_name = extract_var_name(heading_line)
        sections.append((var_name, section_text))

    return preamble, sections


def should_skip(section_text: str) -> bool:
    """Return True if this section must stay in English."""
    return any(kw in section_text for kw in SKIP_KEYWORDS)


def main() -> None:
    v2_content = V2_PATH.read_text(encoding="utf-8")
    zh_content = ZH_PATH.read_text(encoding="utf-8")

    v2_preamble, v2_sections = split_sections(v2_content)
    _, zh_sections = split_sections(zh_content)

    zh_map: dict[str, str] = {name: text for name, text in zh_sections}

    replaced = 0
    skipped_cloud = 0
    kept_en = 0

    result_parts = [v2_preamble]
    for var_name, section_text in v2_sections:
        if should_skip(section_text):
            result_parts.append(section_text)
            skipped_cloud += 1
        elif var_name in zh_map:
            result_parts.append(zh_map[var_name])
            replaced += 1
        else:
            result_parts.append(section_text)
            kept_en += 1

    output = "".join(result_parts)
    V2_PATH.write_text(output, encoding="utf-8")

    print(f"Done. Replaced: {replaced}, Skipped (Cloud/CustomContent): {skipped_cloud}, "
          f"Kept EN (no zh match): {kept_en}, Total sections: {len(v2_sections)}")


if __name__ == "__main__":
    main()
