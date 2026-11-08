# Cada función test_ comprueba un resultado que ya sabemos de antemano
import pytest


from calculos import con_iva, leer_ventas, total, total_por_producto, validar_venta


VENTAS = [
    {"fecha": "2026-10-01", "producto": "cafe", "precio": 1.50},
    {"fecha": "2026-10-01", "producto": "te", "precio": 1.20},
    {"fecha": "2026-10-02", "producto": "cafe", "precio": 1.50},
]


def test_total():
    assert total(VENTAS) == 4.20


def test_total_sin_ventas():
    assert total([]) == 0


def test_total_por_producto():
    assert total_por_producto(VENTAS) == {"cafe": 3.00, "te": 1.20}


# Un mismo test con varios casos: precio de entrada y resultado esperado
@pytest.mark.parametrize("precio, esperado", [(1.00, 1.21), (2.00, 2.42), (0.90, 1.09)])
def test_con_iva(precio, esperado):
    assert con_iva(precio) == esperado


# Filas que tienen que dar error: (fecha, precio)
@pytest.mark.parametrize(
    "fecha, precio",
    [
        ("2026-13-01", "1.50"),  # mes 13
        ("2026-10-01", "-1.50"),  # precio negativo
        ("2026-10-01", "otro"),  # no es un número
    ],
)
def test_validar_venta_rechaza_filas_malas(fecha, precio):
    fila = {"fecha": fecha, "producto": "cafe", "precio": precio}
    with pytest.raises(ValueError):
        validar_venta(fila)


def test_leer_ventas(tmp_path):
    # tmp_path es una carpeta temporal que pytest crea y borra solo
    ruta = tmp_path / "ventas.csv"
    ruta.write_text("fecha,producto,precio\n2026-10-01,cafe,1.50\n2026-10-02,te,1.20\n")
    ventas = leer_ventas(ruta)
    assert len(ventas) == 2
    assert ventas[0]["precio"] == 1.50


def test_leer_ventas_rechaza_columnas_malas(tmp_path):
    ruta = tmp_path / "ventas.csv"
    ruta.write_text("fecha,producto,importe\n2026-10-01,cafe,1.50\n")
    with pytest.raises(ValueError):
        leer_ventas(ruta)


def test_ventas_csv_del_repositorio_es_valido():
    # Calidad de datos: el ventas.csv del repositorio se lee sin errores
    ventas = leer_ventas("ventas.csv")
    assert len(ventas) > 0
