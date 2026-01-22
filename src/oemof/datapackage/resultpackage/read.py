import json
from pathlib import Path
from typing import Any, Dict
from zipfile import ZipFile
import tempfile

import pandas as pd


class ImportResults:
    """
    Leichtgewichtige, importierte Variante von Results.

    - Lädt alle Resources aus datapackage.json
    - 'objective' → float
    - alle anderen → pandas.DataFrame (ggf. leer)
    - MultiIndex-Spalten werden anhand von 'header_rows' korrekt rekonstruiert
    - API:
      * keys()
      * '__getitem__' (z.B. r['flow'])
      * timeindex (erste gefundene DatetimeIndex-Zeitachse)

    """

    def __init__(self, base_path: str | Path):
        self.base_path = Path(base_path)
        self._data: Dict[str, Any] = {}
        self._timeindex: pd.Index | None = None

        self._load()

    def _load(self) -> None:
        dp_path = self.base_path / "datapackage.json"
        if not dp_path.exists():
            raise FileNotFoundError(f"{dp_path} nicht gefunden.")

        with open(dp_path, "r", encoding="utf-8") as f:
            pkg = json.load(f)

        for res in pkg.get("resources", []):
            key = res["name"]
            rel_path = res["path"]
            kind = res.get("kind", "element")  # 'sequence' oder 'element'
            header_rows = int(res.get("header_rows", 1))

            fpath = self.base_path / rel_path

            if not fpath.exists() or fpath.stat().st_size == 0:
                if key == "objective":
                    self._data[key] = None
                else:
                    self._data[key] = pd.DataFrame()
                continue

            # Sonderfall: objective
            if key == "objective":
                df = pd.read_csv(fpath)
                if df.empty:
                    self._data["objective"] = None
                else:
                    val = df.iloc[0, 0]
                    try:
                        self._data["objective"] = float(val)
                    except Exception:
                        self._data["objective"] = None
                continue

            # alle anderen Keys → DataFrame
            # header_rows gibt an, wie viele Kopfzeilen für die Spalten existieren
            if header_rows >= 2:
                header = list(range(header_rows))
            else:
                header = 0

            # sequences: Index als Datum parsen
            if kind == "sequence":
                df = pd.read_csv(
                    fpath, header=header, index_col=0, parse_dates=[0]
                )
            else:
                df = pd.read_csv(
                    fpath, header=header, index_col=0
                )

            self._data[key] = df

        # timeindex: nimm den Index des ersten DataFrames mit DatetimeIndex
        for v in self._data.values():
            if isinstance(v, pd.DataFrame) and isinstance(
                v.index, pd.DatetimeIndex
            ):
                self._timeindex = v.index
                break

    # API ähnlich Results

    def keys(self):
        return set(self._data.keys())

    def __contains__(self, key) -> bool:
        return key in self._data

    def __getitem__(self, key: str):
        if key not in self._data:
            raise KeyError(f"Key '{key}' nicht vorhanden.")
        return self._data[key]

    @property
    def timeindex(self) -> pd.Index | None:
        return self._timeindex


def import_results_from_resultpackage(path: str | Path) -> ImportResults:
    """
    Erzeugt ein ImportResults-Objekt aus
    - einem Verzeichnis (mit 'datapackage.json' und 'results/*/*.csv') oder
    - einer ZIP-Datei, die genau diese Struktur enthält.

    """
    path = Path(path)

    # ZIP-Datei: temporär entpacken
    if path.is_file():
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            with ZipFile(path, "r") as zf:
                zf.extractall(tmp_root)
            # ImportResults liest beim __init__ sofort alle Daten ein,
            # das temporäre Verzeichnis kann danach gelöscht werden.
            return ImportResults(tmp_root)

    # Verzeichnis
    if path.is_dir():
        return ImportResults(path)

    raise FileNotFoundError(f"{path} ist weder Verzeichnis noch ZIP-Datei.")
