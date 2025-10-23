# Removed Test Filtering


## Initial cases.ndjson content:

  {"name": "test1", "result": "OK", "duration_ms": 100, "ai_review": null}
  {"name": "test2", "result": "FAIL", "duration_ms": 200, "ai_review": null}
  {"name": "test3", "result": "OK", "duration_ms": 150, "ai_review": null}

## Updated cases.ndjson content (test2 should be removed):

  {"name": "test1", "result": "OK", "duration_ms": 100, "ai_review": null}
  {"name": "test3", "result": "OK", "duration_ms": 150, "ai_review": null}
Number of cases after filtering: 2
Remaining test names: ['test1', 'test3']

✓ Removed test was successfully filtered out!
