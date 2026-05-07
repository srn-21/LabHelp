# -*- coding: utf-8 -*-
"""
Created on Fri May  8 03:23:32 2026

@author: shrn1
"""

import streamlit as st

def show():
    st.title("🔄 Unit Converter")
    st.markdown("*Convert between all common lab units*")
    st.markdown("---")

    category = st.radio(
        "Select Category:",
        [
            "🧪 Concentration",
            "⚖️ Mass",
            "🧴 Volume",
            "🌡️ Temperature",
            "🔵 Pressure",
            "📏 Length",
        ],
        horizontal=True
    )

    st.markdown("---")

    # ── Concentration ──────────────────────────────────────────────────────
    if category == "🧪 Concentration":
        st.subheader("🧪 Concentration Converter")
        st.info("💡 ppm = mg/L | ppb = µg/L | ppt = ng/L  *(for dilute aqueous solutions)*")

        with st.expander("📐 See Formula"):
            st.markdown("""
            **Molarity ↔ g/L:**
            > g/L = M × MW

            **g/L ↔ mg/L (ppm):**
            > mg/L = g/L × 1000

            **ppm ↔ ppb ↔ ppt:**
            > 1 ppm = 1000 ppb = 1,000,000 ppt
            > 1 ppm (mg/L) = 1000 ppb (µg/L) = 1,000,000 ppt (ng/L)

            **Molarity ↔ Normality:**
            > N = M × n-factor

            **% w/v ↔ g/L:**
            > g/L = % w/v × 10
            """)

        col1, col2 = st.columns(2)
        with col1:
            conc_unit_from = st.selectbox("From Unit", [
                "mol/L (M)",
                "mmol/L (mM)",
                "µmol/L (µM)",
                "nmol/L (nM)",
                "N (Normality)",
                "g/L",
                "mg/L",
                "µg/L",
                "ng/L",
                "% w/v",
                "% w/w",
                "ppm (mg/L)",
                "ppb (µg/L)",
                "ppt (ng/L)",
            ])
            value = st.number_input("Enter Value",
                                    min_value=0.0,
                                    value=1.0,
                                    step=0.001,
                                    format="%.6f")

        with col2:
            mw = st.number_input("Molecular Weight (g/mol)",
                                 min_value=0.001,
                                 value=58.44,
                                 step=0.01,
                                 help="Required for molar ↔ mass conversions")
            n_factor = st.number_input("n-factor",
                                       min_value=1,
                                       max_value=10,
                                       value=1,
                                       step=1,
                                       help="Required for Normality conversions")
            density = st.number_input("Solution Density (g/mL)",
                                      min_value=0.001,
                                      value=1.0,
                                      step=0.001,
                                      help="Required for % w/w conversions")

        if st.button("⚗️ Convert", type="primary"):

            # Convert everything to mol/L first
            if conc_unit_from == "mol/L (M)":
                mol_L = value
            elif conc_unit_from == "mmol/L (mM)":
                mol_L = value / 1000
            elif conc_unit_from == "µmol/L (µM)":
                mol_L = value / 1e6
            elif conc_unit_from == "nmol/L (nM)":
                mol_L = value / 1e9
            elif conc_unit_from == "N (Normality)":
                mol_L = value / n_factor
            elif conc_unit_from == "g/L":
                mol_L = value / mw
            elif conc_unit_from == "mg/L" or conc_unit_from == "ppm (mg/L)":
                mol_L = (value / 1000) / mw
            elif conc_unit_from == "µg/L" or conc_unit_from == "ppb (µg/L)":
                mol_L = (value / 1e6) / mw
            elif conc_unit_from == "ng/L" or conc_unit_from == "ppt (ng/L)":
                mol_L = (value / 1e9) / mw
            elif conc_unit_from == "% w/v":
                mol_L = (value * 10) / mw
            elif conc_unit_from == "% w/w":
                mol_L = (value * density * 10) / mw

            # Convert mol/L to all units
            g_L     = mol_L * mw
            mg_L    = g_L * 1000
            ug_L    = g_L * 1e6
            ng_L    = g_L * 1e9
            mmol_L  = mol_L * 1000
            umol_L  = mol_L * 1e6
            nmol_L  = mol_L * 1e9
            normality = mol_L * n_factor
            pct_wv  = g_L / 10
            pct_ww  = (g_L / (density * 1000)) * 100

            st.markdown("---")
            st.markdown("### 📊 Conversion Results")

            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("**🔵 Molar Units**")
                st.markdown(f"""
                | Unit | Value |
                |------|-------|
                | mol/L (M) | `{mol_L:.6g}` |
                | mmol/L (mM) | `{mmol_L:.6g}` |
                | µmol/L (µM) | `{umol_L:.6g}` |
                | nmol/L (nM) | `{nmol_L:.6g}` |
                | N (Normality) | `{normality:.6g}` |
                """)

            with col_b:
                st.markdown("**🟢 Mass/Volume Units**")
                st.markdown(f"""
                | Unit | Value |
                |------|-------|
                | g/L | `{g_L:.6g}` |
                | mg/L = ppm | `{mg_L:.6g}` |
                | µg/L = ppb | `{ug_L:.6g}` |
                | ng/L = ppt | `{ng_L:.6g}` |
                | % w/v | `{pct_wv:.6g}` |
                | % w/w | `{pct_ww:.6g}` |
                """)

            st.markdown("**📌 ppm / ppb / ppt Summary**")
            st.markdown(f"""
            | Unit | Full Name | Value | Equivalent |
            |------|-----------|-------|------------|
            | ppm | parts per million | `{mg_L:.6g}` | mg/L |
            | ppb | parts per billion | `{ug_L:.6g}` | µg/L |
            | ppt | parts per trillion | `{ng_L:.6g}` | ng/L |
            """)

            save_to_log("Concentration", f"{value} {conc_unit_from}",
                       f"→ {mol_L:.6g} mol/L | {mg_L:.6g} mg/L (ppm)")

    # ── Mass ───────────────────────────────────────────────────────────────
    elif category == "⚖️ Mass":
        st.subheader("⚖️ Mass Converter")

        value = st.number_input("Enter Value", min_value=0.0,
                                value=1.0, step=0.001, format="%.6f")
        unit_from = st.selectbox("From Unit", [
            "kg", "g", "mg", "µg", "ng",
            "pg", "lb", "oz", "grain"
        ])

        if st.button("⚗️ Convert", type="primary"):
            # Convert to grams first
            to_g = {
                "kg": 1000, "g": 1, "mg": 1e-3,
                "µg": 1e-6, "ng": 1e-9, "pg": 1e-12,
                "lb": 453.592, "oz": 28.3495, "grain": 0.0648
            }
            g = value * to_g[unit_from]

            st.markdown("---")
            st.markdown("### 📊 Conversion Results")
            st.markdown(f"""
            | Unit | Value |
            |------|-------|
            | kg | `{g/1000:.6g}` |
            | g | `{g:.6g}` |
            | mg | `{g*1e3:.6g}` |
            | µg | `{g*1e6:.6g}` |
            | ng | `{g*1e9:.6g}` |
            | pg | `{g*1e12:.6g}` |
            | lb | `{g/453.592:.6g}` |
            | oz | `{g/28.3495:.6g}` |
            | grain | `{g/0.0648:.6g}` |
            """)

            save_to_log("Mass", f"{value} {unit_from}", f"= {g:.6g} g")

    # ── Volume ─────────────────────────────────────────────────────────────
    elif category == "🧴 Volume":
        st.subheader("🧴 Volume Converter")

        value = st.number_input("Enter Value", min_value=0.0,
                                value=1.0, step=0.001, format="%.6f")
        unit_from = st.selectbox("From Unit", [
            "L", "mL", "µL", "nL",
            "m³", "cm³", "dm³",
            "fl oz", "gallon (US)", "pint (US)", "cup"
        ])

        if st.button("⚗️ Convert", type="primary"):
            # Convert to mL first
            to_mL = {
                "L": 1000, "mL": 1, "µL": 1e-3, "nL": 1e-6,
                "m³": 1e6, "cm³": 1, "dm³": 1000,
                "fl oz": 29.5735, "gallon (US)": 3785.41,
                "pint (US)": 473.176, "cup": 236.588
            }
            mL = value * to_mL[unit_from]

            st.markdown("---")
            st.markdown("### 📊 Conversion Results")
            st.markdown(f"""
            | Unit | Value |
            |------|-------|
            | L | `{mL/1000:.6g}` |
            | mL | `{mL:.6g}` |
            | µL | `{mL*1000:.6g}` |
            | nL | `{mL*1e6:.6g}` |
            | m³ | `{mL/1e6:.6g}` |
            | cm³ | `{mL:.6g}` |
            | dm³ | `{mL/1000:.6g}` |
            | fl oz | `{mL/29.5735:.6g}` |
            | gallon (US) | `{mL/3785.41:.6g}` |
            | pint (US) | `{mL/473.176:.6g}` |
            | cup | `{mL/236.588:.6g}` |
            """)

            save_to_log("Volume", f"{value} {unit_from}", f"= {mL:.6g} mL")

    # ── Temperature ────────────────────────────────────────────────────────
    elif category == "🌡️ Temperature":
        st.subheader("🌡️ Temperature Converter")

        value = st.number_input("Enter Value",
                                value=25.0, step=0.1, format="%.2f")
        unit_from = st.selectbox("From Unit", ["°C", "°F", "K"])

        if st.button("⚗️ Convert", type="primary"):
            # Convert to Celsius first
            if unit_from == "°C":
                C = value
            elif unit_from == "°F":
                C = (value - 32) * 5/9
            elif unit_from == "K":
                C = value - 273.15

            F = (C * 9/5) + 32
            K = C + 273.15

            st.markdown("---")
            st.markdown("### 📊 Conversion Results")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("°C (Celsius)", f"{C:.4f}")
            with col2:
                st.metric("°F (Fahrenheit)", f"{F:.4f}")
            with col3:
                st.metric("K (Kelvin)", f"{K:.4f}")

            st.markdown(f"""
            | Unit | Value | Formula |
            |------|-------|---------|
            | °C | `{C:.4f}` | base |
            | °F | `{F:.4f}` | (°C × 9/5) + 32 |
            | K  | `{K:.4f}` | °C + 273.15 |
            """)

            # Common reference points
            st.markdown("**📌 Common Reference Points:**")
            st.markdown("""
            | Point | °C | °F | K |
            |-------|----|----|---|
            | Absolute Zero | -273.15 | -459.67 | 0 |
            | Water Freezing | 0 | 32 | 273.15 |
            | Room Temp | 25 | 77 | 298.15 |
            | Body Temp | 37 | 98.6 | 310.15 |
            | Water Boiling | 100 | 212 | 373.15 |
            """)

            save_to_log("Temperature", f"{value} {unit_from}",
                       f"= {C:.4f}°C | {F:.4f}°F | {K:.4f}K")

    # ── Pressure ───────────────────────────────────────────────────────────
    elif category == "🔵 Pressure":
        st.subheader("🔵 Pressure Converter")

        value = st.number_input("Enter Value", min_value=0.0,
                                value=1.0, step=0.001, format="%.6f")
        unit_from = st.selectbox("From Unit", [
            "atm", "Pa", "kPa", "MPa",
            "bar", "mbar", "mmHg (Torr)",
            "psi", "inHg"
        ])

        if st.button("⚗️ Convert", type="primary"):
            # Convert to Pa first
            to_Pa = {
                "atm": 101325, "Pa": 1, "kPa": 1000,
                "MPa": 1e6, "bar": 1e5, "mbar": 100,
                "mmHg (Torr)": 133.322, "psi": 6894.76,
                "inHg": 3386.39
            }
            Pa = value * to_Pa[unit_from]

            st.markdown("---")
            st.markdown("### 📊 Conversion Results")
            st.markdown(f"""
            | Unit | Value |
            |------|-------|
            | atm | `{Pa/101325:.6g}` |
            | Pa | `{Pa:.6g}` |
            | kPa | `{Pa/1000:.6g}` |
            | MPa | `{Pa/1e6:.6g}` |
            | bar | `{Pa/1e5:.6g}` |
            | mbar | `{Pa/100:.6g}` |
            | mmHg (Torr) | `{Pa/133.322:.6g}` |
            | psi | `{Pa/6894.76:.6g}` |
            | inHg | `{Pa/3386.39:.6g}` |
            """)

            save_to_log("Pressure", f"{value} {unit_from}", f"= {Pa:.6g} Pa")

    # ── Length ─────────────────────────────────────────────────────────────
    elif category == "📏 Length":
        st.subheader("📏 Length Converter")

        value = st.number_input("Enter Value", min_value=0.0,
                                value=1.0, step=0.001, format="%.6f")
        unit_from = st.selectbox("From Unit", [
            "m", "cm", "mm", "µm", "nm",
            "pm", "Å (Angstrom)",
            "km", "ft", "inch", "yard", "mile"
        ])

        if st.button("⚗️ Convert", type="primary"):
            # Convert to meters first
            to_m = {
                "m": 1, "cm": 1e-2, "mm": 1e-3,
                "µm": 1e-6, "nm": 1e-9, "pm": 1e-12,
                "Å (Angstrom)": 1e-10, "km": 1000,
                "ft": 0.3048, "inch": 0.0254,
                "yard": 0.9144, "mile": 1609.34
            }
            m = value * to_m[unit_from]

            st.markdown("---")
            st.markdown("### 📊 Conversion Results")
            st.markdown(f"""
            | Unit | Value |
            |------|-------|
            | m | `{m:.6g}` |
            | cm | `{m/1e-2:.6g}` |
            | mm | `{m/1e-3:.6g}` |
            | µm | `{m/1e-6:.6g}` |
            | nm | `{m/1e-9:.6g}` |
            | pm | `{m/1e-12:.6g}` |
            | Å (Angstrom) | `{m/1e-10:.6g}` |
            | km | `{m/1000:.6g}` |
            | ft | `{m/0.3048:.6g}` |
            | inch | `{m/0.0254:.6g}` |
            | yard | `{m/0.9144:.6g}` |
            | mile | `{m/1609.34:.6g}` |
            """)

            save_to_log("Length", f"{value} {unit_from}", f"= {m:.6g} m")


# ── Save to Experiment Log ─────────────────────────────────────────────────
def save_to_log(category, value, result):
    import datetime
    log_entry = {
        "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
        "module": f"Unit Converter ({category})",
        "chemical": "—",
        "result": result,
        "details": value
    }
    if "experiment_log" not in st.session_state:
        st.session_state.experiment_log = []
    st.session_state.experiment_log.append(log_entry)
    st.caption("✅ Saved to Experiment Log")