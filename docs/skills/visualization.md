# Data Visualization

Create clear, honest, high-density charts following the principles of Edward Tufte (*The Visual Display of Quantitative Information*) and Stephen Few (*Show Me the Numbers*, *Information Dashboard Design*). Every pixel should serve the data.

## Core Principles

### 1. Maximize the data-ink ratio (Tufte)

> "Data-ink is the non-erasable core of a graphic. If you erase it, the chart loses information."

Every mark on the page should represent data. Remove borders, background fills, redundant gridlines, decorative elements, and 3D effects. What remains is the data-ink -- the irreducible core.

### 2. Simplify to clarify (Few)

Every design choice should reduce the time from "I see the chart" to "I understand the insight." If the reader must study a legend, decode a color scheme, or mentally subtract decoration from data, the chart has failed.

### 3. Honest proportions (Tufte)

The visual representation of numbers should be directly proportional to the quantities they represent. Truncated axes, perspective distortion, and dual y-axes violate this principle.

---

## How It Works

1. **Identify the question** -- A chart without a clear question is decoration.
2. **Choose the right chart type** -- Match the data relationship to the visual encoding (see Chart Selection).
3. **Build and declutter** -- Apply the removal checklist until only data remains.
4. **Check for lies** -- Verify axes, proportions, and aspect ratio do not distort the data.
5. **State the insight** -- The title should tell the reader what they are looking at and why it matters.

## Chart Selection

| Data relationship | Use | Avoid |
|---|---|---|
| Comparison across categories | Horizontal bar | Pie, donut, radar |
| Comparison over time | Line chart | Area chart (unless stacked parts-of-whole) |
| Distribution | Histogram, box plot, strip plot | 3D histogram |
| Part-of-whole | Stacked bar, treemap | Pie (unless 2-3 slices max) |
| Correlation | Scatter plot | Bubble chart with 3+ encoded dims |
| Ranking | Horizontal bar (sorted) | Vertical bar (hard to read labels) |
| Single KPI + target | Bullet graph (Few) | Gauge/speedometer |
| Small counts (<5 items) | Table or dot plot | Any chart -- a table is clearer |

---

## Good and Bad Examples

### Comparison: Pie chart vs. sorted bar

!!! failure "Bad: 3D exploded pie chart"
    ```python
    import matplotlib.pyplot as plt

    sizes = [35, 25, 20, 15, 5]
    labels = ["Product A", "Product B", "Product C", "Product D", "Product E"]
    explode = (0.1, 0.05, 0, 0, 0)
    colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct="%1.1f%%", shadow=True, startangle=90)
    ax.set_title("Market Share")
    ```

    **Why it fails:**

    - Humans misjudge angles -- 20% and 25% look identical in a pie chart.
    - Exploded slices physically separate the parts, making comparison even harder.
    - Shadow and 3D add chartjunk (Tufte) -- decoration with zero information value.
    - Five saturated colors fight for attention instead of guiding the eye.
    - The title describes the topic ("Market Share") but not the insight.

!!! success "Good: Sorted horizontal bar with direct labels"
    ```python
    import matplotlib.pyplot as plt

    categories = ["Product A", "Product B", "Product C", "Product D", "Product E"]
    values = [35, 25, 20, 15, 5]

    pairs = sorted(zip(values, categories))
    values, categories = zip(*pairs)

    fig, ax = plt.subplots(figsize=(7, 3.5))
    bars = ax.barh(categories, values, color="#4878A8", height=0.6)
    ax.bar_label(bars, fmt="%.0f%%", padding=4, fontsize=10)

    ax.set_xlim(0, 45)
    ax.set_title("Product A leads with 35% market share",
                 fontsize=12, fontweight="bold", loc="left")
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.tick_params(bottom=False, labelbottom=False)
    ax.tick_params(left=False)
    plt.tight_layout()
    ```

    **Why it works:**

    - Sorted bars enable instant comparison -- the ranking is self-evident.
    - Direct labels eliminate the need for an x-axis or mental estimation.
    - Only the left spine remains (minimal non-data ink).
    - Single muted color because all bars represent the same measure.
    - Title states the insight: "Product A leads with 35% market share."

---

### Time Series: Dual-axis vs. small multiples

!!! failure "Bad: Dual-axis line chart"
    ```python
    import matplotlib.pyplot as plt

    months = range(1, 13)
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

    **Why it fails:**

    - Dual y-axes are inherently misleading: by changing the scale of either axis, you can fabricate or hide any apparent correlation. The reader cannot tell if the lines "move together" or if the scales were chosen to make it look that way.
    - Two separate legends for two lines adds unnecessary cognitive load.
    - Full black gridlines compete with the data lines for visual attention.
    - Red-blue color pairing is a cliche that provides no semantic meaning.

!!! success "Good: Small multiples with shared x-axis"
    ```python
    import matplotlib.pyplot as plt

    months = range(1, 13)
    revenue = [10, 12, 15, 14, 18, 22, 25, 24, 28, 30, 35, 40]
    headcount = [50, 52, 53, 55, 58, 60, 62, 65, 68, 70, 72, 75]
    month_labels = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 5), sharex=True)

    ax1.plot(months, revenue, color="#4878A8", linewidth=2)
    ax1.set_ylabel("Revenue ($M)")
    ax1.set_title("Revenue quadrupled; headcount grew 50%",
                  fontsize=12, fontweight="bold", loc="left")
    ax1.annotate(f"${revenue[-1]}M", xy=(12, revenue[-1]),
                 fontsize=10, color="#4878A8", fontweight="bold")

    ax2.plot(months, headcount, color="#D4652F", linewidth=2)
    ax2.set_ylabel("Headcount")
    ax2.set_xticks(list(months))
    ax2.set_xticklabels(month_labels)
    ax2.annotate(f"{headcount[-1]}", xy=(12, headcount[-1]),
                 fontsize=10, color="#D4652F", fontweight="bold")

    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#EEEEEE", linewidth=0.5)

    plt.tight_layout()
    ```

    **Why it works:**

    - Each metric has its own panel and its own honest y-axis scale.
    - No misleading correlation is implied -- the reader draws their own conclusions.
    - Direct annotation at the end of each line replaces legends.
    - Light gridlines (`#EEEEEE`) aid estimation without competing with data.
    - Title states the comparison: "Revenue quadrupled; headcount grew 50%."

---

### Multiple Series: Spaghetti vs. highlight

!!! failure "Bad: Rainbow spaghetti chart"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(12):
        ax.plot(np.random.randn(50).cumsum(), linewidth=1)
    ax.legend([f"Series {i}" for i in range(12)],
              loc="upper left", fontsize=7)
    ax.set_title("All Series")
    ax.grid(True, color="black", alpha=0.3)
    ```

    **Why it fails:**

    - Twelve undifferentiated lines are visually unresolvable -- the reader cannot trace any individual series.
    - The legend with 12 entries requires constant cross-referencing (a "lookup table" the reader must decode).
    - Black gridlines compete with the data for visual priority.
    - The title "All Series" communicates nothing.

!!! success "Good: Highlight one, gray the rest"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    fig, ax = plt.subplots(figsize=(7, 4))

    for i in range(11):
        data = np.random.randn(50).cumsum()
        ax.plot(data, color="#CCCCCC", linewidth=0.8, alpha=0.6)

    highlight = np.random.randn(50).cumsum() + 10
    ax.plot(highlight, color="#D4652F", linewidth=2.5)
    ax.annotate("Product X", xy=(49, highlight[-1]),
                fontsize=10, color="#D4652F", fontweight="bold",
                xytext=(5, 0), textcoords="offset points")

    ax.set_title("Product X outperformed all peers",
                 fontsize=12, fontweight="bold", loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#EEEEEE", linewidth=0.5)
    plt.tight_layout()
    ```

    **Why it works:**

    - Gray context lines show the competitive field without demanding attention.
    - One saturated color draws the eye to the story instantly (preattentive processing -- Few).
    - Direct label on the highlighted series eliminates the legend entirely.
    - Title states the finding: "Product X outperformed all peers."

---

### KPI Display: Gauge vs. bullet graph

!!! failure "Bad: Gauge / speedometer chart"
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

    **Why it fails:**

    - A gauge uses a large circular area to display a single number -- extreme waste of space.
    - The semicircular shape means the visual distance between values is inconsistent (angular vs. linear).
    - Red-yellow-green (traffic light) encoding is inaccessible to the ~8% of men who are red-green colorblind.
    - The decorative dial metaphor (mimicking a physical instrument) is pure chartjunk.

!!! success "Good: Bullet graph (Stephen Few, 2006)"
    ```python
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 1.5))

    # Qualitative ranges (light to dark = poor to excellent)
    ax.barh(0, 100, height=0.5, color="#DDDDDD")
    ax.barh(0, 75, height=0.5, color="#BBBBBB")
    ax.barh(0, 50, height=0.5, color="#999999")

    # Actual value
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

    **Why it works:**

    - Encodes actual value, target, and qualitative ranges in a compact horizontal strip.
    - Multiple bullet graphs stack vertically for dashboards -- far more space-efficient than gauges.
    - Grayscale is inherently colorblind-safe.
    - Linear encoding means visual distance is proportional to numeric distance (no angular distortion).
    - Designed by Stephen Few specifically to replace gauges in dashboards.

---

### Proportions: Truncated axis vs. honest axis

!!! failure "Bad: Truncated y-axis on a bar chart"
    ```python
    import matplotlib.pyplot as plt

    products = ["A", "B", "C"]
    values = [98, 100, 102]

    fig, ax = plt.subplots()
    ax.bar(products, values, color=["red", "blue", "green"])
    ax.set_ylim(96, 104)
    ax.set_title("Product Performance")
    ```

    **Why it fails:**

    - Truncating the y-axis makes a 4% total range look like a 10x difference. This is Tufte's **lie factor** -- the visual representation is not proportional to the data.
    - Bar charts encode value as bar *length* measured from zero. Without a zero baseline, the bars lie.
    - Three different saturated colors for bars representing the same measure add false distinctions.

!!! success "Good: Full axis with annotation"
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

    **Why it works:**

    - Y-axis starts at zero, so bar lengths honestly represent the quantities.
    - The title communicates the real story: the differences are negligible.
    - Single color because all bars represent the same measure.
    - If the small differences truly matter, use a **dot plot** or **table** instead -- chart types that do not require a zero baseline.

---

## Color Guidelines

| Purpose | Approach | Example |
|---|---|---|
| Default | Single muted hue for all marks | `#4878A8` (steel blue) |
| Emphasis | One saturated/warm color for the focal point | `#D4652F` (burnt orange) |
| Categorical (2-5) | Colorblind-safe distinct hues | `#4878A8`, `#D4652F`, `#6AAF6A`, `#8B6CAF`, `#C75A7A` |
| Sequential | Single-hue gradient (light to dark) | Blues: `#deebf7` to `#08519c` |
| Diverging | Two-hue gradient with neutral midpoint | Blue-white-red |

!!! warning "Never use rainbow colormaps"
    Rainbow colormaps (`jet`, `rainbow`, `hsv`) create false boundaries in continuous data, are not perceptually uniform, and fail for colorblind users. Use `viridis`, `cividis`, or single-hue sequential palettes instead.

---

## Declutter Checklist

Apply this checklist to every chart before finalizing:

- [ ] Remove 3D effects, shadows, and gradient fills
- [ ] Remove chart border (box around the plot area)
- [ ] Remove top and right axis spines
- [ ] Remove or lighten gridlines to `#EEEEEE`
- [ ] Remove legend if labels can go directly on the data
- [ ] Remove redundant axis labels (if units are in the title)
- [ ] Check that the title states an insight, not just a topic
- [ ] Verify bar charts start at zero
- [ ] Verify no dual y-axes (use small multiples instead)
- [ ] Confirm the color palette works in grayscale / for colorblind users

---

## Key References

- **Tufte, E.R.** (2001). *The Visual Display of Quantitative Information*. 2nd ed.
- **Tufte, E.R.** (2006). *Beautiful Evidence*.
- **Few, S.** (2012). *Show Me the Numbers*. 2nd ed.
- **Few, S.** (2006). *Information Dashboard Design*.
- **Few, S.** (2006). "Bullet Graph Design Specification." Perceptual Edge.
- **Wilke, C.O.** (2019). *Fundamentals of Data Visualization*. O'Reilly.
