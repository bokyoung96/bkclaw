from tft_us_quantdb.validation import validate_quantdb_pipeline


def test_validation_runs_and_passes() -> None:
    results = validate_quantdb_pipeline()
    assert results
    assert all(result.passed for result in results)
