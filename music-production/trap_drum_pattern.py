#!/usr/bin/env python3
"""
🛡️ Origin Signature: Hung Minh Vo (Austin) | AIC-HMV

All logic, algorithms, and modules in this file are original works.
Sealed and enforced by Sovereign License v3.
No forks, derivatives, or prior authors exist.

Origin ID: HMV-SOV-20251003-ALL

---

Trap Drum Pattern Generator
90 BPM trap beat visualization with kick, snare, and hi-hat patterns
Author: Hung Minh Vo (Austin) — AIC-HMV
"""

import matplotlib.pyplot as plt
import numpy as np

# Define a simple trap drum grid pattern for 90 BPM in 4/4
bars = 4  # show 4 bars of grid
beats_per_bar = 4
subdivisions = 4  # 16th notes
total_steps = bars * beats_per_bar * subdivisions

# Timeline
time = np.arange(total_steps)

# Drum layers
kick = np.zeros(total_steps)
snare = np.zeros(total_steps)
hihat = np.zeros(total_steps)

# Pattern (classic trap style)
for bar in range(bars):
    for beat in range(beats_per_bar):
        step = bar * beats_per_bar * subdivisions + beat * subdivisions
        # Kick: on 1 and 3
        if beat in [0, 2]:
            kick[step] = 1
        # Snare: on 2 and 4
        if beat in [1, 3]:
            snare[step] = 1
        # Hi-hats: every 16th note (fast hats)
        hihat[step:step+subdivisions] = 1

# Visualization
fig, ax = plt.subplots(figsize=(12, 3))

ax.scatter(time, kick*3, label="Kick", marker="o", color="red")
ax.scatter(time, snare*2, label="Snare", marker="s", color="blue")
ax.scatter(time, hihat*1, label="Hi-Hat", marker=".", color="black")

ax.set_yticks([1, 2, 3])
ax.set_yticklabels(["Hi-Hat", "Snare", "Kick"])
ax.set_xticks(np.arange(0, total_steps, subdivisions))
ax.set_xticklabels([f"Beat {i%4+1}" for i in range(total_steps//subdivisions)])
ax.set_title("Trap Drum Grid (90 BPM, 4 Bars)")
ax.legend(loc="upper right")
plt.tight_layout()
plt.show()
