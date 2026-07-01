---
name: visualization
description: Create clear, honest, high-density charts following Tufte and Few principles. Use when building data visualizations, plots, or charts and the user wants publication-quality, non-misleading output.
---

# Data Visualization

Create clear, honest, high-density charts following the principles of Edward Tufte and Stephen Few. Every pixel should serve the data.

## Steps

1. Identify the data and the question the chart must answer. A chart without a clear question is decoration.
2. Choose the right chart type (see Chart Selection below).
3. Build the chart using matplotlib, plotly, or altair.
4. Apply the declutter checklist:
   - Remove chartjunk: 3D effects, background images, gradient fills, decorative gridlines.
   - Maximize the data-ink ratio: every mark on the page should represent data.
   - Remove or mute gridlines (light gray at most, never black).
   - Remove chart borders and unnecessary axis spines (keep only left and bottom).
   - Remove legends when labels can be placed directly on the data.
   - Use direct annotation instead of forcing the reader to cross-reference a legend.
   - Use a muted, colorblind-safe palette. Reserve bright/saturated color for emphasis only.
5. Check for lie factor violations:
   - Axes must start at zero for bar charts and area charts (never truncate).
   - Line charts and dot plots may use a non-zero baseline when the range is meaningful.
   - Aspect ratio should not exaggerate or flatten trends. Use banking to 45 degrees when possible.
   - Dual y-axes are almost always misleading. Use small multiples instead.
6. Apply small multiples when comparing across categories. One clear pattern per panel is better than one overloaded chart.
7. Add a clear, descriptive title that states the insight, not just the topic. "Revenue grew 40% in Q3" is better than "Revenue by Quarter."
8. Review final output against Tufte's test: if you removed this element, would the chart lose information? If not, remove it.

## Chart Selection

| Data relationship | Chart type | Avoid |
|---|---|---|
| Comparison across categories | Horizontal bar | Pie, donut, radar |
| Comparison over time | Line chart | Area chart (unless stacked parts-of-whole) |
| Distribution | Histogram, box plot, strip plot | 3D histogram |
| Part-of-whole | Stacked bar, treemap | Pie (unless 2-3 slices max) |
| Correlation | Scatter plot | Bubble chart with 3+ encoded dims |
| Ranking | Horizontal bar (sorted) | Vertical bar (hard to read labels) |
| Small counts | Table or dot plot | Any chart (a table is clearer for <5 items) |

## Examples

### BAD: 3D exploded pie chart

```python
import matplotlib.pyplot as plt

# 3D pie chart — everything wrong at once
fig, ax = plt.subplots(figsize=(8, 8))
sizes = [35, 25, 20, 15, 5]
labels = ["Product A", "Product B", "Product C", "Product D", "Product E"]
explode = (0.1, 0.05, 0, 0, 0)
colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"]

ax.pie(sizes, explode=explode, labels=labels, colors=colors,
       autopct="%1.1f%%", shadow=True, startangle=90)
ax.set_title("Market Share")
```

Pie charts distort proportions (humans misjudge angles). Exploded slices make comparison harder. Shadow and 3D add chartjunk. Five saturated colors fight for attention. The title describes the topic, not the insight.

### GOOD: Sorted horizontal bar

```python
import matplotlib.pyplot as plt

categories = ["Product A", "Product B", "Product C", "Product D", "Product E"]
values = [35, 25, 20, 15, 5]

# Sort descending
pairs = sorted(zip(values, categories))
values, categories = zip(*pairs)

fig, ax = plt.subplots(figsize=(7, 3.5))
bars = ax.barh(categories, values, color="#4878A8", height=0.6)
ax.bar_label(bars, fmt="%.0f%%", padding=4, fontsize=10)

ax.set_xlim(0, 45)
ax.set_xlabel("")
ax.set_title("Product A leads with 35% market share", fontsize=12, fontweight="bold", loc="left")
ax.spines[["top", "right", "bottom"]].set_visible(False)
ax.tick_params(bottom=False, labelbottom=False)
ax.tick_params(left=False)
plt.tight_layout()
```

Sorted bars are easy to compare. Direct labels eliminate the need for an x-axis. Only left spine remains. Single muted color. Title states the insight.

---

### BAD: Overloaded dual-axis line chart

```python
import matplotlib.pyplot as plt
import numpy as np

months = np.arange(1, 13)
revenue = [10, 12, 15, 14, 18, 22, 25, 24, 28, 30, 35, 40]
headcount = [50, 52, 53, 55, 58, 60, 62, 65, 68, 70, 72, 75]

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(months, revenue, "b-o", linewidth=2)
ax1.set_ylabel("Revenue ($M)", color="blue")

ax2 = ax1.twinx()
ax2.plot(months, headcount, "r-s", linewidth=2)
ax2.set_ylabel("Headcount", color="red")

ax1.set_title("Revenue and Headcount Over Time")
ax1.legend(["Revenue"], loc="upper left")
ax2.legend(["Headcount"], loc="upper right")
ax1.grid(True)
```

Dual y-axes mislead: by changing the scale of either axis, you can fabricate or hide any apparent correlation. Two legends for two lines adds clutter. Full grid obscures the data.

### GOOD: Small multiples with shared x-axis

```python
import matplotlib.pyplot as plt
import numpy as np

months = np.arange(1, 13)
revenue = [10, 12, 15, 14, 18, 22, 25, 24, 28, 30, 35, 40]
headcount = [50, 52, 53, 55, 58, 60, 62, 65, 68, 70, 72, 75]
month_labels = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 5), sharex=True)

ax1.plot(months, revenue, color="#4878A8", linewidth=2)
ax1.set_ylabel("Revenue ($M)")
ax1.set_title("Revenue quadrupled; headcount grew 50%", fontsize=12,
              fontweight="bold", loc="left")
ax1.annotate(f"${revenue[-1]}M", xy=(12, revenue[-1]),
             fontsize=10, color="#4878A8", fontweight="bold")

ax2.plot(months, headcount, color="#D4652F", linewidth=2)
ax2.set_ylabel("Headcount")
ax2.set_xticks(months)
ax2.set_xticklabels(month_labels)
ax2.annotate(f"{headcount[-1]}", xy=(12, headcount[-1]),
             fontsize=10, color="#D4652F", fontweight="bold")

for ax in (ax1, ax2):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#EEEEEE", linewidth=0.5)

plt.tight_layout()
```

Each metric gets its own panel with its own scale. No misleading correlation implied. Direct annotation replaces legends. Light gridlines aid reading without dominating. Title states the insight.

---

### BAD: Rainbow spaghetti line chart

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))
for i in range(12):
    ax.plot(np.random.randn(50).cumsum(), linewidth=1)
ax.legend([f"Series {i}" for i in range(12)], loc="upper left", fontsize=7)
ax.set_title("All Series")
ax.grid(True, color="black", alpha=0.3)
```

Twelve undifferentiated lines are unreadable. The legend requires constant cross-referencing. Black gridlines compete with data. The title says nothing.

### GOOD: Highlight one, gray the rest

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
fig, ax = plt.subplots(figsize=(7, 4))

# Gray background lines
for i in range(11):
    data = np.random.randn(50).cumsum()
    ax.plot(data, color="#CCCCCC", linewidth=0.8, alpha=0.6)

# Highlighted series
highlight = np.random.randn(50).cumsum() + 10
ax.plot(highlight, color="#D4652F", linewidth=2.5)
ax.annotate("Product X", xy=(49, highlight[-1]),
            fontsize=10, color="#D4652F", fontweight="bold",
            xytext=(5, 0), textcoords="offset points")

ax.set_title("Product X outperformed all peers", fontsize=12,
             fontweight="bold", loc="left")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color="#EEEEEE", linewidth=0.5)
plt.tight_layout()
```

Gray context lines show the field. One saturated color draws the eye to the story. Direct label eliminates the legend. Title states the finding.

---

### BAD: Cluttered dashboard gauge

```python
import plotly.graph_objects as go

fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=72,
    title={"text": "KPI Score"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "darkblue"},
        "steps": [
            {"range": [0, 33], "color": "red"},
            {"range": [33, 66], "color": "yellow"},
            {"range": [66, 100], "color": "green"},
        ],
        "threshold": {"line": {"color": "black", "width": 4}, "value": 90},
    },
))
```

Gauge charts waste space to display a single number. Traffic-light colors (red/yellow/green) are inaccessible to colorblind users. The decorative dial adds no information a number alone could not convey.

### GOOD: Bullet graph (Stephen Few)

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(7, 1.5))

# Qualitative ranges (light to dark = poor to excellent)
ax.barh(0, 100, height=0.5, color="#DDDDDD")  # poor
ax.barh(0, 75, height=0.5, color="#BBBBBB")   # satisfactory
ax.barh(0, 50, height=0.5, color="#999999")    # good

# Actual value (thin dark bar)
ax.barh(0, 72, height=0.22, color="#333333")

# Target marker
ax.plot(90, 0, marker="|", color="black", markersize=20, markeredgewidth=2.5)

ax.set_xlim(0, 105)
ax.set_yticks([])
ax.set_title("KPI: 72 / 90 target", fontsize=11, fontweight="bold", loc="left")
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(left=False)
plt.tight_layout()
```

Bullet graphs (Few, 2006) encode actual value, target, and qualitative ranges in minimal space. Grayscale is colorblind-safe. Multiple bullet graphs stack vertically for dashboards.

---

### BAD: Truncated y-axis bar chart

```python
import matplotlib.pyplot as plt

products = ["A", "B", "C"]
values = [98, 100, 102]

fig, ax = plt.subplots()
ax.bar(products, values, color=["red", "blue", "green"])
ax.set_ylim(96, 104)  # Truncated axis exaggerates tiny differences
ax.set_title("Product Performance")
```

Truncating the y-axis on a bar chart makes a 4% difference look like a 10x difference. This violates Tufte's lie factor principle. Three saturated colors for three bars add no information.

### GOOD: Full axis with annotation

```python
import matplotlib.pyplot as plt

products = ["A", "B", "C"]
values = [98, 100, 102]

fig, ax = plt.subplots(figsize=(5, 4))
bars = ax.bar(products, values, color="#4878A8", width=0.5)
ax.bar_label(bars, fmt="%.0f", padding=4)
ax.set_ylim(0, 120)
ax.set_title("Products perform within 4% of each other",
             fontsize=11, fontweight="bold", loc="left")
ax.spines[["top", "right"]].set_visible(False)
ax.set_ylabel("Score")
plt.tight_layout()
```

Full y-axis starting at zero shows the true proportion. The title honestly communicates that differences are small. Single color because the bars represent the same measure.

## Color Guidelines

- **Default palette**: Use a single muted hue for most marks. Add a second color only to encode a second variable.
- **Emphasis**: Reserve saturated or warm colors (orange, red) for the one thing you want the reader to notice.
- **Colorblind-safe palettes**: Use `#4878A8` (blue), `#D4652F` (orange), `#6AAF6A` (green), `#8B6CAF` (purple), `#C75A7A` (pink). Avoid red-green encoding.
- **Sequential data**: Use a single-hue gradient (light to dark). Never use rainbow colormaps (jet, rainbow, hsv).
- **Diverging data**: Use a two-hue gradient with a neutral midpoint (e.g., blue-white-red).
- **Background**: White or very light gray (`#F8F8F8`). Never dark backgrounds for print or static reports.

## Notes

- Tufte's core principle: "Above all else, show the data." If an element does not help the reader understand the data, remove it.
- Few's core principle: "Simplify to clarify." Every design choice should reduce the time to insight.
- Pie charts are acceptable only with 2-3 slices where the reader needs a part-of-whole impression, not precise comparison.
- Tables beat charts when the dataset has fewer than ~5 data points or when exact values matter more than patterns.
- Sparklines (Tufte) are excellent for embedding trends in tables or dashboards — small, word-sized line charts with no axes.
- Never use 3D charts for 2D data. The third dimension adds no information and distorts perception.
- Aspect ratio matters: wide charts flatten trends, tall charts exaggerate them. Default to roughly 2:1 width-to-height for line charts.
