from __future__ import annotations

import argparse
import json
from pathlib import Path

from reliability_lab.chaos import load_queries, run_cache_comparison, run_simulation
from reliability_lab.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--out", default="reports/metrics.json")
    args = parser.parse_args()
    config = load_config(args.config)
    queries = load_queries()

    metrics = run_simulation(config, queries)
    out_path = Path(args.out)
    metrics.write_json(out_path)

    csv_path = out_path.with_suffix(".csv")
    metrics.write_csv(csv_path)

    comparison = run_cache_comparison(config, queries)
    comparison_path = out_path.parent / "cache_comparison.json"
    comparison_path.write_text(json.dumps(comparison, indent=2, ensure_ascii=False))

    print(f"wrote {out_path}")
    print(f"wrote {csv_path}")
    print(f"wrote {comparison_path}")


if __name__ == "__main__":
    main()
