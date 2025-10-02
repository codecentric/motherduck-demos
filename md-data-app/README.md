# Motherduck Data App Demo

A simple data app built with plotly/dash and motherduck

### Run the the demo
1. Install dependencies
```shell
uv sync
```

2. Run app
```shell
uv run python main.py
```

3. Open web-app on http://127.0.0.1:8050/

### Optional:
If you want to skip browser authentication to Motherduck, you can export your MOTHERDUCK_TOKEN as an environment variable:
```shell
export MOTHERDUCK_TOKEN=...
```

The token can be retrieved, e.g. in the duckdb cli:
```sql
ATTACH 'md:'
PRAGMA PRINT_MD_TOKEN;
```

or in the Motherduck UI: https://app.motherduck.com/settings/tokens