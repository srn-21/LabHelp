# -*- coding: utf-8 -*-
"""
Created on Wed May  6 03:41:51 2026

@author: shrn1
"""

import streamlit as st
import json

# ── Load Chemical Database ─────────────────────────────────────────────────
import os

def load_chemicals():
    # Get the folder where solution_prep.py lives
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "chemicals_db.json")
    with open(db_path, "r") as f:
        return json.load(f)

# ── Solid Solute Calculator ────────────────────────────────────────────────
def solid_solute_calculator():
    st.subheader("⚖️ Solid Solute Calculator")
    st.markdown("*How much solid chemical do I need to weigh?*")
    st.markdown("---")

    chemicals = load_chemicals()
    solid_names = [f"{c['name']} ({c['formula']})" for c in chemicals["solids"]]

    # ── Formula Display ────────────────────────────────────────────────────
    with st.expander("📐 See Formula"):
        st.markdown("""
        **Molarity Formula:**
        > M = (mass × purity) / (MW × V)

        **Rearranged to find mass:**
        > mass (g) = M × MW × V / purity

        Where:
        - M = desired molarity (mol/L)
        - MW = molecular weight (g/mol)
        - V = final volume (L)
        - purity = purity fraction (e.g. 0.99)

        **Normality Formula:**
        > N = M × n-factor

        **Mass from Normality:**
        > mass (g) = (N / n-factor) × MW × V / purity
        """)

    st.markdown("### 🔬 Select Your Chemical")
    col1, col2 = st.columns(2)

    with col1:
        selected = st.selectbox("Search Chemical", solid_names)
        chemical = chemicals["solids"][solid_names.index(selected)]

        st.info(f"""
        **Selected:** {chemical['name']}
        **Formula:** {chemical['formula']}
        **MW:** {chemical['mw']} g/mol
        **Purity:** {chemical['purity']}%
        """)

    with col2:
        # override purity if needed
        purity = st.number_input(
            "Purity (%)",
            min_value=1.0,
            max_value=100.0,
            value=float(chemical['purity']),
            step=0.1,
            help="Auto-filled from database, you can change it"
        )
        mw = st.number_input(
            "Molecular Weight (g/mol)",
            min_value=1.0,
            value=float(chemical['mw']),
            step=0.01,
            help="Auto-filled from database, you can change it"
        )

    st.markdown("### 🎯 What Do You Want to Prepare?")
    col3, col4, col5 = st.columns(3)

    with col3:
        conc = st.number_input("Desired Concentration", min_value=0.001, value=1.0, step=0.001)

    with col4:
        conc_unit = st.selectbox("Concentration Unit", [
            "mol/L (M)", 
            "mmol/L (mM)", 
            "N (Normality)",
            "g/L", 
            "mg/L", 
            "% w/v"
        ])

    # ── n-factor input — only shows when Normality is selected ────────────
    if conc_unit == "N (Normality)":
        default_n = int(chemical.get("n_factor", 1))
        st.info(f"💡 Normality = Molarity × n-factor | Default n-factor for {chemical['name']}: **{default_n}**")
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            n_factor = st.number_input(
                "n-factor (equivalents)",
                min_value=1,
                max_value=10,
                value=default_n,
                step=1,
                help="Auto-filled from database. Change only if reaction type differs."
            )
        with col_n2:
            st.markdown("**n-factor guide:**")
            st.caption("Acids → no. of H⁺ ions")
            st.caption("Bases → no. of OH⁻ ions")
            st.caption("Redox → electrons transferred")
    else:
        n_factor = 1

    with col5:
        vol = st.number_input("Final Volume", min_value=0.1, value=100.0, step=0.1)
        vol_unit = st.selectbox("Volume Unit", ["mL", "L"])

    # ── Calculate ──────────────────────────────────────────────────────────
    if st.button("⚗️ Calculate", type="primary"):

        # Convert volume to Litres
        V = vol / 1000 if vol_unit == "mL" else vol

        # Convert concentration to mol/L
        # Convert concentration to mol/L
        if conc_unit == "mol/L (M)":
            M = conc
        elif conc_unit == "mmol/L (mM)":
            M = conc / 1000
        elif conc_unit == "N (Normality)":
            M = conc / n_factor
        elif conc_unit == "g/L":
            M = conc / mw
        elif conc_unit == "mg/L":
            M = (conc / 1000) / mw
        elif conc_unit == "% w/v":
            M = (conc * 10) / mw

        purity_fraction = purity / 100
        mass = (M * mw * V) / purity_fraction

        # ── Results ────────────────────────────────────────────────────────
        st.markdown("---")
        st.success(f"⚖️ Weigh **{mass:.4f} g** of {chemical['name']}")

        # ── Step by Step ───────────────────────────────────────────────────
        st.markdown("### 📋 Step-by-Step Preparation Protocol")

        st.markdown(f"""
        **Step 1 — Weigh the chemical**
        > Weigh **{mass:.4f} g** of {chemical['name']} ({chemical['formula']})
        > using an analytical balance

        **Step 2 — Dissolve**
        > Transfer to a beaker, add ~{vol*0.7:.1f} {vol_unit} of distilled water
        > Stir until completely dissolved

        **Step 3 — Make up to volume**
        > Transfer to a **{vol:.0f} {vol_unit}** volumetric flask
        > Make up to the mark with distilled water

        **Step 4 — Mix well**
        > Stopper and invert the flask several times to mix thoroughly

        **✅ Final Solution:** {conc} {conc_unit} {chemical['name']} in {vol} {vol_unit}
        """)

        # ── Calculation Breakdown ──────────────────────────────────────────
        with st.expander("🔢 See Calculation Breakdown"):
            st.markdown(f"""
            **Formula used:** mass = M × MW × V / purity

            - Desired concentration = {conc} {conc_unit} = **{M:.6f} mol/L**
            - Molecular weight = **{mw} g/mol**
            - Final volume = {vol} {vol_unit} = **{V:.4f} L**
            - Purity = **{purity}% = {purity_fraction}**

            **mass = {M:.6f} × {mw} × {V:.4f} / {purity_fraction}**
            **mass = {mass:.4f} g**
            """)

        # ── Save to Experiment Log ─────────────────────────────────────────
        import datetime
        log_entry = {
            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
            "module": "Solid Solute Calculator",
            "chemical": chemical['name'],
            "result": f"Weigh {mass:.4f} g",
            "details": f"{conc} {conc_unit} in {vol} {vol_unit}"
        }

        if "experiment_log" not in st.session_state:
            st.session_state.experiment_log = []
        st.session_state.experiment_log.append(log_entry)
        st.caption("✅ Saved to Experiment Log")


# ── Main Solution Prep Page ────────────────────────────────────────────────
def show():
    st.title("🧪 Solution Preparation")
    st.markdown("---")

    sub = st.selectbox("Select Calculator", [
        "⚖️ Solid Solute Calculator",
        "🧴 Liquid Solute Calculator",
        "💧 Dilution C₁V₁=C₂V₂",
        "🔁 Serial Dilution",
        "⚗️ Acid Mixtures",
        "🧮 Buffer Preparation",
    ])

    st.markdown("---")

    if sub == "⚖️ Solid Solute Calculator":
        solid_solute_calculator()
    elif sub == "🧴 Liquid Solute Calculator":   # ← change this
        liquid_solute_calculator()    
    elif sub == "💧 Dilution C₁V₁=C₂V₂":
        dilution_calculator()
    elif sub == "🔁 Serial Dilution":
        serial_dilution_calculator()
    elif sub == "⚗️ Acid Mixtures":
        acid_mixtures_calculator()
    elif sub == "🧮 Buffer Preparation":
        buffer_preparation_calculator()
    else:print("buffer preparation calculator coming soon")
        
# ── Liquid Solute Calculator ───────────────────────────────────────────────
def liquid_solute_calculator():
    st.subheader("🧴 Liquid Solute Calculator")
    st.markdown("*How much liquid chemical do I need to measure?*")
    st.markdown("---")

    chemicals = load_chemicals()
    liquid_names = [f"{c['name']} ({c['formula']})" for c in chemicals["liquids"]]

    # ── Formula Display ────────────────────────────────────────────────────
    with st.expander("📐 See Formula"):
        st.markdown("""
        **Volume of liquid chemical needed:**
        > volume (mL) = (M × MW × V) / (density × purity_fraction)

        **Normality Formula:**
        > N = M × n-factor
        > mass (g) = (N / n-factor) × MW × V / purity

        Where:
        - M        = desired molarity (mol/L)
        - MW       = molecular weight (g/mol)
        - V        = final volume (L)
        - density  = density of liquid (g/mL)
        - purity   = assay % (e.g. 37 for 37% HCl)
        """)

    st.markdown("### 🔬 Select Your Chemical")
    col1, col2 = st.columns(2)

    with col1:
        selected = st.selectbox("Search Chemical", liquid_names)
        chemical = chemicals["liquids"][liquid_names.index(selected)]

        st.info(f"""
        **Selected:** {chemical['name']}
        **Formula:** {chemical['formula']}
        **MW:** {chemical['mw']} g/mol
        **Density:** {chemical['density']} g/mL
        **Purity/Assay:** {chemical['purity']}%
        """)

    with col2:
        purity = st.number_input(
            "Purity/Assay (%)",
            min_value=1.0,
            max_value=100.0,
            value=float(chemical['purity']),
            step=0.1,
            help="Auto-filled from database, you can change it"
        )
        density = st.number_input(
            "Density (g/mL)",
            min_value=0.1,
            value=float(chemical['density']),
            step=0.001,
            help="Auto-filled from database, you can change it"
        )
        mw = st.number_input(
            "Molecular Weight (g/mol)",
            min_value=1.0,
            value=float(chemical['mw']),
            step=0.01,
            help="Auto-filled from database, you can change it"
        )

    st.markdown("### 🎯 What Do You Want to Prepare?")
    col3, col4, col5 = st.columns(3)

    with col3:
        conc = st.number_input("Desired Concentration", min_value=0.001, value=1.0, step=0.001)

    with col4:
        conc_unit = st.selectbox("Concentration Unit", [
            "mol/L (M)",
            "mmol/L (mM)",
            "N (Normality)",
            "g/L",
            "mg/L",
            "% v/v"
        ])

    # ── n-factor — only shows for Normality ───────────────────────────────
    if conc_unit == "N (Normality)":
        default_n = int(chemical.get("n_factor", 1))
        st.info(f"💡 Normality = Molarity × n-factor | Default n-factor for {chemical['name']}: **{default_n}**")
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            n_factor = st.number_input(
                "n-factor (equivalents)",
                min_value=1,
                max_value=10,
                value=default_n,
                step=1,
                help="Auto-filled from database. Change only if reaction type differs."
            )
        with col_n2:
            st.markdown("**n-factor guide:**")
            st.caption("Acids → no. of H⁺ ions")
            st.caption("Bases → no. of OH⁻ ions")
            st.caption("Redox → electrons transferred")
    else:
        n_factor = 1

    with col5:
        vol = st.number_input("Final Volume", min_value=0.1, value=100.0, step=0.1)
        vol_unit = st.selectbox("Volume Unit", ["mL", "L"])

    # ── Safety Warning ─────────────────────────────────────────────────────
    dangerous = ["Hydrochloric Acid", "Sulfuric Acid", "Nitric Acid",
                 "Perchloric Acid", "Hydrofluoric Acid"]
    if chemical['name'] in dangerous:
        st.warning(f"⚠️ **Safety:** Always add {chemical['name']} slowly to water. Never add water to acid! Work in a fume hood.")

    # ── Calculate ──────────────────────────────────────────────────────────
    if st.button("⚗️ Calculate", type="primary"):

        # Convert volume to litres
        V = vol / 1000 if vol_unit == "mL" else vol

        # Convert concentration to mol/L
        if conc_unit == "mol/L (M)":
            M = conc
        elif conc_unit == "mmol/L (mM)":
            M = conc / 1000
        elif conc_unit == "N (Normality)":
            M = conc / n_factor
        elif conc_unit == "g/L":
            M = conc / mw
        elif conc_unit == "mg/L":
            M = (conc / 1000) / mw
        elif conc_unit == "% v/v":
            M = (conc * density * 10) / mw

        # Calculate volume of liquid chemical needed
        vol_needed = (M * mw * V) / (density * purity / 100)

        # ── Results ────────────────────────────────────────────────────────
        st.markdown("---")
        st.success(f"🧴 Measure **{vol_needed:.4f} mL** of {chemical['name']}")

        # ── Step by Step ───────────────────────────────────────────────────
        st.markdown("### 📋 Step-by-Step Preparation Protocol")
        st.markdown(f"""
        **Step 1 — Prepare your flask**
        > Take a **{vol:.0f} {vol_unit}** volumetric flask
        > Add ~{vol*0.5:.0f} {vol_unit} of distilled water first

        **Step 2 — Measure the chemical**
        > Carefully measure **{vol_needed:.4f} mL** of {chemical['name']}
        > Using a pipette or measuring cylinder

        **Step 3 — Add to flask slowly**
        > Add the {chemical['name']} slowly to the water while stirring
        > {'⚠️ Work in fume hood — add acid to water slowly!' if chemical['name'] in dangerous else 'Mix gently'}

        **Step 4 — Make up to volume**
        > Allow to cool to room temperature if needed
        > Make up to **{vol:.0f} {vol_unit}** mark with distilled water

        **Step 5 — Mix well**
        > Stopper and invert several times to mix thoroughly

        **✅ Final Solution:** {conc} {conc_unit} {chemical['name']} in {vol} {vol_unit}
        """)

        # ── Calculation Breakdown ──────────────────────────────────────────
        with st.expander("🔢 See Calculation Breakdown"):
            st.markdown(f"""
            **Formula:** volume (mL) = (M × MW × V) / (density × purity_fraction)

            - Desired concentration = {conc} {conc_unit} = **{M:.6f} mol/L**
            - Molecular weight = **{mw} g/mol**
            - Final volume = {vol} {vol_unit} = **{V:.4f} L**
            - Density = **{density} g/mL**
            - Purity/Assay = **{purity}%**

            **volume = ({M:.6f} × {mw} × {V:.4f}) / ({density} × {purity/100:.4f})**
            **volume = {vol_needed:.4f} mL**
            """)

        # ── Save to Experiment Log ─────────────────────────────────────────
        import datetime
        log_entry = {
            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
            "module": "Liquid Solute Calculator",
            "chemical": chemical['name'],
            "result": f"Measure {vol_needed:.4f} mL",
            "details": f"{conc} {conc_unit} in {vol} {vol_unit}"
        }
        if "experiment_log" not in st.session_state:
            st.session_state.experiment_log = []
        st.session_state.experiment_log.append(log_entry)
        st.caption("✅ Saved to Experiment Log")
        
# ── Dilution Calculator ────────────────────────────────────────────────────
def dilution_calculator():
    st.subheader("💧 Dilution Calculator")
    st.markdown("*C₁V₁ = C₂V₂ — Solve for any variable*")
    st.markdown("---")

    # ── Formula Display ────────────────────────────────────────────────────
    with st.expander("📐 See Formula"):
        st.markdown("""
        **Dilution Formula:**
        > C₁V₁ = C₂V₂

        **Rearranged:**
        > V₁ = (C₂ × V₂) / C₁  → volume to take from stock
        > C₁ = (C₂ × V₂) / V₁  → stock concentration
        > C₂ = (C₁ × V₁) / V₂  → final concentration
        > V₂ = (C₁ × V₁) / C₂  → final volume

        Where:
        - C₁ = initial (stock) concentration
        - V₁ = volume taken from stock
        - C₂ = final (desired) concentration
        - V₂ = final (desired) volume
        """)

    # ── Solve For ──────────────────────────────────────────────────────────
    st.markdown("### 🎯 What do you want to find?")
    solve_for = st.selectbox("Solve for:", [
        "V₁ — Volume to take from stock",
        "C₂ — Final concentration",
        "C₁ — Stock concentration",
        "V₂ — Final volume",
    ])

    st.markdown("---")
    st.markdown("### 🔢 Enter Known Values")

    # ── Concentration Unit ─────────────────────────────────────────────────
    conc_unit = st.selectbox("Concentration Unit", [
        "mol/L (M)", "mmol/L (mM)", "µmol/L (µM)",
        "N (Normality)", "g/L", "mg/L", "µg/L", "% v/v", "% w/v"
    ])

    vol_unit = st.selectbox("Volume Unit", ["mL", "L", "µL"])

    st.markdown("---")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # ── Input fields — grey out the one being solved ───────────────────────
    with col1:
        if "C₁" not in solve_for:
            C1 = st.number_input(f"C₁ — Stock Concentration ({conc_unit})",
                                  min_value=0.0, value=1.0, step=0.001)
        else:
            st.info("C₁ = ? (solving for this)")
            C1 = None

    with col2:
        if "V₁" not in solve_for:
            V1 = st.number_input(f"V₁ — Stock Volume ({vol_unit})",
                                  min_value=0.0, value=10.0, step=0.1)
        else:
            st.info("V₁ = ?")
            V1 = None

    with col3:
        if "C₂" not in solve_for:
            C2 = st.number_input(f"C₂ — Final Concentration ({conc_unit})",
                                  min_value=0.0, value=0.1, step=0.001)
        else:
            st.info("C₂ = ? (solving for this)")
            C2 = None

    with col4:
        if "V₂" not in solve_for:
            V2 = st.number_input(f"V₂ — Final Volume ({vol_unit})",
                                  min_value=0.0, value=100.0, step=0.1)
        else:
            st.info("V₂ = ? (solving for this)")
            V2 = None

    # ── Calculate ──────────────────────────────────────────────────────────
    if st.button("⚗️ Calculate", type="primary"):

        st.markdown("---")

        if "V₁" in solve_for:
            result = (C2 * V2) / C1
            st.success(f"💧 Take **{result:.4f} {vol_unit}** from stock solution")
            step2 = f"Make up to **{V2:.1f} {vol_unit}** with solvent"
            solvent_vol = V2 - result

            st.markdown("### 📋 Step-by-Step Protocol")
            st.markdown(f"""
            **Step 1 — Measure stock solution**
            > Take **{result:.4f} {vol_unit}** of your {C1} {conc_unit} stock solution
            > using a pipette

            **Step 2 — Transfer to volumetric flask**
            > Transfer to a **{V2:.0f} {vol_unit}** volumetric flask
            > containing a small amount of solvent

            **Step 3 — Make up to volume**
            > Add solvent to make up to **{V2:.0f} {vol_unit}**
            > (add approximately {solvent_vol:.2f} {vol_unit} of solvent)

            **Step 4 — Mix well**
            > Stopper and invert several times

            **✅ Final Solution:** {C2} {conc_unit} in {V2} {vol_unit}
            """)

            with st.expander("🔢 See Calculation Breakdown"):
                st.markdown(f"""
                **Formula:** V₁ = (C₂ × V₂) / C₁

                - C₁ = **{C1} {conc_unit}** (stock)
                - C₂ = **{C2} {conc_unit}** (desired)
                - V₂ = **{V2} {vol_unit}** (desired volume)

                **V₁ = ({C2} × {V2}) / {C1}**
                **V₁ = {result:.4f} {vol_unit}**
                """)

        elif "C₂" in solve_for:
            result = (C1 * V1) / V2
            st.success(f"🧪 Final concentration = **{result:.6f} {conc_unit}**")

            with st.expander("🔢 See Calculation Breakdown"):
                st.markdown(f"""
                **Formula:** C₂ = (C₁ × V₁) / V₂

                - C₁ = **{C1} {conc_unit}**
                - V₁ = **{V1} {vol_unit}**
                - V₂ = **{V2} {vol_unit}**

                **C₂ = ({C1} × {V1}) / {V2}**
                **C₂ = {result:.6f} {conc_unit}**
                """)

        elif "C₁" in solve_for:
            result = (C2 * V2) / V1
            st.success(f"🧪 Required stock concentration = **{result:.6f} {conc_unit}**")

            with st.expander("🔢 See Calculation Breakdown"):
                st.markdown(f"""
                **Formula:** C₁ = (C₂ × V₂) / V₁

                - C₂ = **{C2} {conc_unit}**
                - V₁ = **{V1} {vol_unit}**
                - V₂ = **{V2} {vol_unit}**

                **C₁ = ({C2} × {V2}) / {V1}**
                **C₁ = {result:.6f} {conc_unit}**
                """)

        elif "V₂" in solve_for:
            result = (C1 * V1) / C2
            st.success(f"💧 Final volume = **{result:.4f} {vol_unit}**")

            with st.expander("🔢 See Calculation Breakdown"):
                st.markdown(f"""
                **Formula:** V₂ = (C₁ × V₁) / C₂

                - C₁ = **{C1} {conc_unit}**
                - V₁ = **{V1} {vol_unit}**
                - C₂ = **{C2} {conc_unit}**

                **V₂ = ({C1} × {V1}) / {C2}**
                **V₂ = {result:.4f} {vol_unit}**
                """)

        # ── Save to Experiment Log ─────────────────────────────────────────
        import datetime
        log_entry = {
            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
            "module": "Dilution Calculator",
            "chemical": "—",
            "result": f"{solve_for.split('—')[0].strip()} = {result:.4f}",
            "details": f"C₁={C1}, V₁={V1}, C₂={C2}, V₂={V2} ({conc_unit}, {vol_unit})"
        }
        if "experiment_log" not in st.session_state:
            st.session_state.experiment_log = []
        st.session_state.experiment_log.append(log_entry)
        st.caption("✅ Saved to Experiment Log")
        
# ── Serial Dilution Calculator ─────────────────────────────────────────────
def serial_dilution_calculator():
    st.subheader("🔁 Serial Dilution Calculator")
    st.markdown("*Step-by-step dilution chain — same factor repeated each time*")
    st.markdown("---")

    with st.expander("📐 See Formula"):
        st.markdown("""
        **Concentration at each step:**
        > Cₙ = C₀ / (DF)ⁿ

        **Volume to take from previous tube:**
        > V_transfer = V_total / DF

        **Volume of diluent to add:**
        > V_diluent = V_total - V_transfer

        Where:
        - C₀ = starting concentration
        - DF = dilution factor (e.g. 10 for 1:10)
        - n  = step number
        - V_total = total volume in each tube
        """)

    st.markdown("### ⚙️ Setup")
    col1, col2 = st.columns(2)

    with col1:
        start_conc = st.number_input(
            "Starting Concentration (C₀)",
            min_value=0.000001,
            value=1.0,
            step=0.001,
            format="%.6f"
        )
        conc_unit = st.selectbox("Concentration Unit", [
            "mol/L (M)", "mmol/L (mM)", "µmol/L (µM)",
            "g/L", "mg/L", "µg/L", "ppm", "ppb", "% v/v"
        ])

    with col2:
        dilution_factor = st.number_input(
            "Dilution Factor",
            min_value=2,
            max_value=1000,
            value=10,
            step=1,
            help="e.g. 10 means 1:10 dilution each step"
        )
        num_steps = st.number_input(
            "Number of Steps (tubes)",
            min_value=2,
            max_value=20,
            value=5,
            step=1
        )

    col3, col4 = st.columns(2)
    with col3:
        total_vol = st.number_input(
            "Volume in Each Tube",
            min_value=0.1,
            value=10.0,
            step=0.1
        )
    with col4:
        vol_unit = st.selectbox("Volume Unit", ["mL", "L", "µL"])

    # ── Calculate ──────────────────────────────────────────────────────────
    if st.button("⚗️ Calculate", type="primary"):

        v_transfer = total_vol / dilution_factor
        v_diluent  = total_vol - v_transfer

        # ── Summary boxes ──────────────────────────────────────────────────
        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Transfer Volume", f"{v_transfer:.4f} {vol_unit}")
        with col_b:
            st.metric("Diluent to Add", f"{v_diluent:.4f} {vol_unit}")
        with col_c:
            st.metric("Dilution Factor", f"1:{dilution_factor}")

        # ── Build Table ────────────────────────────────────────────────────
        st.markdown("### 📊 Dilution Table")

        import pandas as pd

        rows = []

        # Stock row
        rows.append({
            "Tube": "Stock",
            f"Concentration ({conc_unit})": f"{start_conc:.6g}",
            f"Transfer ({vol_unit})": f"{v_transfer:.4f}",
            f"Diluent ({vol_unit})": f"{v_diluent:.4f}",
            f"Total Vol ({vol_unit})": f"{total_vol:.2f}",
            "Dilution Factor": "—"
        })

        for i in range(1, int(num_steps) + 1):
            conc_i = start_conc / (dilution_factor ** i)
            rows.append({
                "Tube": f"Tube {i}",
                f"Concentration ({conc_unit})": f"{conc_i:.6g}",
                f"Transfer ({vol_unit})": f"{v_transfer:.4f}" if i < num_steps else "—",
                f"Diluent ({vol_unit})": f"{v_diluent:.4f}" if i < num_steps else "—",
                f"Total Vol ({vol_unit})": f"{total_vol:.2f}",
                "Dilution Factor": f"1:{dilution_factor}"
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # ── Step by Step Protocol ──────────────────────────────────────────
        st.markdown("### 📋 Step-by-Step Protocol")

        st.markdown(f"""
        **Preparation:**
        > Label {num_steps} tubes as Tube 1 to Tube {num_steps}
        > Add **{v_diluent:.4f} {vol_unit}** of diluent to each tube
        """)

        for i in range(1, int(num_steps) + 1):
            conc_i = start_conc / (dilution_factor ** i)
            source  = "Stock" if i == 1 else f"Tube {i-1}"
            st.markdown(f"""
        **Tube {i}** — {conc_i:.6g} {conc_unit}
        > Transfer **{v_transfer:.4f} {vol_unit}** from {source}
        > Mix well before taking next transfer
            """)

        st.warning("⚠️ Always mix each tube thoroughly before transferring to the next!")

        # ── Calculation Breakdown ──────────────────────────────────────────
        with st.expander("🔢 See Calculation Breakdown"):
            st.markdown(f"""
            **Transfer volume** = Total volume / DF = {total_vol} / {dilution_factor} = **{v_transfer:.4f} {vol_unit}**

            **Diluent volume** = Total - Transfer = {total_vol} - {v_transfer:.4f} = **{v_diluent:.4f} {vol_unit}**

            | Step | Formula | Result |
            |------|---------|--------|
            """ + "\n".join([
                f"| Tube {i} | {start_conc:.6g} / {dilution_factor}^{i} | {start_conc / (dilution_factor**i):.6g} {conc_unit} |"
                for i in range(1, int(num_steps)+1)
            ]))

        # ── Save to Experiment Log ─────────────────────────────────────────
        import datetime
        log_entry = {
            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
            "module": "Serial Dilution",
            "chemical": "—",
            "result": f"{num_steps} steps, DF=1:{dilution_factor}",
            "details": f"Start: {start_conc} {conc_unit}, End: {start_conc/(dilution_factor**num_steps):.6g} {conc_unit}"
        }
        if "experiment_log" not in st.session_state:
            st.session_state.experiment_log = []
        st.session_state.experiment_log.append(log_entry)
        st.caption("✅ Saved to Experiment Log")
        
# ── Acid Mixtures Calculator ───────────────────────────────────────────────
def acid_mixtures_calculator():
    st.subheader("⚗️ Acid Mixtures Calculator")
    st.markdown("*Prepare fixed-ratio acid mixtures safely*")
    st.markdown("---")

    # ── Mixture Database ───────────────────────────────────────────────────
    mixtures = {
        "Aqua Regia (3:1)": {
            "components": [
                {"name": "Hydrochloric Acid (HCl)", "ratio": 3, "conc": "37%", "density": 1.19},
                {"name": "Nitric Acid (HNO₃)", "ratio": 1, "conc": "70%", "density": 1.41}
            ],
            "use": "Dissolving noble metals (gold, platinum, palladium)",
            "hazard": "🔴 EXTREMELY CORROSIVE — produces toxic NOCl gas. Always prepare fresh in fume hood!",
            "order": "Add HNO₃ first, then HCl slowly",
            "color": "error"
        },
        "Piranha Solution (3:1)": {
            "components": [
                {"name": "Sulfuric Acid (H₂SO₄)", "ratio": 3, "conc": "98%", "density": 1.84},
                {"name": "Hydrogen Peroxide (H₂O₂)", "ratio": 1, "conc": "30%", "density": 1.11}
            ],
            "use": "Cleaning organic residues from glass/silicon surfaces",
            "hazard": "🔴 EXTREMELY DANGEROUS — highly exothermic, can cause fires/explosions. Never store in closed containers!",
            "order": "Add H₂O₂ slowly to H₂SO₄, never reverse!",
            "color": "error"
        },
        "Nital 2% (2:98)": {
            "components": [
                {"name": "Nitric Acid (HNO₃)", "ratio": 2, "conc": "70%", "density": 1.41},
                {"name": "Ethanol", "ratio": 98, "conc": "99.9%", "density": 0.789}
            ],
            "use": "Metallographic etching of iron and steel",
            "hazard": "🟡 Flammable — keep away from heat sources. Work in fume hood.",
            "order": "Add HNO₃ slowly to ethanol",
            "color": "warning"
        },
        "Alkaline Piranha (1:1:5)": {
            "components": [
                {"name": "Ammonium Hydroxide (NH₄OH)", "ratio": 1, "conc": "25%", "density": 0.91},
                {"name": "Hydrogen Peroxide (H₂O₂)", "ratio": 1, "conc": "30%", "density": 1.11},
                {"name": "Water (H₂O)", "ratio": 5, "conc": "100%", "density": 1.00}
            ],
            "use": "Cleaning silicon wafers, removing organic contamination",
            "hazard": "🟡 Corrosive — produces heat. Work in fume hood.",
            "order": "Add NH₄OH to water first, then H₂O₂ slowly",
            "color": "warning"
        },
        "Buffered HF (BHF) (6:1)": {
            "components": [
                {"name": "Ammonium Fluoride (NH₄F)", "ratio": 6, "conc": "40%", "density": 1.15},
                {"name": "Hydrofluoric Acid (HF)", "ratio": 1, "conc": "48%", "density": 1.15}
            ],
            "use": "Etching silicon dioxide (SiO₂) in semiconductor fabrication",
            "hazard": "🔴 EXTREMELY DANGEROUS — HF causes deep tissue damage. Use full PPE, face shield, HF-resistant gloves!",
            "order": "Add HF slowly to NH₄F solution",
            "color": "error"
        },
        "Custom Mixture": {
            "components": [],
            "use": "Define your own ratio mixture",
            "hazard": "⚠️ Follow appropriate safety guidelines for your chemicals",
            "order": "Follow safe mixing practices",
            "color": "warning"
        }
    }

    # ── Select Mixture ─────────────────────────────────────────────────────
    selected_mixture = st.selectbox("Select Mixture", list(mixtures.keys()))
    mixture = mixtures[selected_mixture]

    st.markdown("---")

    # ── Custom Mixture Builder ─────────────────────────────────────────────
    if selected_mixture == "Custom Mixture":
        st.markdown("### ✏️ Define Your Custom Mixture")
        num_components = st.number_input("Number of Components", min_value=2, max_value=5, value=2, step=1)

        custom_components = []
        for i in range(int(num_components)):
            st.markdown(f"**Component {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                cname = st.text_input(f"Name", key=f"cname_{i}", placeholder="e.g. HCl")
            with col2:
                cratio = st.number_input(f"Ratio parts", min_value=1, value=1, step=1, key=f"cratio_{i}")
            custom_components.append({"name": cname, "ratio": cratio})
        mixture["components"] = custom_components

    # ── Mixture Info ───────────────────────────────────────────────────────
    if selected_mixture != "Custom Mixture":
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"**Use:** {mixture['use']}")
        with col_info2:
            st.info(f"**Mixing order:** {mixture['order']}")

    # ── Safety Warning ─────────────────────────────────────────────────────
    if mixture["color"] == "error":
        st.error(f"⚠️ **Safety Warning:** {mixture['hazard']}")
    else:
        st.warning(f"⚠️ **Safety Warning:** {mixture['hazard']}")

    # ── Show Ratio ─────────────────────────────────────────────────────────
    if mixture["components"]:
        ratio_str = " : ".join([str(c["ratio"]) for c in mixture["components"]])
        names_str = " : ".join([c["name"].split("(")[0].strip() for c in mixture["components"]])
        st.markdown(f"**Ratio:** {names_str} = **{ratio_str}**")

    st.markdown("---")

    # ── Total Volume Input ─────────────────────────────────────────────────
    st.markdown("### 🎯 How Much Do You Want to Prepare?")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        total_vol = st.number_input("Total Volume", min_value=1.0, value=100.0, step=1.0)
    with col_v2:
        vol_unit = st.selectbox("Volume Unit", ["mL", "L"])

    # ── Calculate ──────────────────────────────────────────────────────────
    if st.button("⚗️ Calculate", type="primary"):

        components = mixture["components"]
        total_ratio = sum(c["ratio"] for c in components)

        st.markdown("---")
        st.markdown("### 📊 Component Volumes")

        # Results columns
        cols = st.columns(len(components))
        volumes = []
        for i, comp in enumerate(components):
            vol_i = (comp["ratio"] / total_ratio) * total_vol
            volumes.append(vol_i)
            with cols[i]:
                st.metric(
                    label=comp["name"].split("(")[0].strip(),
                    value=f"{vol_i:.4f} {vol_unit}"
                )

        # ── Step by Step ───────────────────────────────────────────────────
        st.markdown("### 📋 Step-by-Step Preparation Protocol")
        st.markdown(f"**Preparing {total_vol} {vol_unit} of {selected_mixture}**")
        st.markdown("")

        if selected_mixture != "Custom Mixture":
            st.markdown(f"**⚠️ Mixing Order:** {mixture['order']}")
            st.markdown("")

        for i, (comp, vol_i) in enumerate(zip(components, volumes)):
            st.markdown(f"""
        **Step {i+1} — {comp['name'].split('(')[0].strip()}**
        > Measure **{vol_i:.4f} {vol_unit}** carefully
        > {'Use a glass measuring cylinder or pipette' if vol_i > 5 else 'Use a micropipette for accuracy'}
            """)

        st.markdown(f"""
        **Final Step — Mix**
        > Combine in order stated above
        > Mix gently — **do not shake vigorously**
        > Total volume = **{total_vol} {vol_unit}**
        """)

        st.error("🧤 Always wear appropriate PPE: gloves, lab coat, safety goggles, work in fume hood!")

        # ── Calculation Breakdown ──────────────────────────────────────────
        with st.expander("🔢 See Calculation Breakdown"):
            st.markdown(f"**Total ratio parts = {total_ratio}**")
            st.markdown("")
            for comp, vol_i in zip(components, volumes):
                st.markdown(f"""
                **{comp['name'].split('(')[0].strip()}:**
                > ({comp['ratio']} / {total_ratio}) × {total_vol} = **{vol_i:.4f} {vol_unit}**
                """)

        # ── Save to Experiment Log ─────────────────────────────────────────
        import datetime
        log_entry = {
            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
            "module": "Acid Mixtures",
            "chemical": selected_mixture,
            "result": f"{total_vol} {vol_unit} prepared",
            "details": " + ".join([f"{v:.2f}{vol_unit} {c['name'].split('(')[0].strip()}"
                                   for c, v in zip(components, volumes)])
        }
        if "experiment_log" not in st.session_state:
            st.session_state.experiment_log = []
        st.session_state.experiment_log.append(log_entry)
        st.caption("✅ Saved to Experiment Log")
        
# ── Buffer Preparation Calculator ──────────────────────────────────────────
def buffer_preparation_calculator():
    st.subheader("🧮 Buffer Preparation")
    st.markdown("*Henderson-Hasselbalch — calculate exact amounts for any buffer*")
    st.markdown("---")

    with st.expander("📐 See Formula"):
        st.markdown("""
        **Henderson-Hasselbalch:**
        > pH = pKa + log([A⁻]/[HA])

        **Ratio of base to acid:**
        > [A⁻]/[HA] = 10^(pH - pKa)

        **Individual concentrations:**
        > [A⁻] = C × 10^(pH-pKa) / (1 + 10^(pH-pKa))
        > [HA]  = C / (1 + 10^(pH-pKa))

        Where:
        - pH  = desired pH
        - pKa = acid dissociation constant
        - C   = total buffer concentration
        - [A⁻] = conjugate base concentration
        - [HA]  = weak acid concentration
        """)

    # ── Buffer Database ────────────────────────────────────────────────────
    buffers = {
        "Acetate Buffer": {
            "pka": 4.76,
            "range": "3.6 – 5.6",
            "acid": {
                "name": "Acetic Acid",
                "formula": "CH₃COOH",
                "mw": 60.05,
                "type": "liquid",
                "density": 1.05,
                "purity": 99.5
            },
            "base": {
                "name": "Sodium Acetate",
                "formula": "CH₃COONa",
                "mw": 82.03,
                "type": "solid",
                "purity": 99.0,
                "hydrates": {
                    "Anhydrous (MW = 82.03)": 82.03,
                    "Trihydrate . 33H₂O (MW = 136.08)": 136.08
                }
            }
        },
        "Phosphate Buffer": {
            "pka": 7.20,
            "range": "5.8 – 8.0",
            "acid": {
                "name": "Sodium Dihydrogen Phosphate",
                "formula": "NaH₂PO₄",
                "mw": 119.98,
                "type": "solid",
                "purity": 99.0,
                "hydrates": {
                    "Anhydrous (MW = 119.98)": 119.98,
                    "Monohydrate · H₂O (MW = 137.99)": 137.99,
                    "Dihydrate · 2H₂O (MW = 156.01)": 156.01
                }
            },
            "base": {
                "name": "Disodium Hydrogen Phosphate",
                "formula": "Na₂HPO₄",
                "mw": 141.96,
                "type": "solid",
                "purity": 99.0,
                "hydrates": {
                    "Anhydrous (MW = 141.96)": 141.96,
                    "Dihydrate · 2H₂O (MW = 177.99)": 177.99,
                    "Heptahydrate · 7H₂O (MW = 268.07)": 268.07,
                    "Dodecahydrate · 12H₂O (MW = 358.14)": 358.14
                }
            }
        },
        "Tris Buffer": {
            "pka": 8.06,
            "range": "7.0 – 9.0",
            "acid": {
                "name": "Tris-HCl",
                "formula": "Tris·HCl",
                "mw": 157.60,
                "type": "solid",
                "purity": 99.0
            },
            "base": {
                "name": "Tris Base",
                "formula": "Tris",
                "mw": 121.14,
                "type": "solid",
                "purity": 99.9
            }
        },
        "Citrate Buffer": {
            "pka": 4.76,
            "range": "3.0 – 6.2",
            "acid": {
                "name": "Citric Acid",
                "formula": "C₆H₈O₇",
                "mw": 192.12,
                "type": "solid",
                "purity": 99.5,
                "hydrates": {
                    "Anhydrous (MW = 192.12)": 192.12,
                    "Monohydrate · H₂O (MW = 210.14)": 210.14
                }
            },
            "base": {
                "name": "Sodium Citrate",
                "formula": "Na₃C₆H₅O₇",
                "mw": 258.07,
                "type": "solid",
                "purity": 99.0,
                "hydrates": {
                    "Anhydrous (MW = 258.07)": 258.07,
                    "Dihydrate · 2H₂O (MW = 294.10)": 294.10
                }
            }
        },
        "Carbonate Buffer": {
            "pka": 10.33,
            "range": "9.2 – 10.8",
            "acid": {
                "name": "Sodium Bicarbonate",
                "formula": "NaHCO₃",
                "mw": 84.01,
                "type": "solid",
                "purity": 99.5
            },
            "base": {
                "name": "Sodium Carbonate",
                "formula": "Na₂CO₃",
                "mw": 105.99,
                "type": "solid",
                "purity": 99.5,
                "hydrates": {
                    "Anhydrous (MW = 105.99)": 105.99,
                    "Monohydrate · H₂O (MW = 124.00)": 124.00,
                    "Decahydrate · 10H₂O (MW = 286.14)": 286.14
                }
            }
        },
        "Borate Buffer": {
            "pka": 9.24,
            "range": "8.0 – 10.0",
            "acid": {
                "name": "Boric Acid",
                "formula": "H₃BO₃",
                "mw": 61.83,
                "type": "solid",
                "purity": 99.5
            },
            "base": {
                "name": "Sodium Borate",
                "formula": "Na₂B₄O₇",
                "mw": 201.22,
                "type": "solid",
                "purity": 99.5,
                "hydrates": {
                    "Anhydrous (MW = 201.22)": 201.22,
                    "Decahydrate · 10H₂O (MW = 381.37)": 381.37
            }
        },
        "HEPES Buffer": {
            "pka": 7.55,
            "range": "6.8 – 8.2",
            "acid": {
                "name": "HEPES acid form",
                "formula": "HEPES",
                "mw": 238.30,
                "type": "solid",
                "purity": 99.5
            },
            "base": {
                "name": "HEPES Sodium Salt",
                "formula": "HEPES-Na",
                "mw": 260.29,
                "type": "solid",
                "purity": 99.5
            }
        },
        "MES Buffer": {
            "pka": 6.15,
            "range": "5.5 – 6.7",
            "acid": {
                "name": "MES acid form",
                "formula": "MES",
                "mw": 195.20,
                "type": "solid",
                "purity": 99.5
            },
            "base": {
                "name": "MES Sodium Salt",
                "formula": "MES-Na",
                "mw": 217.22,
                "type": "solid",
                "purity": 99.5
                }
            }
        }
    }


    # ── Select Buffer ──────────────────────────────────────────────────────
    st.markdown("### 🔬 Select Buffer System")
    selected_buffer = st.selectbox("Buffer System", list(buffers.keys()))
    buf = buffers[selected_buffer]

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        **pKa:** {buf['pka']}
        **Useful pH Range:** {buf['range']}
        **Acid component:** {buf['acid']['name']} ({buf['acid']['formula']})
        **Base component:** {buf['base']['name']} ({buf['base']['formula']})
        """)
    with col2:
        pka = st.number_input(
            "pKa",
            value=float(buf['pka']),
            step=0.01,
            help="Auto-filled — change only if you have a different value"
        )

    st.markdown("### 🎯 What Do You Want to Prepare?")
    col3, col4, col5 = st.columns(3)

    with col3:
        desired_ph = st.number_input(
            "Desired pH",
            min_value=0.0,
            max_value=14.0,
            value=float(buf['pka']),
            step=0.1,
            format="%.2f"
        )

    with col4:
        total_conc = st.number_input(
            "Total Buffer Concentration (mol/L)",
            min_value=0.001,
            value=0.1,
            step=0.001,
            format="%.4f"
        )

    with col5:
        total_vol = st.number_input("Final Volume", min_value=1.0, value=100.0, step=1.0)
        vol_unit = st.selectbox("Volume Unit", ["mL", "L"])

    # ── pH Range Warning ───────────────────────────────────────────────────
    ph_min = float(buf['range'].split('–')[0].strip())
    ph_max = float(buf['range'].split('–')[1].strip())
    if desired_ph < ph_min or desired_ph > ph_max:
        st.warning(f"⚠️ pH {desired_ph} is outside the recommended range ({buf['range']}) for {selected_buffer}. Results may be inaccurate!")
    else:
        st.success(f"✅ pH {desired_ph} is within the recommended range ({buf['range']})")

    # ── Hydrate Selection BEFORE Calculate ────────────────────────────────
    acid = buf['acid']
    base = buf['base']

    st.markdown("### 🧴 Select Chemical Forms Available in Your Lab")
    col_h1, col_h2 = st.columns(2)

    with col_h1:
        if acid['type'] == 'solid' and "hydrates" in acid:
            acid_hydrate_choice = st.selectbox(
                f"Form of {acid['name']}",
                list(acid["hydrates"].keys()),
                key="acid_hydrate"
            )
            acid_mw = acid["hydrates"][acid_hydrate_choice]
        else:
            acid_mw = acid['mw']
            acid_hydrate_choice = acid['name']
        st.caption(f"MW = {acid_mw} g/mol")

    with col_h2:
        if "hydrates" in base:
            base_hydrate_choice = st.selectbox(
                f"Form of {base['name']}",
                list(base["hydrates"].keys()),
                key="base_hydrate"
            )
            base_mw = base["hydrates"][base_hydrate_choice]
        else:
            base_mw = base['mw']
            base_hydrate_choice = base['name']
        st.caption(f"MW = {base_mw} g/mol")

    # ── Calculate ──────────────────────────────────────────────────────────
    if st.button("⚗️ Calculate", type="primary"):

        import math
        ratio = 10 ** (desired_ph - pka)
        V = total_vol / 1000 if vol_unit == "mL" else total_vol

        conc_base = total_conc * ratio / (1 + ratio)
        conc_acid = total_conc / (1 + ratio)

        moles_acid = conc_acid * V
        moles_base = conc_base * V

        # Acid amount
        if acid['type'] == 'solid':
            amount_acid = (moles_acid * acid_mw) / (acid['purity'] / 100)
            acid_unit = "g"
            acid_instruction = f"Weigh **{amount_acid:.4f} g** of {acid['name']} ({acid_hydrate_choice})"
        else:
            amount_acid = (moles_acid * acid['mw']) / (acid['density'] * acid['purity'] / 100)
            acid_unit = "mL"
            acid_instruction = f"Measure **{amount_acid:.4f} mL** of {acid['name']}"

        # Base amount
        amount_base = (moles_base * base_mw) / (base['purity'] / 100)
        base_instruction = f"Weigh **{amount_base:.4f} g** of {base['name']} ({base_hydrate_choice})"

        # ── Results ────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📊 Results")

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("Base : Acid Ratio", f"{ratio:.3f} : 1")
        with col_r2:
            st.metric(f"{acid['name'].split()[0]} needed",
                     f"{amount_acid:.4f} {acid_unit}")
        with col_r3:
            st.metric(f"{base['name'].split()[0]} needed",
                     f"{amount_base:.4f} g")

        # ── Step by Step ───────────────────────────────────────────────────
        st.markdown("### 📋 Step-by-Step Preparation Protocol")
        st.markdown(f"""
        **Step 1 — Prepare acid component**
        > {acid_instruction} ({acid['formula']})
        > MW = {acid['mw']} g/mol | Purity = {acid['purity']}%

        **Step 2 — Prepare base component**
        > {base_instruction} ({base['formula']})
        > MW = {base['mw']} g/mol | Purity = {base['purity']}%

        **Step 3 — Dissolve**
        > Dissolve both in ~{total_vol * 0.7:.0f} {vol_unit} of distilled water
        > Stir until completely dissolved

        **Step 4 — Combine and check pH**
        > Combine both solutions in a {total_vol:.0f} {vol_unit} volumetric flask
        > Check pH with a calibrated pH meter
        > Adjust if needed with small amounts of acid or base

        **Step 5 — Make up to volume**
        > Make up to **{total_vol:.0f} {vol_unit}** with distilled water
        > Check pH again after dilution

        **Step 6 — Final check**
        > Verify pH = **{desired_ph}**
        > Label with: buffer name, pH, concentration, date, initials

        **✅ Final Solution:** {total_conc} mol/L {selected_buffer}, pH {desired_ph}, {total_vol} {vol_unit}
        """)

        # ── Calculation Breakdown ──────────────────────────────────────────
        with st.expander("🔢 See Calculation Breakdown"):
            st.markdown(f"""
            **Step 1 — Find ratio using Henderson-Hasselbalch:**
            > [A⁻]/[HA] = 10^(pH - pKa) = 10^({desired_ph} - {pka}) = **{ratio:.4f}**

            **Step 2 — Find individual concentrations:**
            > [A⁻] (base) = {total_conc} × {ratio:.4f} / (1 + {ratio:.4f}) = **{conc_base:.6f} mol/L**
            > [HA] (acid)  = {total_conc} / (1 + {ratio:.4f}) = **{conc_acid:.6f} mol/L**

            **Step 3 — Find moles in {total_vol} {vol_unit}:**
            > moles of acid = {conc_acid:.6f} × {V:.4f} = **{moles_acid:.6f} mol**
            > moles of base = {conc_base:.6f} × {V:.4f} = **{moles_base:.6f} mol**

            **Step 4 — Convert to mass/volume:**
            > {acid['name']}: {moles_acid:.6f} × {acid['mw']} / {acid['purity']/100} = **{amount_acid:.4f} {acid_unit}**
            > {base['name']}: {moles_base:.6f} × {base['mw']} / {base['purity']/100} = **{amount_base:.4f} g**
            """)

        # ── Save to Experiment Log ─────────────────────────────────────────
        import datetime
        log_entry = {
            "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
            "module": "Buffer Preparation",
            "chemical": selected_buffer,
            "result": f"pH {desired_ph}, {total_conc} mol/L",
            "details": f"{acid['name']}: {amount_acid:.4f} {acid_unit} | {base['name']}: {amount_base:.4f} g"
        }
        if "experiment_log" not in st.session_state:
            st.session_state.experiment_log = []
        st.session_state.experiment_log.append(log_entry)
        st.caption("✅ Saved to Experiment Log")