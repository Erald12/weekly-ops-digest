# Weekly Ops Digest

A Python pipeline that reads two weeks of sales data, calculates the key metrics, creates charts, and asks Claude to write a short plain-English summary. Python does all the math. Claude only writes the words, and a check in Python blocks any summary that includes a number not found in the data.

## What it produces

- `output/weekly_digest.md`: a summary, a product breakdown table, and embedded charts
- `output/charts/`: three PNG charts
  - Revenue by product, this week vs last week
  - Daily revenue, this week
  - Returns by product, this week

## How it works

```
incoming/*.csv  ->  metrics.py  ->  charts.py  ->  summarize.py  ->  weekly_digest.md
   (data)          (Python math)   (PNG files)   (Claude + check)     (report)
```

1. `metrics.py` totals revenue, units, and returns, compares this week to last week, and computes return rates by product.
2. `charts.py` draws three charts with matplotlib.
3. `summarize.py` sends the calculated figures to Claude, then checks that every number in the reply appears in the data. If a number doesn't match, the summary is replaced with a warning, and the report still includes the table and charts.
4. `main.py` ties the steps together and writes the report.

## Project structure

```
weekly-ops-digest/
├── requirements.txt
├── .env.example
├── .gitignore
├── incoming/
│   ├── sales_this_week.csv
│   └── sales_last_week.csv
├── output/                 # generated, not committed
└── src/
    ├── metrics.py
    ├── charts.py
    ├── summarize.py
    └── main.py
```

## Input format

Both CSV files use the same columns:

| Column | Description |
|---|---|
| `date` | Sale date (YYYY-MM-DD) |
| `product` | Product name |
| `units` | Units sold (integer) |
| `revenue` | Revenue in pesos (number) |
| `returns` | Units returned (integer) |

The sample files in `incoming/` contain fake data for testing. Replace them with your own exports, keeping the same columns.

## Setup

Requires Python 3.9 or later and an Anthropic API key.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
```

Open `.env` and replace `your_key_here` with your API key. Don't commit this file.

## Run

From the project root:

```bash
python -m src.main
```

The script prints where the report and charts were written. Open `output/weekly_digest.md` in any Markdown viewer.

On Windows, you can also run it from PyCharm. Set the **Working directory** in the run configuration to the project folder.

## Scheduling (optional)

To run it every Monday morning:

- **Windows:** create a task in Task Scheduler that runs `python -m src.main` with the project folder as the start-in directory.
- **Linux/macOS:** add a cron entry, for example `0 8 * * 1 cd /path/to/weekly-ops-digest && .venv/bin/python -m src.main`.

## Cost and limits

- Each run makes one Claude API call, so the cost is small.
- The number check compares digits only. It catches invented figures, but it can't verify that Claude described a number correctly, such as calling a change an increase when it was a decrease. Read the summary before sharing it.
- The sample data is fictional. Test with a few real weeks before relying on the output.

## Results

<!-- Fill in with real measurements before sharing -->
- Manual time to build this report: about ___ minutes
- Pipeline run time: about ___ seconds
- Summaries withheld by the number check in testing: ___ of ___ runs

## Tools

Python, pandas-free standard library for metrics, matplotlib for charts, the Anthropic API for the summary, and Claude Code for development.
