from typing import Any

from jsonschema import Draft202012Validator


def validate_arguments(arguments: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """
    Validates arguments against the given JSON Schema.
    Returns a list of validation error messages (empty if valid).
    """
    validator = Draft202012Validator(schema)
    errors = []
    for error in validator.iter_errors(arguments):
        errors.append(error.message)
    return errors
