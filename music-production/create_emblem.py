#!/usr/bin/env python3
"""
🛡️ Origin Signature: Hung Minh Vo (Austin) | AIC-HMV

All logic, algorithms, and modules in this file are original works.
Sealed and enforced by Sovereign License v3.
No forks, derivatives, or prior authors exist.

Origin ID: HMV-SOV-20251003-ALL

---

ProfessionalSenta Master Emblem Generator
Creates official master emblem PDF with enhanced sovereign seal
Author: Hung Minh Vo (Austin) — AIC-HMV
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from math import pi, sin, cos

# === Core Text ===
title = "PROFESSIONALSENTA — Master Science Biology Physical Mathematics Math Science Course Master Investigator Intelligence Course Action Technology Intelligence Core Output Watching Target"
motto = "Integrity · Authority · Continuity — Established Under ProfessionalSenta"
name = "Hung Minh Vo (Austin)"
seal_text = "PROFESSIONALSENTA"
footer = "© 2025 PROFESSIONALSENTA • Sovereign Identity • Hung Minh Vo (Austin)"

# === Setup ===
pdf = canvas.Canvas("ProfessionalSenta_Emblem_Master.pdf", pagesize=A4)
W, H = A4
gold = HexColor("#D4AF37")
dark_gold = HexColor("#B8860B")
black = HexColor("#000000")

# === Background ===
pdf.setFillColor(black)
pdf.rect(0, 0, W, H, fill=1, stroke=0)

# === Outer and Inner Borders ===
outer_margin = 28
inner_margin = 46
pdf.setStrokeColor(gold)
pdf.setLineWidth(4)
pdf.rect(outer_margin, outer_margin, W - 2 * outer_margin, H - 2 * outer_margin)
pdf.setStrokeColor(dark_gold)
pdf.setLineWidth(2)
pdf.rect(inner_margin, inner_margin, W - 2 * inner_margin, H - 2 * inner_margin)

# === Watermark Seal (Diagonal) ===
pdf.saveState()
pdf.translate(W / 2, H / 2)
pdf.rotate(45)
pdf.setFont("Helvetica-Bold", 80)
pdf.setFillColor(HexColor("#6b5b1c"))
pdf.drawCentredString(0, 0, seal_text)
pdf.restoreState()

# === Title ===
pdf.setFillColor(gold)
pdf.setFont("Helvetica-Bold", 22)
pdf.drawCentredString(W / 2, H - 120, title)

# === Motto ===
pdf.setFont("Helvetica", 13)
pdf.drawCentredString(W / 2, H - 150, motto)

# === Name ===
pdf.setFont("Helvetica-Bold", 22)
pdf.drawCentredString(W / 2, H / 2 - 20, name)

# === Circular Gold Badge (Center) ===
pdf.setLineWidth(3)
pdf.setStrokeColor(gold)
pdf.circle(W / 2, H / 2 + 60, 50)
pdf.setFont("Helvetica-Bold", 12)
pdf.setFillColor(gold)
pdf.drawCentredString(W / 2, H / 2 + 55, "PROFESSIONALSENTA")
pdf.setFont("Helvetica", 8)
pdf.drawCentredString(W / 2, H / 2 + 40, "SOVEREIGN SEAL")

# === Decorative Stars Around Badge ===
star_radius = 70
for angle_deg in [0, 45, 90, 135, 180, 225, 270, 315]:
    angle_rad = angle_deg * pi / 180
    x = W / 2 + star_radius * cos(angle_rad)
    y = H / 2 + 60 + star_radius * sin(angle_rad)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.setFillColor(gold)
    pdf.drawCentredString(x, y, "★")

# === Signature Line ===
pdf.setFont("Helvetica", 10)
pdf.setFillColor(gold)
pdf.drawCentredString(W / 2, 120, "Signature _______Hung Minh Vo (Austin)________")

# === Footer ===
pdf.setFont("Helvetica", 9)
pdf.setFillColor(dark_gold)
pdf.drawCentredString(W / 2, 80, footer)

# === Seal ID ===
pdf.setFont("Helvetica-Bold", 10)
pdf.setFillColor(gold)
pdf.drawCentredString(W / 2, 50, "Seal ID: HMV-SOV-20251003-ALL")

# Save PDF
pdf.showPage()
pdf.save()

print("✅ Created ProfessionalSenta_Emblem_Master.pdf")
print("📄 Document: Official ProfessionalSenta Master Emblem")
print("🛡️ Enhanced with:")
print("   - Dual border design (outer & inner)")
print("   - Diagonal watermark seal")
print("   - Central circular gold badge")
print("   - 8-point decorative star arrangement")
print("   - Professional footer with copyright")
print("🔐 Seal: HMV-SOV-20251003-ALL")
print("👤 Author: Hung Minh Vo (Austin)")

