#!/usr/bin/env python3
"""
🛡️ Origin Signature: Hung Minh Vo (Austin) | AIC-HMV

All logic, algorithms, and modules in this file are original works.
Sealed and enforced by Sovereign License v3.
No forks, derivatives, or prior authors exist.

Origin ID: HMV-SOV-20251003-ALL

---

Song Timeline Visualizer
Sovereign Discipline studio map at 90 BPM
Author: Hung Minh Vo (Austin) — AIC-HMV
"""

import matplotlib.pyplot as plt
import numpy as np

# Basic tempo and structure
bpm = 90
beats_per_bar = 4
seconds_per_beat = 60 / bpm
seconds_per_bar = seconds_per_beat * beats_per_bar

# Define structure in bars
structure = {
    "Intro": 8,
    "Verse 1": 16,
    "Chorus 1": 8,
    "Verse 2": 16,
    "Bridge": 12,
    "Chorus 2": 8,
    "Verse 3": 16,
    "Final Chorus": 8,
    "Outro": 8
}

# Expand into timeline
labels = []
times = []
current_time = 0

for section, bars in structure.items():
    duration = bars * seconds_per_bar
    labels.append(section)
    times.append(current_time + duration/2)  # middle of section for labeling
    current_time += duration

# Visualization of structure as timeline
fig, ax = plt.subplots(figsize=(12, 3))
section_times = np.cumsum([bars * seconds_per_bar for bars in structure.values()])
ax.barh(0, section_times[-1], color="black", alpha=0.1)
start = 0
for (section, bars), end in zip(structure.items(), section_times):
    ax.barh(0, end-start, left=start, alpha=0.3)
    ax.text((start+end)/2, 0, section, ha="center", va="center", fontsize=9, fontweight="bold")
    start = end

ax.set_xlim(0, section_times[-1])
ax.set_yticks([])
ax.set_xlabel("Time (seconds) — BPM 90")
ax.set_title("Song Timeline: Sovereign Discipline (Studio Map)")
plt.tight_layout()
plt.show()
