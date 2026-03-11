import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import pandas as pd
import numpy as np

# Realistic Phase Details for College Project (w/ Milestones)
phases = [
    # Phase 1
    {"Task": "Literature Survey & Req Gathering", "Phase": "1. Planning", "Start": "2025-08-01", "Finish": "2025-08-15", "Color": "#1f77b4", "Type": "Task"},
    {"Task": "Project Scope & Feasibility", "Phase": "1. Planning", "Start": "2025-08-15", "Finish": "2025-08-25", "Color": "#1f77b4", "Type": "Task"},
    {"Task": "★ Synopsis Approval", "Phase": "1. Planning", "Start": "2025-08-25", "Finish": "2025-08-25", "Color": "#e377c2", "Type": "Milestone"},
    
    # Phase 2
    {"Task": "UI/UX & Wireframing", "Phase": "2. Design", "Start": "2025-08-26", "Finish": "2025-09-15", "Color": "#ff7f0e", "Type": "Task"},
    {"Task": "Database & Architecture Plan", "Phase": "2. Design", "Start": "2025-09-15", "Finish": "2025-09-30", "Color": "#ff7f0e", "Type": "Task"},
    {"Task": "★ Design Phase Completion", "Phase": "2. Design", "Start": "2025-09-30", "Finish": "2025-09-30", "Color": "#e377c2", "Type": "Milestone"},
    
    # Phase 3
    {"Task": "Backend App Development", "Phase": "3. Implementation", "Start": "2025-10-01", "Finish": "2025-10-31", "Color": "#2ca02c", "Type": "Task"},
    {"Task": "Frontend UI Development", "Phase": "3. Implementation", "Start": "2025-11-01", "Finish": "2025-11-30", "Color": "#2ca02c", "Type": "Task"},
    {"Task": "★ Core System MVP Ready", "Phase": "3. Implementation", "Start": "2025-11-30", "Finish": "2025-11-30", "Color": "#e377c2", "Type": "Milestone"},
    
    # Phase 4
    {"Task": "Data Collection & Preprocessing", "Phase": "4. ML Integration", "Start": "2025-12-01", "Finish": "2025-12-20", "Color": "#d62728", "Type": "Task"},
    {"Task": "Model Training & API Linking", "Phase": "4. ML Integration", "Start": "2025-12-21", "Finish": "2026-01-15", "Color": "#d62728", "Type": "Task"},
    {"Task": "★ ML Integration Success", "Phase": "4. ML Integration", "Start": "2026-01-15", "Finish": "2026-01-15", "Color": "#e377c2", "Type": "Milestone"},
    
    # Phase 5
    {"Task": "System Testing & Bug Fixing", "Phase": "5. Testing & Docs", "Start": "2026-01-16", "Finish": "2026-02-10", "Color": "#9467bd", "Type": "Task"},
    {"Task": "Blackbook Writing & Final Polish", "Phase": "5. Testing & Docs", "Start": "2026-02-11", "Finish": "2026-02-28", "Color": "#9467bd", "Type": "Task"},
    {"Task": "★ Final Project Submission", "Phase": "5. Testing & Docs", "Start": "2026-02-28", "Finish": "2026-02-28", "Color": "#e377c2", "Type": "Milestone"}
]

df = pd.DataFrame(phases)
df['Start'] = pd.to_datetime(df['Start'])
df['Finish'] = pd.to_datetime(df['Finish'])
df['Duration'] = df['Finish'] - df['Start']

fig, ax = plt.subplots(figsize=(12.5, 8.5))
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#f8f9fa')

tasks = df['Task'][::-1].reset_index(drop=True)
y_pos = np.arange(len(tasks))

# Plot bars and milestones
for i, task in enumerate(tasks):
    row = df[df['Task'] == task].iloc[0]
    
    if row['Type'] == 'Task':
        ax.barh(i, row['Duration'].days, left=mdates.date2num(row['Start']), color=row['Color'], edgecolor='white', height=0.6, alpha=0.85)
    else:
        # Plot milestone star
        ax.plot(mdates.date2num(row['Start']), i, marker='*', markersize=20, color='#e377c2', markeredgecolor='white')

ax.set_yticks(y_pos)
# Handle styling for task names
yticklabels = []
for t in tasks:
    if "★" in t:
        yticklabels.append(t)
    else:
        yticklabels.append(t)
ax.set_yticklabels(yticklabels, fontsize=11, fontweight='500', color='#333333')

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.xticks(rotation=0, fontsize=10, color='#333333')
plt.xlabel("Timeline (August 2025 - February 2026)", fontsize=12, fontweight='bold', color='#333333', labelpad=15)
plt.title("AGMIS College Project Implementation Timeline", fontsize=16, fontweight='bold', color='#111111', pad=20)

ax.xaxis.grid(True, linestyle='--', color='#cccccc', alpha=0.7)
ax.set_axisbelow(True)

legend_elements = [
    Patch(facecolor='#1f77b4', alpha=0.85, label='1. Planning'),
    Patch(facecolor='#ff7f0e', alpha=0.85, label='2. Design'),
    Patch(facecolor='#2ca02c', alpha=0.85, label='3. Implementation'),
    Patch(facecolor='#d62728', alpha=0.85, label='4. ML Integration'),
    Patch(facecolor='#9467bd', alpha=0.85, label='5. Testing & Docs'),
    plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#e377c2', markersize=16, label='Milestone')
]
ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, frameon=False, fontsize=10)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')

ax.set_xlim(mdates.date2num(pd.to_datetime("2025-07-25")), mdates.date2num(pd.to_datetime("2026-03-05")))

plt.tight_layout()
plt.savefig(r'e:\\Projects\\agmis\\Docs\\AGMIS_College_Gantt_Chart.png', dpi=300, bbox_inches='tight')
print("Successfully generated: Docs/AGMIS_College_Gantt_Chart.png")
