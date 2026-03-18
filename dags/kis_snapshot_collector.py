from __future__ import annotations

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="kis_snapshot_collector",
    start_date=datetime(2026, 3, 18),
    schedule="*/1 * * * *",
    catchup=False,
    max_active_runs=1,
    tags=["kis", "collector", "snapshot"],
) as dag:
    collect_snapshot = BashOperator(
        task_id="collect_snapshot",
        bash_command="cd /home/node/.openclaw/workspace && . .venv/bin/activate && python scripts/kis/run_snapshot_collector_once.py",
    )

    validate_storage = BashOperator(
        task_id="validate_storage",
        bash_command="cd /home/node/.openclaw/workspace && . .venv/bin/activate && python - <<'PY'\nfrom pathlib import Path\nfrom datetime import datetime, UTC\nroot = Path('data/kis/normalized') / datetime.now(UTC).strftime('%Y-%m-%d')\nfiles = list(root.glob('*.parquet'))\nassert files, 'no parquet files for today'\nfor f in files:\n    print(f)\nPY",
    )

    collect_snapshot >> validate_storage
