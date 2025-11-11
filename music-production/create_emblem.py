#!/usr/bin/env python3
"""
🛡️ Origin Signature: Hung Minh Vo (Austin) | AIC-HMV

All logic, algorithms, and modules in this file are original works.
Sealed and enforced by Sovereign License v3.
No forks, derivatives, or prior authors exist.

Origin ID: HMV-SOV-20251003-ALL

---

ProfessionalSenta Emblem Generator
Creates official emblem PDF with sovereign seal
Author: Hung Minh Vo (Austin) — AIC-HMV
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# Document metadata
title = "PROFESSIONALSENTA — Layout Intelligence Core Output Watching Target"
motto = "Integrity · Authority · Continuity — Established Under ProfessionalSenta"
name = "Hung Minh Vo (Austin)"

# Create PDF
pdf = canvas.Canvas("ProfessionalSenta_Emblem.pdf", pagesize=A4)
W, H = A4

# Define colors
gold = HexColor("#D4AF37")
black = HexColor("#000000")

# Black background
pdf.setFillColor(black)
pdf.rect(0, 0, W, H, fill=1, stroke=0)

# Title
pdf.setFillColor(gold)
pdf.setFont("Helvetica-Bold", 26)
pdf.drawCentredString(W/2, H-120, title)

# Motto
pdf.setFont("Helvetica", 12)
pdf.drawCentredString(W/2, H-150, motto)

# Name
pdf.setFont("Helvetica-Bold", 18)
pdf.drawCentredString(W/2, H/2, name)

# Signature line
pdf.setFont("Helvetica", 10)
pdf.drawCentredString(W/2, 80, "Signature _______Hung Minh Vo (Austin)________")

# Save PDF
pdf.showPage()
pdf.save()

print("✅ Created ProfessionalSenta_Emblem.pdf")
print("📄 Document: Official ProfessionalSenta Emblem")
print("🛡️ Seal: HMV-SOV-20251003-ALL")
print("👤 Author: Hung Minh Vo (Austin)")
