# -*- coding: utf-8 -*-
"""
Created on Fri May  8 03:15:21 2026

@author: shrn1
"""

import streamlit as st

def show():
    st.title("🔢 Moles Calculator")
    st.markdown("*Calculate moles from mass, solution, gas or molecules*")
    st.markdown("---")

    method = st.radio(
        "Calculate moles from:",
        [
            "⚖️ Mass of substance",
            "🧪 Volume of solution",
            "💨 Volume of gas (STP)",
            "🔬 Number of molecules"
        ],
        horizontal=True
    )

    st.markdown("---")

    # ── From Mass ──────────────────────────────────────────────────────────
    if method == "⚖️ Mass of substance":
        st.subheader("⚖️ Moles from Mass")

        with st.expander("📐 See Formula"):
            st.markdown("""
            > n = m / MW

            Where:
            - n  = moles (mol)
            - m  = mass of substance (g)
            - MW = molecular weight (g/mol)
            """)

        col1, col2 = st.columns(2)
        with col1:
            mass_unit = st.selectbox("Mass Unit", ["g", "mg", "kg"])
            mass = st.number_input("Mass", min_value=0.0, value=1.0, step=0.001, format="%.4f")
        with col2:
            mw = st.number_input("Molecular Weight (g/mol)", min_value=0.001, value=58.44, step=0.01)
            st.caption("e.g. NaCl = 58.44, NaOH = 40.00")

        if st.button("⚗️ Calculate", type="primary"):
            # Convert mass to grams
            if mass_unit == "mg":
                mass_g = mass / 1000
            elif mass_unit == "kg":
                mass_g = mass * 1000
            else:
                mass_g = mass

            moles = mass_g / mw

            st.markdown("---")
            st.success(f"🔢 Moles = **{moles:.6f} mol**")

            # Other useful outputs
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("Moles", f"{moles:.6f} mol")
            with col_r2:
                st.metric("Millimoles", f"{moles*1000:.4f} mmol")
            with col_r3:
                st.metric("Molecules", f"{moles * 6.022e23:.4e}")

            with st.expander("🔢 See Calculation Breakdown"):
                st.markdown(f"""
                **Formula:** n = m / MW

                - Mass = {mass} {mass_unit} = **{mass_g:.4f} g**
                - MW   = **{mw} g/mol**

                **n = {mass_g:.4f} / {mw}**
                **n = {moles:.6f} mol**
                """)

            save_to_log("From Mass", f"{moles:.6f} mol",
                       f"mass={mass}{mass_unit}, MW={mw}g/mol")

    # ── From Solution ──────────────────────────────────────────────────────
    elif method == "🧪 Volume of solution":
        st.subheader("🧪 Moles from Solution")

        with st.expander("📐 See Formula"):
            st.markdown("""
            > n = M × V

            Where:
            - n = moles (mol)
            - M = molarity (mol/L)
            - V = volume (L)
            """)

        col1, col2 = st.columns(2)
        with col1:
            molarity = st.number_input("Molarity (mol/L)", min_value=0.0, value=1.0,
                                       step=0.001, format="%.4f")
        with col2:
            vol = st.number_input("Volume", min_value=0.0, value=100.0, step=0.1)
            vol_unit = st.selectbox("Volume Unit", ["mL", "L", "µL"])

        if st.button("⚗️ Calculate", type="primary"):
            # Convert to L
            if vol_unit == "mL":
                V = vol / 1000
            elif vol_unit == "µL":
                V = vol / 1_000_000
            else:
                V = vol

            moles = molarity * V

            st.markdown("---")
            st.success(f"🔢 Moles = **{moles:.6f} mol**")

            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("Moles", f"{moles:.6f} mol")
            with col_r2:
                st.metric("Millimoles", f"{moles*1000:.4f} mmol")
            with col_r3:
                st.metric("Molecules", f"{moles * 6.022e23:.4e}")

            with st.expander("🔢 See Calculation Breakdown"):
                st.markdown(f"""
                **Formula:** n = M × V

                - Molarity = **{molarity} mol/L**
                - Volume   = {vol} {vol_unit} = **{V:.6f} L**

                **n = {molarity} × {V:.6f}**
                **n = {moles:.6f} mol**
                """)

            save_to_log("From Solution", f"{moles:.6f} mol",
                       f"M={molarity}mol/L, V={vol}{vol_unit}")

    # ── From Gas ───────────────────────────────────────────────────────────
    elif method == "💨 Volume of gas (STP)":
        st.subheader("💨 Moles from Gas Volume at STP")

        with st.expander("📐 See Formula"):
            st.markdown("""
            > n = V / 22.4

            At **STP** (Standard Temperature and Pressure):
            - Temperature = 0°C (273.15 K)
            - Pressure    = 1 atm
            - 1 mole of any ideal gas = **22.4 L**

            > For SATP (25°C, 1 bar) use 24.8 L instead
            """)

        col1, col2 = st.columns(2)
        with col1:
            gas_vol = st.number_input("Gas Volume", min_value=0.0,
                                      value=22.4, step=0.1)
            gas_vol_unit = st.selectbox("Volume Unit", ["L", "mL"])
        with col2:
            molar_vol = st.selectbox(
                "Molar Volume",
                ["22.4 L/mol (STP — 0°C, 1 atm)",
                 "24.8 L/mol (SATP — 25°C, 1 bar)"],
                help="STP = 0°C | SATP = 25°C"
            )

        if st.button("⚗️ Calculate", type="primary"):
            # Convert to L
            V = gas_vol / 1000 if gas_vol_unit == "mL" else gas_vol
            mv = 22.4 if "22.4" in molar_vol else 24.8
            moles = V / mv

            st.markdown("---")
            st.success(f"🔢 Moles = **{moles:.6f} mol**")

            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("Moles", f"{moles:.6f} mol")
            with col_r2:
                st.metric("Millimoles", f"{moles*1000:.4f} mmol")
            with col_r3:
                st.metric("Molecules", f"{moles * 6.022e23:.4e}")

            with st.expander("🔢 See Calculation Breakdown"):
                st.markdown(f"""
                **Formula:** n = V / molar volume

                - Gas Volume   = {gas_vol} {gas_vol_unit} = **{V:.4f} L**
                - Molar Volume = **{mv} L/mol**

                **n = {V:.4f} / {mv}**
                **n = {moles:.6f} mol**
                """)

            save_to_log("From Gas", f"{moles:.6f} mol",
                       f"V={gas_vol}{gas_vol_unit}, molar vol={mv}L/mol")

    # ── From Molecules ─────────────────────────────────────────────────────
    elif method == "🔬 Number of molecules":
        st.subheader("🔬 Moles from Number of Molecules")

        with st.expander("📐 See Formula"):
            st.markdown("""
            > n = N / Nₐ

            Where:
            - n  = moles (mol)
            - N  = number of molecules/atoms/ions
            - Nₐ = Avogadro's number = 6.022 × 10²³ mol⁻¹
            """)

        col1, col2 = st.columns(2)
        with col1:
            coeff = st.number_input("Number of molecules (coefficient)",
                                    min_value=0.0, value=6.022, step=0.001,
                                    format="%.4f")
        with col2:
            exponent = st.number_input("× 10 ^ (exponent)",
                                       min_value=0, max_value=30,
                                       value=23, step=1)

        num_molecules = coeff * (10 ** exponent)
        st.info(f"📊 Entered: **{coeff} × 10^{exponent}** = {num_molecules:.4e} molecules")

        if st.button("⚗️ Calculate", type="primary"):
            avogadro = 6.022e23
            moles = num_molecules / avogadro

            st.markdown("---")
            st.success(f"🔢 Moles = **{moles:.6f} mol**")

            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("Moles", f"{moles:.6f} mol")
            with col_r2:
                st.metric("Millimoles", f"{moles*1000:.4f} mmol")
            with col_r3:
                st.metric("Micromoles", f"{moles*1e6:.4f} µmol")

            with st.expander("🔢 See Calculation Breakdown"):
                st.markdown(f"""
                **Formula:** n = N / Nₐ

                - N  = **{num_molecules:.4e} molecules**
                - Nₐ = **6.022 × 10²³ mol⁻¹**

                **n = {num_molecules:.4e} / 6.022×10²³**
                **n = {moles:.6f} mol**
                """)

            save_to_log("From Molecules", f"{moles:.6f} mol",
                       f"N={num_molecules:.4e}")


# ── Save to Experiment Log ─────────────────────────────────────────────────
def save_to_log(method, result, details):
    import datetime
    log_entry = {
        "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
        "module": f"Moles Calculator ({method})",
        "chemical": "—",
        "result": result,
        "details": details
    }
    if "experiment_log" not in st.session_state:
        st.session_state.experiment_log = []
    st.session_state.experiment_log.append(log_entry)
    st.caption("✅ Saved to Experiment Log")