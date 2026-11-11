# Laboratorio final individual — ¿Autorizarías este cambio a producción?

Proyecto educativo de un servicio de telemetría IT–OT **simulado**. Contiene dos problemas intencionales: una regresión de autorización y una dependencia con vulnerabilidades conocidas. No se conecta a PLC ni a sistemas industriales.

## Preparación

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Diagnóstico inicial
```bash
python -m pytest -q
python -m bandit -r src -q
python -m pip_audit -r requirements-audit.txt
```

**Esperado inicialmente:** 7 pruebas ejecutadas, 2 fallidas; Bandit sin hallazgos sobre `src` (esto NO significa que la autorización sea correcta); `pip-audit` con hallazgos conocidos en la dependencia auditada. El servicio no necesita instalar la biblioteca vulnerable para este ejercicio.

## Tu reto
1. Identifica el requisito que incumple la prueba fallida y corrige el código de producción, **sin cambiar las pruebas**.
2. Analiza `requirements-audit.txt`. Investiga una versión corregida y compatible, actualiza ese archivo y vuelve a auditar. Si el servicio de auditoría no está disponible, documenta el error de infraestructura y no lo confundas con ausencia de vulnerabilidades.
3. Ejecuta nuevamente las tres verificaciones.
4. Crea un repositorio GitHub individual y sube tu proyecto. El workflow está en `.github/workflows/security-ci.yml`.
5. Comprueba la ejecución de GitHub Actions; no modifiques el workflow para ocultar fallas.
6. Explica tu decisión de integración, distinguiéndola de una autorización para desplegar en OT.

## Evidencias
- Captura inicial de pytest (falla), captura inicial de pip-audit (hallazgos).
- Captura posterior de pytest (aprobado), captura posterior de pip-audit (resultado).
- Enlace al repositorio y captura de GitHub Actions posterior a la corrección.
- Respuestas y decisión técnica según las instrucciones de Canvas.

## Importante
`requirements.txt` contiene solo herramientas del laboratorio; `requirements-audit.txt` representa un manifiesto de una dependencia de un componente hipotético y se **audita, pero no se instala**. No afirmes que el SBOM completo del producto está representado por este archivo. `pip-audit` requiere conectividad a su servicio de vulnerabilidades y su resultado puede cambiar conforme se actualizan los avisos.

---

## Entrega — Rodrigo Adahir Hernández Escamilla (A01752896)

### Cambios realizados
| Commit | Cambio | GitHub Actions |
|---|---|---|
| `695b69a` | Proyecto base sin modificar (regresión + dependencia vulnerable) | Run #1 ❌ falla (pytest 2 fallidas, pip-audit 37 vulnerabilidades) |
| `2f3d585` | `src/telemetry.py`: lista blanca estricta (`operation == ALLOWED_OPERATION`); `requirements-audit.txt`: `requests` 2.19.1 → 2.34.2 | Run #2 ✅ pasa |
| `c9b1aa0` | Nuevo `tests/test_telemetry_edge_cases.py` (40 casos borde); las pruebas originales no se modificaron | Run #3 ✅ pasa |

El workflow `.github/workflows/security-ci.yml` **no se modificó**.

### Resultados
| Verificación | Antes | Después |
|---|---|---|
| pytest | 5 de 7 (2 fallidas: `test_write_is_denied`, `test_write_cannot_read_or_modify_telemetry`) | 7 de 7 · 47 de 47 con casos borde · cobertura 100 % de `src/` |
| Bandit | 0 hallazgos (no detecta la regresión de lógica) | 0 hallazgos |
| pip-audit `requirements-audit.txt` | 37 filas / 19 avisos únicos en requests, urllib3, idna | No known vulnerabilities found |
| pip-audit `requirements.txt` | — | No known vulnerabilities found |

**Decisión:** se autoriza la **integración** al repositorio principal, no el **despliegue** en un entorno OT real (faltan autenticación, controles de solo lectura en PLC/red, monitoreo y revisión de código obligatoria).

### Evidencia (`evidencia/`)
| Archivo | Contenido |
|---|---|
| `A_pytest_inicial.txt` | Evidencia A: pytest inicial |
| `bandit_inicial.txt` · `bandit_final.txt` | Bandit antes y después |
| `B_audit_inicial.txt` | Evidencia B: pip-audit inicial |
| `diff_correccion.txt` | Diff de la corrección |
| `C_pytest_final.txt` | Evidencia C: pytest después de corregir |
| `D_audit_final.txt` · `H_audit_herramientas.txt` | Evidencia D: pip-audit de ambos manifiestos |
| `F_pytest_extendido.txt` · `G_cobertura.txt` | 47 pruebas y cobertura |
| `F0_pytest_extendido_original.txt` | Pruebas extendidas contra el código original |
| `actions/E*_*.log` | Evidencia E: logs completos de los runs #1, #2 y #3 |
| `capturas/` | Capturas de GitHub Actions y gráficas |
