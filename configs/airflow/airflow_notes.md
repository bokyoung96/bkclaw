# Airflow Notes

초기 단계에서는 skeleton만 둡니다.

예상 DAG:
- paper_idea_pipeline
- nightly_data_refresh
- weekly_research_report

실제 설치 시 결정할 것:
- executor(LocalExecutor / CeleryExecutor 등)
- metadata DB(sqlite / postgres)
- docker 내부 단일 실행 vs 분리 실행
