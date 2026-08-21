#!/usr/bin/env python3
"""Validate translated locale files against the English source strings."""

import argparse
import json
import re
import sys
from pathlib import Path


PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")


def load_locale_file(path):
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except OSError as error:
        return None, f"unable to read file: {error}"
    except json.JSONDecodeError as error:
        return None, f"malformed JSON at line {error.lineno}, column {error.colno}: {error.msg}"

    if not isinstance(data, dict):
        return None, "top-level JSON value must be an object"

    return data, None


def extract_placeholders(value):
    if not isinstance(value, str):
        return set()
    return set(PLACEHOLDER_PATTERN.findall(value))


def format_placeholders(placeholders):
    if not placeholders:
        return "none"
    return ", ".join(f"{{{name}}}" for name in sorted(placeholders))


def validate_locale(source_strings, locale_path):
    locale_strings, error = load_locale_file(locale_path)
    if error:
        return [f"File error: {error}"]

    issues = []
    source_keys = set(source_strings)
    locale_keys = set(locale_strings)

    for key in sorted(source_keys - locale_keys):
        issues.append(f"Missing key: {key}")

    for key in sorted(locale_keys - source_keys):
        issues.append(f"Extra key: {key}")

    for key in sorted(source_keys & locale_keys):
        translated_value = locale_strings[key]
        if translated_value == "":
            issues.append(f"Empty value: {key}")

        expected = extract_placeholders(source_strings[key])
        actual = extract_placeholders(translated_value)
        if expected != actual:
            issues.append(
                f"Placeholder mismatch: {key} "
                f"(expected {format_placeholders(expected)}, found {format_placeholders(actual)})"
            )

    return issues


def check_locales(locales_dir):
    source_path = locales_dir / "en.json"
    source_strings, error = load_locale_file(source_path)
    if error:
        print(f"Cannot validate locales: {source_path} is invalid ({error})", file=sys.stderr)
        return 1

    locale_paths = sorted(path for path in locales_dir.glob("*.json") if path.name != "en.json")
    if not locale_paths:
        print(f"No locale files found in {locales_dir}", file=sys.stderr)
        return 1

    total_issues = 0

    for locale_path in locale_paths:
        issues = validate_locale(source_strings, locale_path)
        total_issues += len(issues)

        print(f"\n{locale_path.name}")
        print("-" * len(locale_path.name))
        if issues:
            for issue in issues:
                print(f"- {issue}")
        else:
            print("OK")

    print(f"\nTotal issues: {total_issues}")
    return 0 if total_issues == 0 else 1


def parse_args():
    parser = argparse.ArgumentParser(description="Validate locale JSON files against en.json.")
    parser.add_argument(
        "--locales-dir",
        type=Path,
        default=Path("locales"),
        help="Directory containing en.json and translated locale JSON files.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    return check_locales(args.locales_dir)


if __name__ == "__main__":
    sys.exit(main())
