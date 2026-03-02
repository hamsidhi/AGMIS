"""
Server-side chart generation using matplotlib.
Returns base64-encoded PNG for embedding in HTML img tags.
"""
import io
import base64
import os

# Avoid slow font cache on Windows - use temp dir and Agg backend before any other matplotlib import
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.path.dirname(__file__), ".mplcache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Use bundled font to avoid slow font search on first run
plt.rcParams["font.family"] = "DejaVu Sans"


def _fig_to_base64(fig, dpi=80):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def trend_chart(weeks, actual_scores, predicted_path):
    """Line chart: history (actual) + future prediction."""
    fig, ax = plt.subplots(figsize=(7, 3.5), facecolor="white")
    weeks = list(weeks) if weeks else ["Current", "Predicted"]
    actual = list(actual_scores) if actual_scores else [0]
    predicted = list(predicted_path) if predicted_path else [0]
    n = len(weeks)
    x = np.arange(n)
    # Plot actual only for points we have
    x_actual = x[: len(actual)]
    actual_plot = actual[: len(x_actual)] if len(actual) >= len(x_actual) else actual + [actual[-1]] * (len(x_actual) - len(actual)) if actual else [0] * len(x_actual)
    ax.plot(x_actual, actual_plot, "o-", color="#4f46e5", linewidth=2, markersize=6, label="History (actual)")
    pred_plot = (predicted + [predicted[-1]] * (n - len(predicted)))[:n] if predicted else [0] * n
    ax.plot(x, pred_plot, "--", color="#10b981", linewidth=2, label="Future prediction")
    ax.set_xticks(x)
    ax.set_xticklabels(weeks, rotation=45, ha="right")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score %")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    b64 = _fig_to_base64(fig)
    plt.close(fig)
    return b64


def metrics_pie_chart(attendance, assignments, internal):
    """Doughnut: Attendance, Assignments, Internal, Other."""
    fig, ax = plt.subplots(figsize=(5, 3.5), facecolor="white")
    att = float(attendance or 0)
    assign = float(assignments or 0)
    internal_val = float(internal or 0)
    other = max(0, 100 - att - assign - internal_val)
    sizes = [att, assign, internal_val, other]
    labels = ["Attendance %", "Assignments %", "Internal %", "Other"]
    colors = ["#4f46e5", "#10b981", "#f59e0b", "#e5e7eb"]
    result = ax.pie(sizes, labels=None, colors=colors, autopct="%1.1f%%", startangle=90, pctdistance=0.75)
    wedges = result[0]
    for w in wedges:
        w.set_edgecolor("white")
        w.set_linewidth(1.5)
    centre_circle = plt.Circle((0, 0), 0.50, fc="white")
    ax.add_artist(centre_circle)
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
    plt.tight_layout()
    b64 = _fig_to_base64(fig)
    plt.close(fig)
    return b64


def current_vs_target_chart(current_att, current_assign, current_internal, target_att=75, target_assign=80, target_internal=70):
    """Bar chart: current % vs target %."""
    fig, ax = plt.subplots(figsize=(6, 3), facecolor="white")
    labels = ["Attendance", "Assignments", "Internal"]
    current = [float(current_att or 0), float(current_assign or 0), float(current_internal or 0)]
    targets = [target_att, target_assign, target_internal]
    x = np.arange(len(labels))
    w = 0.35
    ax.bar(x - w / 2, current, w, label="Current %", color="#4f46e5", edgecolor="white")
    ax.bar(x + w / 2, targets, w, label="Target %", color="#10b981", alpha=0.7, edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("%")
    ax.set_ylim(0, 100)
    ax.legend(fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    b64 = _fig_to_base64(fig)
    plt.close(fig)
    return b64


def distribution_bar_chart(distribution):
    """Bar chart: Excellent, Good, Average, At Risk, Critical."""
    fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="white")
    labels = ["Excellent", "Good", "Average", "At Risk", "Critical"]
    dist = distribution or {}
    counts = [
        dist.get("excellent", 0) or 0,
        dist.get("good", 0) or 0,
        dist.get("average", 0) or 0,
        dist.get("at_risk", 0) or 0,
        dist.get("critical", 0) or 0,
    ]
    colors = ["#10b981", "#34d399", "#fbbf24", "#f59e0b", "#ef4444"]
    ax.bar(labels, counts, color=colors, edgecolor="white")
    ax.set_ylabel("Number of students")
    ymax = max(counts) * 1.15 if counts and max(counts) > 0 else 1
    ax.set_ylim(0, max(1, ymax))
    plt.xticks(rotation=25, ha="right")
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    b64 = _fig_to_base64(fig)
    plt.close(fig)
    return b64


def distribution_pie_chart(distribution):
    """Doughnut: performance distribution."""
    fig, ax = plt.subplots(figsize=(5, 3.5), facecolor="white")
    labels = ["Excellent", "Good", "Average", "At Risk", "Critical"]
    dist = distribution or {}
    sizes = [
        dist.get("excellent", 0) or 0,
        dist.get("good", 0) or 0,
        dist.get("average", 0) or 0,
        dist.get("at_risk", 0) or 0,
        dist.get("critical", 0) or 0,
    ]
    if sum(sizes) == 0:
        sizes = [1]
        labels = ["No data"]
    colors = ["#10b981", "#34d399", "#fbbf24", "#f59e0b", "#ef4444"][: len(sizes)]
    result = ax.pie(sizes, labels=None, colors=colors, autopct="%1.1f%%", startangle=90, pctdistance=0.75)
    wedges = result[0]
    for w in wedges:
        w.set_edgecolor("white")
        w.set_linewidth(1.5)
    centre_circle = plt.Circle((0, 0), 0.50, fc="white")
    ax.add_artist(centre_circle)
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
    plt.tight_layout()
    b64 = _fig_to_base64(fig)
    plt.close(fig)
    return b64


def risk_overview_pie_chart(at_risk_count, total):
    """Doughnut: At Risk vs On Track."""
    fig, ax = plt.subplots(figsize=(4, 3), facecolor="white")
    safe = max(0, (total or 0) - (at_risk_count or 0))
    sizes = [at_risk_count or 0, safe]
    if sum(sizes) == 0:
        sizes = [1]
        labels = ["No data"]
    else:
        labels = ["At Risk", "On Track"]
    colors = ["#ef4444", "#10b981"][: len(sizes)]
    result = ax.pie(sizes, labels=None, colors=colors, autopct="%1.1f%%", startangle=90, pctdistance=0.75)
    wedges = result[0]
    for w in wedges:
        w.set_edgecolor("white")
        w.set_linewidth(1.5)
    centre_circle = plt.Circle((0, 0), 0.55, fc="white")
    ax.add_artist(centre_circle)
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
    plt.tight_layout()
    b64 = _fig_to_base64(fig)
    plt.close(fig)
    return b64
