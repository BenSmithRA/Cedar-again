#!/usr/bin/env python3
"""
Convert a CEDAR "timber" export (the .xlsx you download from
https://cedar.azurewebsites.net/export/) into data/factors.json for the
fast CEDAR browser.

Usage:
    pip install pandas openpyxl
    python convert_timber.py path/to/your_export.xlsx

This writes data/factors.json, overwriting the placeholder sample data.
"""

import sys
import json
from pathlib import Path

TIMBER_COLUMNS = [
    "id_res_out", "pid_res_out", "id_reference", "pid_reference", "ref_rwid",
    "ref_doi", "ref_pmid", "ref_bibtex_key", "ref_title", "country",
    "study_design", "id_factor", "pid_factor", "factor_title",
    "factor_description", "factor_group", "comparator_group",
    "host_level_01", "host_level_02", "host_production_stream",
    "host_life_stage", "stage_allocate", "stage_observe", "moa_type",
    "moa_unit", "resistance_class", "resistance", "resistance_gene",
    "microbe_level_01", "microbe_level_02", "is_figure_extract",
    "figure_extract_method", "figure_extract_reproducible",
    "contable_a", "contable_b", "contable_c", "contable_d",
    "prevtable_a", "prevtable_b", "prevtable_c", "prevtable_d",
    "table_n_exp", "table_n_ref", "odds_ratio", "odds_ratio_lo",
    "odds_ratio_up", "odds_ratio_sig", "odds_ratio_confidence",
]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"File not found: {src}")
        sys.exit(1)

    try:
        import pandas as pd
    except ImportError:
        print("Missing dependency. Run: pip install pandas openpyxl")
        sys.exit(1)

    if src.suffix.lower() == ".csv":
        df = pd.read_csv(src)
    else:
        df = pd.read_excel(src)

    # Keep only columns we know about, in case the export has extras.
    present = [c for c in TIMBER_COLUMNS if c in df.columns]
    missing = [c for c in TIMBER_COLUMNS if c not in df.columns]
    if missing:
        print(f"Note: export is missing expected columns (fine, they'll just be blank): {missing}")

    df = df[present]
    df = df.where(pd.notnull(df), None)

    records = json.loads(df.to_json(orient="records"))

    out = {
        "is_sample_data": False,
        "generated_note": f"Converted from {src.name}",
        "factors": records,
    }

    out_path = Path(__file__).parent / "data" / "factors.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(records)} factors to {out_path}")


if __name__ == "__main__":
    main()
