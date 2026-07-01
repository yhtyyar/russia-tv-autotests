#!/usr/bin/env python3
"""Generate Performance Dashboard HTML from Web Vitals history.

Usage:
    python scripts/generate_perf_dashboard.py

Reads reports/performance/history.json, writes perf/index.html.
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

HISTORY_PATH = Path("reports/performance/history.json")
OUTPUT_PATH = Path("perf/index.html")

BUDGETS = {"LCP": 2500, "CLS": 0.1, "FCP": 1800, "TTFB": 600}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Performance Dashboard — russia-tv.online</title>
<style>
:root{{ --bg:#0f172a; --card:#1e293b; --text:#e2e8f0; --muted:#94a3b8;
  --ok:#22c55e; --warn:#eab308; --bad:#ef4444; --accent:#38bdf8; }}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.5}}
.container{{max-width:1200px;margin:0 auto;padding:24px}}
h1{{font-size:1.8rem;margin-bottom:8px}} .subtitle{{color:var(--muted);margin-bottom:24px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-bottom:32px}}
.card{{background:var(--card);border-radius:12px;padding:20px}}
.card h2{{font-size:1.1rem;margin-bottom:12px;color:var(--accent)}}
.metric{{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #334155}}
.metric:last-child{{border:none}}
.metric .name{{font-weight:600}} .metric .val{{font-family:monospace;font-size:1.1rem}}
.status{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-left:8px}}
.status.ok{{background:var(--ok)}} .status.warn{{background:var(--warn)}} .status.bad{{background:var(--bad)}}
.budget{{color:var(--muted);font-size:0.85rem}}
table{{width:100%;border-collapse:collapse;margin-top:12px}}
th,td{{padding:10px;text-align:left;border-bottom:1px solid #334155;font-size:0.9rem}}
th{{color:var(--accent);font-weight:600}}
tr:hover{{background:#334155/30}}
.chart{{height:200px;margin-top:16px;position:relative}}
.chart svg{{width:100%;height:100%}}
.footer{{text-align:center;color:var(--muted);margin-top:40px;font-size:0.8rem}}
a{{color:var(--accent)}}
</style>
</head>
<body>
<div class="container">
  <h1>📊 Performance Dashboard</h1>
  <p class="subtitle">russia-tv.online — Core Web Vitals &mdash; последнее обновление: {updated}</p>

  <div class="grid">
    {cards}
  </div>

  <div class="card">
    <h2>📈 История метрик</h2>
    {history_table}
  </div>

  <div class="card">
    <h2>📉 Тренды по метрикам</h2>
    {charts}
  </div>

  <div class="footer">
    <a href="https://yhtyyar.github.io/russia-tv-autotests/allure/">Allure Report</a> &bull;
    <a href="https://github.com/yhtyyar/russia-tv-autotests">GitHub</a>
  </div>
</div>
</body>
</html>
"""


def _status(v: float, budget: float) -> str:
    if v <= budget:
        return "ok"
    if v <= budget * 1.5:
        return "warn"
    return "bad"


def _fmt(v: float, key: str) -> str:
    if key == "CLS":
        return f"{v:.3f}"
    return f"{v:.0f} ms"


def build_cards(latest: dict[str, dict[str, float]]) -> str:
    cards = []
    for page, metrics in latest.items():
        rows = ""
        for key in ["FCP", "LCP", "CLS", "TTFB"]:
            val = metrics.get(key)
            budget = BUDGETS.get(key, 0)
            if val is None:
                continue
            st = _status(val, budget)
            rows += (
                f'<div class="metric">'
                f'<span class="name">{key}</span>'
                f'<span><span class="val">{_fmt(val, key)}</span>'
                f'<span class="status {st}"></span></span></div>'
            )
        cards.append(f'<div class="card"><h2>🌐 {page}</h2>{rows}</div>')
    return "\n".join(cards)


def build_history_table(history: list[dict[str, Any]]) -> str:
    if not history:
        return "<p>Нет данных</p>"
    rows = ""
    for run in reversed(history[-20:]):
        ts = run["timestamp"][:19].replace("T", " ")
        pages = run.get("pages", {})
        for page, metrics in pages.items():
            vals = " ".join(f"{k}={_fmt(v, k)}" for k, v in metrics.items() if k in BUDGETS)
            rows += f"<tr><td>{ts}</td><td>{page}</td><td>{vals}</td></tr>"
    return (
        f"<table><thead><tr><th>Дата</th><th>Страница</th>"
        f"<th>Метрики</th></tr></thead><tbody>{rows}</tbody></table>"
    )


def build_charts(history: list[dict[str, Any]]) -> str:
    if len(history) < 2:
        return "<p>Недостаточно данных для графиков (нужно ≥2 прогона)</p>"
    # Simple sparklines as SVG polylines
    charts_html = ""
    for metric in ["LCP", "CLS", "FCP", "TTFB"]:
        data = []
        labels = []
        for run in history:
            for _page, metrics in run.get("pages", {}).items():
                v = metrics.get(metric)
                if v is not None:
                    data.append(v)
                    labels.append(run["timestamp"][:10])
        if not data:
            continue
        # Normalize to 0-180 height
        max_v = max(data) * 1.2
        min_v = 0
        points = " ".join(
            f"{i * (300 / max(len(data)-1, 1)):.1f},{180 - (v - min_v) / (max_v - min_v) * 180:.1f}"
            for i, v in enumerate(data)
        )
        budget = BUDGETS[metric]
        budget_y = 180 - (budget / max_v) * 180
        charts_html += (
            f'<div class="card"><h3>{metric} (бюджет: {budget}{" ms" if metric != "CLS" else ""})</h3>'
            f'<div class="chart"><svg viewBox="0 0 300 180" preserveAspectRatio="none">'
            f'<line x1="0" y1="{budget_y:.1f}" x2="300" y2="{budget_y:.1f}" stroke="#ef4444" stroke-dasharray="4" opacity="0.5"/>'
            f'<polyline points="{points}" fill="none" stroke="#38bdf8" stroke-width="2"/>'
            f'</svg></div></div>'
        )
    return charts_html


def main() -> None:
    history: list[dict[str, Any]] = []
    if HISTORY_PATH.exists():
        history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))

    latest = history[-1].get("pages", {}) if history else {}

    cards = build_cards(latest)
    table = build_history_table(history)
    charts = build_charts(history)

    html = HTML_TEMPLATE.format(
        updated=datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC"),
        cards=cards,
        history_table=table,
        charts=charts,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"Performance Dashboard generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
