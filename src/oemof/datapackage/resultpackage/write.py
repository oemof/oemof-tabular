import json
from pathlib import Path
from typing import Any, Dict, List
from zipfile import ZipFile, ZIP_DEFLATED
import tempfile

import pandas as pd


def _normalize_df_for_csv(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """
    - Setzt einen Indexnamen, falls keiner existiert (für sauberere CSVs).
    - Normalisiert 'variable_costs' auf einen MultiIndex (from, to),

      wenn die Spalten Tupel sind.
    """
    df = df.copy()

    if df.index.name is None:
        df.index.name = "index"

    if key == "variable_costs":
        # Bug-Workaround: Spalten als Tupel -> zu MultiIndex(from, to)
        if not isinstance(df.columns, pd.MultiIndex):
            if all(isinstance(c, tuple) and len(c) == 2 for c in df.columns):
                df.columns = pd.MultiIndex.from_tuples(
                    df.columns, names=["from", "to"]
                )

    return df


def _export_df_resource(
    df: pd.DataFrame,
    key: str,
    results_root: Path,
    resources: List[Dict[str, Any]],
) -> None:
    """
    Schreibt einen DataFrame als CSV nach
    - results/sequences/<key>.csv  (falls DatetimeIndex)
    - results/elements/<key>.csv   (sonst)

    und trägt die Ressource in 'resources' ein.
    """
    df = _normalize_df_for_csv(df, key)

    if isinstance(df.index, pd.DatetimeIndex):
        subdir = results_root / "sequences"
        kind = "sequence"
        rel_prefix = "results/sequences"
    else:
        subdir = results_root / "elements"
        kind = "element"
        rel_prefix = "results/elements"

    subdir.mkdir(parents=True, exist_ok=True)

    fname = f"{key}.csv"
    fpath = subdir / fname

    # MultiIndex-Spalten bleiben unverändert -> mehrere Headerzeilen im CSV
    df.to_csv(fpath)

    if isinstance(df.columns, pd.MultiIndex):
        header_rows = df.columns.nlevels
    else:
        header_rows = 1

    resources.append(
        {
            "name": key,
            "path": f"{rel_prefix}/{fname}",
            "kind": kind,
            "format": "csv",
            "header_rows": header_rows,
        }
    )


def _to_dataframe(value: Any) -> pd.DataFrame | None:
    """Versucht, einen Wert generisch in einen DataFrame zu wandeln."""
    if isinstance(value, pd.DataFrame):
        return value.copy()
    if isinstance(value, pd.Series):
        return value.to_frame()
    try:
        return pd.DataFrame(value)
    except Exception:
        return None


def _zip_dir(src_dir: Path, zip_path: Path) -> None:
    """Packt den Inhalt von src_dir als ZIP nach zip_path."""
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        for file_path in src_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(src_dir)
                zf.write(file_path, arcname)


def export_results_to_datapackage(
    results: Any, base_path: str | Path, zip: bool = False
) -> None:
    """
    Exportiert ein oemof.solph.Results-Objekt als datapackage-ähnliche Struktur.

    Variante ohne ZIP (zip=False, Standard)
    ---------------------------------------
    base_path/
    ├─ datapackage.json
    └─ results/
       ├─ elements/
       │  ├─ objective.csv
       │  └─ <key>.csv
       └─ sequences/
          └─ <key>.csv   (für Zeitreihen mit DatetimeIndex)

    Variante mit ZIP (zip=True)
    ---------------------------
    - base_path endet auf '.zip':
        * erzeugt eine temporäre Struktur und packt sie als ZIP nach base_path
        * das temporäre Verzeichnis wird danach gelöscht
    - base_path endet nicht auf '.zip':
        * erzeugt die Struktur unter base_path (Verzeichnis)
        * zusätzlich wird base_path.with_suffix('.zip') erzeugt

    Regeln für Inhalte
    ------------------
    - für jeden key in results.keys() wird genau eine CSV geschrieben
    - 'objective' wird als 1‑Wert‑CSV gespeichert und später wieder zu float
    - Daten mit DatetimeIndex → sequences, sonst → elements
    - falls keine DataFrame‑Konvertierung möglich ist → leere Datei in elements

    """
    base_path = Path(base_path)

    # Fall A: base_path ist eine .zip-Datei -> temporäres Verzeichnis nutzen
    if zip:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            _export_results_to_dir(results, tmp_root)
            _zip_dir(tmp_root, base_path)
    else:
        base_path.mkdir(parents=True, exist_ok=True)
        _export_results_to_dir(results, base_path)



def _export_results_to_dir(results: Any, base_path: Path) -> None:
    """Hilfsfunktion: schreibt die komplette Struktur in ein Verzeichnis."""
    results_root = base_path / "results"
    (results_root / "elements").mkdir(parents=True, exist_ok=True)
    (results_root / "sequences").mkdir(parents=True, exist_ok=True)

    resources: List[Dict[str, Any]] = []

    for key in results.keys():
        value = results[key]

        # Sonderfall: objective
        if key == "objective":
            try:
                val = float(value)
                df = pd.DataFrame({"objective": [val]})
            except Exception:
                # leere Datei + einfacher Resource-Eintrag
                fname = "objective.csv"
                fpath = results_root / "elements" / fname
                fpath.touch()
                resources.append(
                    {
                        "name": "objective",
                        "path": "results/elements/objective.csv",
                        "kind": "element",
                        "format": "csv",
                        "header_rows": 1,
                    }
                )
                continue

            # bewusst über _export_df_resource, damit Schema einheitlich ist
            _export_df_resource(df, "objective", results_root, resources)
            continue

        # Normalfall: alles andere möglichst als DataFrame speichern
        df = _to_dataframe(value)

        if df is None:
            # keine sinnvolle Konvertierung möglich → leere Datei in elements
            fname = f"{key}.csv"
            fpath = results_root / "elements" / fname
            fpath.touch()
            resources.append(
                {
                    "name": key,
                    "path": f"results/elements/{fname}",
                    "kind": "element",
                    "format": "csv",
                    "header_rows": 0,
                }
            )
            continue

        _export_df_resource(df, key, results_root, resources)

    # datapackage.json schreiben
    datapackage = {
        "name": "oemof_solph_results",
        "profile": "tabular-data-package",
        "resources": resources,
    }

    with open(base_path / "datapackage.json", "w", encoding="utf-8") as f:
        json.dump(datapackage, f, indent=2)
