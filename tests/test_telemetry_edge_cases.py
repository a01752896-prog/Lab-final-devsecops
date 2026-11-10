"""Pruebas adicionales de casos borde para REQ-SEC-01.

No sustituyen ni modifican las pruebas originales (tests/test_telemetry.py);
amplían la cobertura del requisito: solo la operación exacta "read" se autoriza
y cualquier otra entrada se rechaza por defecto (lista blanca estricta).
"""
import pytest

from src.telemetry import get_telemetry, is_operation_allowed

# Entradas que NO deben autorizarse: variantes de write, otras operaciones de
# control, variantes de "read" con mayúsculas/espacios y valores no textuales.
DENIED_OPERATIONS = [
    "WRITE", "Write", " write", "write ",
    "delete", "update", "set", "admin", "*",
    "READ", "Read", " read", "read ", "read\n",
    "read,write", "readwrite",
    None, 1, True,
]


@pytest.mark.parametrize("operation", DENIED_OPERATIONS)
def test_non_read_operations_are_denied(operation):
    assert is_operation_allowed(operation) is False


@pytest.mark.parametrize("operation", DENIED_OPERATIONS)
def test_denied_response_does_not_leak_values(operation):
    result = get_telemetry(operation, "temperature")
    assert result["status"] == "denied"
    assert "value" not in result


def test_read_pressure_is_allowed():
    assert get_telemetry("read", "pressure") == {
        "status": "ok", "measurement": "pressure", "value": 1.2
    }


def test_default_measurement_is_temperature():
    assert get_telemetry("read")["measurement"] == "temperature"
