# -*- coding: utf-8 -*-
"""
Created on Fri May  8 03:44:06 2026

@author: shrn1
"""

import streamlit as st

def show():
    st.title("📐 Formula Reference")
    st.markdown("*Complete formula cheat sheet for lab chemists & students*")
    st.markdown("---")

    # ── Search ─────────────────────────────────────────────────────────────
    search = st.text_input("🔍 Search formulas...",
                           placeholder="e.g. molarity, pH, Beer-Lambert...")
    st.markdown("---")

    # ── Formula Database ───────────────────────────────────────────────────
    sections = {

        "🧪 Solution Concentration": [
            {
                "name": "Molarity (M)",
                "formula": "M = n / V = mass / (MW × V)",
                "units": "mol/L",
                "variables": {
                    "M": "Molarity (mol/L)",
                    "n": "moles of solute (mol)",
                    "V": "volume of solution (L)",
                    "mass": "mass of solute (g)",
                    "MW": "molecular weight (g/mol)"
                },
                "example": "Dissolve 4.00 g NaOH (MW=40) in 1L → M = 4/40 = 0.1 mol/L",
                "tip": "Always measure final volume, not volume of solvent added!"
            },
            {
                "name": "Molality (m)",
                "formula": "m = n / kg(solvent)",
                "units": "mol/kg",
                "variables": {
                    "m": "molality (mol/kg)",
                    "n": "moles of solute (mol)",
                    "kg(solvent)": "mass of solvent in kg"
                },
                "example": "1 mol NaCl in 1 kg water → m = 1 mol/kg",
                "tip": "Molality doesn't change with temperature — useful for colligative properties!"
            },
            {
                "name": "Normality (N)",
                "formula": "N = M × n-factor",
                "units": "eq/L",
                "variables": {
                    "N": "Normality (equivalents/L)",
                    "M": "Molarity (mol/L)",
                    "n-factor": "number of equivalents per mole"
                },
                "example": "1M H₂SO₄ → N = 1 × 2 = 2N (n-factor=2 for 2 H⁺)",
                "tip": "n-factor = H⁺ for acids | OH⁻ for bases | electrons for redox"
            },
            {
                "name": "% w/v",
                "formula": "% w/v = (mass of solute / volume of solution) × 100",
                "units": "g/100mL",
                "variables": {
                    "mass": "mass of solute (g)",
                    "volume": "volume of solution (mL)"
                },
                "example": "5g NaCl in 100mL → 5% w/v",
                "tip": "Most common for solid-in-liquid solutions in lab"
            },
            {
                "name": "% w/w",
                "formula": "% w/w = (mass of solute / mass of solution) × 100",
                "units": "g/100g",
                "variables": {
                    "mass of solute": "grams of solute",
                    "mass of solution": "total grams of solution"
                },
                "example": "5g NaCl in 95g water → 5% w/w",
                "tip": "Used for concentrated acids (e.g. HCl 37% w/w)"
            },
            {
                "name": "% v/v",
                "formula": "% v/v = (volume of solute / volume of solution) × 100",
                "units": "mL/100mL",
                "variables": {
                    "volume of solute": "mL of liquid solute",
                    "volume of solution": "total mL of solution"
                },
                "example": "5mL ethanol in 100mL → 5% v/v",
                "tip": "Used for liquid-in-liquid mixtures like alcohol solutions"
            },
            {
                "name": "ppm / ppb / ppt",
                "formula": "ppm = mg/L | ppb = µg/L | ppt = ng/L",
                "units": "mg/L, µg/L, ng/L",
                "variables": {
                    "ppm": "parts per million = mg/L (aqueous)",
                    "ppb": "parts per billion = µg/L (aqueous)",
                    "ppt": "parts per trillion = ng/L (aqueous)"
                },
                "example": "1 ppm = 1 mg/L | 1 ppb = 1 µg/L | 1 ppt = 1 ng/L",
                "tip": "1 ppm = 1000 ppb = 1,000,000 ppt. Valid for dilute aqueous solutions where density ≈ 1 g/mL"
            },
        ],

        "💧 Dilution": [
            {
                "name": "Simple Dilution",
                "formula": "C₁V₁ = C₂V₂",
                "units": "any consistent units",
                "variables": {
                    "C₁": "initial concentration (stock)",
                    "V₁": "volume taken from stock",
                    "C₂": "final concentration",
                    "V₂": "final total volume"
                },
                "example": "5M HCl, want 0.1M in 100mL → V₁ = (0.1×100)/5 = 2mL",
                "tip": "Units of C must match. Units of V must match. Mix them and you'll get wrong answers!"
            },
            {
                "name": "Serial Dilution",
                "formula": "Cₙ = C₀ / (DF)ⁿ",
                "units": "same as starting concentration",
                "variables": {
                    "Cₙ": "concentration at step n",
                    "C₀": "starting concentration",
                    "DF": "dilution factor (e.g. 10)",
                    "n": "step number"
                },
                "example": "1M, DF=10, step 3 → C₃ = 1/10³ = 0.001M",
                "tip": "Transfer volume = Total volume / DF. Always mix before each transfer!"
            },
            {
                "name": "Dilution Factor",
                "formula": "DF = C₁ / C₂ = V₂ / V₁",
                "units": "dimensionless",
                "variables": {
                    "DF": "dilution factor",
                    "C₁": "stock concentration",
                    "C₂": "final concentration",
                    "V₁": "volume of stock taken",
                    "V₂": "final total volume"
                },
                "example": "5M → 0.1M: DF = 5/0.1 = 50x dilution",
                "tip": "DF = 10 means 1:10 dilution. Higher DF = more dilute solution"
            },
        ],

        "🔢 Moles": [
            {
                "name": "Moles from Mass",
                "formula": "n = m / MW",
                "units": "mol",
                "variables": {
                    "n": "moles (mol)",
                    "m": "mass (g)",
                    "MW": "molecular weight (g/mol)"
                },
                "example": "5.85g NaCl (MW=58.5) → n = 5.85/58.5 = 0.1 mol",
                "tip": "MW is the sum of atomic weights of all atoms in the formula"
            },
            {
                "name": "Moles from Solution",
                "formula": "n = M × V",
                "units": "mol",
                "variables": {
                    "n": "moles (mol)",
                    "M": "molarity (mol/L)",
                    "V": "volume (L)"
                },
                "example": "0.5M NaOH, 250mL → n = 0.5 × 0.25 = 0.125 mol",
                "tip": "Always convert volume to Litres before calculating!"
            },
            {
                "name": "Moles from Gas at STP",
                "formula": "n = V / 22.4",
                "units": "mol",
                "variables": {
                    "n": "moles (mol)",
                    "V": "volume of gas (L)",
                    "22.4": "molar volume at STP (L/mol)"
                },
                "example": "44.8L CO₂ at STP → n = 44.8/22.4 = 2 mol",
                "tip": "STP = 0°C, 1 atm. At SATP (25°C, 1 bar), use 24.8 L/mol instead"
            },
            {
                "name": "Moles from Molecules",
                "formula": "n = N / Nₐ",
                "units": "mol",
                "variables": {
                    "n": "moles (mol)",
                    "N": "number of molecules",
                    "Nₐ": "Avogadro's number = 6.022 × 10²³ mol⁻¹"
                },
                "example": "6.022×10²³ molecules → n = 1 mol",
                "tip": "Avogadro's number applies to atoms, molecules, ions — any particles!"
            },
        ],

        "🧮 Buffer Chemistry": [
            {
                "name": "Henderson-Hasselbalch",
                "formula": "pH = pKa + log([A⁻]/[HA])",
                "units": "pH (dimensionless)",
                "variables": {
                    "pH": "desired pH",
                    "pKa": "acid dissociation constant",
                    "[A⁻]": "concentration of conjugate base",
                    "[HA]": "concentration of weak acid"
                },
                "example": "Acetate buffer: pH=5, pKa=4.76 → ratio=10^(5-4.76)=1.74",
                "tip": "Best buffering occurs within ±1 pH unit of pKa"
            },
            {
                "name": "Buffer Ratio",
                "formula": "[A⁻]/[HA] = 10^(pH - pKa)",
                "units": "dimensionless",
                "variables": {
                    "[A⁻]/[HA]": "base to acid ratio",
                    "pH": "desired pH",
                    "pKa": "dissociation constant"
                },
                "example": "pH=7.4, pKa=7.2 → ratio = 10^0.2 = 1.58",
                "tip": "Ratio >10 or <0.1 means you're outside effective buffer range!"
            },
            {
                "name": "pKa and pKb",
                "formula": "pKa + pKb = 14 (at 25°C)",
                "units": "dimensionless",
                "variables": {
                    "pKa": "acid dissociation constant",
                    "pKb": "base dissociation constant"
                },
                "example": "NH₃: pKb=4.74 → pKa=14-4.74=9.26",
                "tip": "Lower pKa = stronger acid. pKa changes with temperature!"
            },
        ],

        "📊 Analytical Chemistry": [
            {
                "name": "Beer-Lambert Law",
                "formula": "A = ε × c × l",
                "units": "A (absorbance, dimensionless)",
                "variables": {
                    "A": "absorbance (no units)",
                    "ε": "molar absorptivity (L/mol·cm)",
                    "c": "concentration (mol/L)",
                    "l": "path length (cm)"
                },
                "example": "ε=5000, c=0.001M, l=1cm → A = 5000×0.001×1 = 5.0",
                "tip": "Beer-Lambert is linear only for A between 0.1 and 1.0. Outside this range, dilute your sample!"
            },
            {
                "name": "Transmittance & Absorbance",
                "formula": "A = -log(T) = log(I₀/I)",
                "units": "dimensionless",
                "variables": {
                    "A": "absorbance",
                    "T": "transmittance (0 to 1)",
                    "I₀": "incident light intensity",
                    "I": "transmitted light intensity"
                },
                "example": "T=0.01 → A = -log(0.01) = 2",
                "tip": "T=1 means no absorption. T=0 means complete absorption"
            },
            {
                "name": "% Transmittance",
                "formula": "A = 2 - log(%T)",
                "units": "dimensionless",
                "variables": {
                    "A": "absorbance",
                    "%T": "percent transmittance (0-100)"
                },
                "example": "%T=50 → A = 2-log(50) = 0.301",
                "tip": "Many old spectrophotometers show %T — use this formula to convert!"
            },
            {
                "name": "Calibration Curve",
                "formula": "y = mx + b  →  c = (A - b) / m",
                "units": "concentration units",
                "variables": {
                    "y/A": "absorbance (measured)",
                    "m": "slope of calibration line",
                    "x/c": "concentration (unknown)",
                    "b": "y-intercept"
                },
                "example": "slope=0.5, intercept=0.02, A=0.52 → c=(0.52-0.02)/0.5=1.0 mg/L",
                "tip": "Always run at least 5 standards. R² should be >0.999 for good calibration!"
            },
        ],

        "⚗️ Liquid Chemical Preparation": [
            {
                "name": "Volume of Liquid Chemical Needed",
                "formula": "V = (M × MW × Vf) / (density × purity/100)",
                "units": "mL",
                "variables": {
                    "V": "volume of liquid chemical (mL)",
                    "M": "desired molarity (mol/L)",
                    "MW": "molecular weight (g/mol)",
                    "Vf": "final solution volume (L)",
                    "density": "density of liquid chemical (g/mL)",
                    "purity": "assay % (e.g. 37 for 37%)"
                },
                "example": "1M HCl, 100mL: V=(1×36.46×0.1)/(1.19×0.37)=8.27mL",
                "tip": "Always add acid to water — never water to acid!"
            },
            {
                "name": "Molarity of Concentrated Acid",
                "formula": "M = (density × purity × 1000) / MW",
                "units": "mol/L",
                "variables": {
                    "M": "molarity (mol/L)",
                    "density": "density (g/mL)",
                    "purity": "assay fraction (e.g. 0.37)",
                    "MW": "molecular weight (g/mol)"
                },
                "example": "Conc. HCl: M=(1.19×0.37×1000)/36.46=12.08 mol/L",
                "tip": "Use this to find stock concentration when it's not stated on the label!"
            },
        ],

        "🌡️ Physical Chemistry": [
            {
                "name": "Ideal Gas Law",
                "formula": "PV = nRT",
                "units": "various",
                "variables": {
                    "P": "pressure (atm)",
                    "V": "volume (L)",
                    "n": "moles (mol)",
                    "R": "gas constant = 0.08206 L·atm/mol·K",
                    "T": "temperature (K)"
                },
                "example": "1 mol gas at 25°C, 1atm → V=nRT/P=1×0.08206×298/1=24.5L",
                "tip": "Always use Kelvin for temperature! T(K) = T(°C) + 273.15"
            },
            {
                "name": "pH and pOH",
                "formula": "pH = -log[H⁺]  |  pOH = -log[OH⁻]  |  pH + pOH = 14",
                "units": "dimensionless",
                "variables": {
                    "pH": "hydrogen ion activity",
                    "pOH": "hydroxide ion activity",
                    "[H⁺]": "hydrogen ion concentration (mol/L)",
                    "[OH⁻]": "hydroxide ion concentration (mol/L)"
                },
                "example": "[H⁺]=0.001M → pH=-log(0.001)=3",
                "tip": "pH<7 acidic | pH=7 neutral | pH>7 basic (at 25°C)"
            },
            {
                "name": "Nernst Equation",
                "formula": "E = E° - (RT/nF) × ln(Q)",
                "units": "Volts (V)",
                "variables": {
                    "E": "cell potential (V)",
                    "E°": "standard cell potential (V)",
                    "R": "gas constant = 8.314 J/mol·K",
                    "T": "temperature (K)",
                    "n": "moles of electrons transferred",
                    "F": "Faraday constant = 96485 C/mol",
                    "Q": "reaction quotient"
                },
                "example": "At 25°C: E = E° - (0.0592/n) × log(Q)",
                "tip": "At 25°C simplifies to E = E° - (0.0592/n) × log(Q)"
            },
        ],
    }

    # ── Render Sections ────────────────────────────────────────────────────
    for section_name, formulas in sections.items():

        # Filter by search
        if search:
            formulas = [f for f in formulas if
                       search.lower() in f["name"].lower() or
                       search.lower() in f["formula"].lower() or
                       search.lower() in str(f["variables"]).lower() or
                       search.lower() in f["example"].lower()]
            if not formulas:
                continue

        st.markdown(f"## {section_name}")

        for formula in formulas:
            with st.expander(f"📌 {formula['name']}  —  `{formula['formula']}`"):

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**📐 Formula:**")
                    st.code(formula["formula"])

                    st.markdown("**📦 Variables:**")
                    for var, desc in formula["variables"].items():
                        st.markdown(f"- **{var}** = {desc}")

                with col2:
                    st.markdown("**🧪 Example:**")
                    st.info(formula["example"])

                    st.markdown("**💡 Tip:**")
                    st.success(formula["tip"])

                    st.markdown(f"**📏 Units:** `{formula['units']}`")

        st.markdown("---")

    # ── No Results ─────────────────────────────────────────────────────────
    if search and not any(
        search.lower() in f["name"].lower() or
        search.lower() in f["formula"].lower()
        for formulas in sections.values()
        for f in formulas
    ):
        st.warning(f"No formulas found for '{search}'. Try a different keyword!")