from decider.argument_validator import validate_arguments


def test_valid_arguments():
    schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        "required": ["name"],
    }
    args = {"name": "Alice", "age": 30}
    errors = validate_arguments(args, schema)
    assert len(errors) == 0


def test_missing_required():
    schema = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
    args = {}
    errors = validate_arguments(args, schema)
    assert len(errors) > 0
    assert "name" in errors[0] or "required" in errors[0]


def test_wrong_type():
    schema = {"type": "object", "properties": {"age": {"type": "integer"}}}
    args = {"age": "thirty"}
    errors = validate_arguments(args, schema)
    assert len(errors) > 0
    assert "type" in errors[0].lower() or "integer" in errors[0].lower()


def test_additional_properties():
    schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "additionalProperties": False,
    }
    args = {"name": "Bob", "age": 40}
    errors = validate_arguments(args, schema)
    assert len(errors) > 0


def test_empty_schema():
    schema = {}
    args = {"anything": "goes"}
    errors = validate_arguments(args, schema)
    assert len(errors) == 0


def test_empty_arguments_with_required():
    schema = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
    errors = validate_arguments({}, schema)
    assert len(errors) > 0
