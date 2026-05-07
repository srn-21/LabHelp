# -*- coding: utf-8 -*-
"""
Created on Fri May  8 03:30:44 2026

@author: shrn1
"""

import streamlit as st
import datetime

def show():
    st.title("📁 Experiment Log")
    st.markdown("*All your calculations saved automatically in one place*")
    st.markdown("---")

    # ── Initialize log if empty ────────────────────────────────────────────
    if "experiment_log" not in st.session_state:
        st.session_state.experiment_log = []

    log = st.session_state.experiment_log

    # ── Top Summary ────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Calculations", len(log))
    with col2:
        modules = list(set([e["module"].split("(")[0].strip() for e in log]))
        st.metric("Modules Used", len(modules))
    with col3:
        if log:
            st.metric("Last Calculation", log[-1]["timestamp"])
        else:
            st.metric("Last Calculation", "—")

    st.markdown("---")

    # ── Empty State ────────────────────────────────────────────────────────
    if not log:
        st.info("""
        📭 No calculations saved yet!

        Go to any calculator, run a calculation,
        and it will automatically appear here.
        """)
        return

    # ── Filter Options ─────────────────────────────────────────────────────
    st.markdown("### 🔍 Filter")
    col_f1, col_f2 = st.columns(2)

    with col_f1:
        all_modules = ["All Modules"] + list(set(
            [e["module"].split("(")[0].strip() for e in log]
        ))
        filter_module = st.selectbox("Filter by Module", all_modules)

    with col_f2:
        sort_order = st.radio("Sort", ["Newest First", "Oldest First"],
                              horizontal=True)

    # ── Apply Filter ───────────────────────────────────────────────────────
    filtered = log.copy()

    if filter_module != "All Modules":
        filtered = [e for e in filtered
                   if filter_module in e["module"]]

    if sort_order == "Newest First":
        filtered = list(reversed(filtered))

    st.markdown(f"**Showing {len(filtered)} of {len(log)} calculations**")
    st.markdown("---")

    # ── Display Log Entries ────────────────────────────────────────────────
    for i, entry in enumerate(filtered):
        with st.expander(
            f"🕐 {entry['timestamp']}  |  "
            f"📌 {entry['module']}  |  "
            f"✅ {entry['result']}"
        ):
            col_e1, col_e2 = st.columns(2)

            with col_e1:
                st.markdown(f"**🕐 Time:** {entry['timestamp']}")
                st.markdown(f"**📌 Module:** {entry['module']}")
                st.markdown(f"**🧪 Chemical:** {entry['chemical']}")
                st.markdown(f"**✅ Result:** {entry['result']}")
                st.markdown(f"**📋 Details:** {entry['details']}")

            with col_e2:
                # ── Add Note ───────────────────────────────────────────────
                note_key = f"note_{i}"
                existing_note = entry.get("note", "")
                note = st.text_area(
                    "📝 Add Note",
                    value=existing_note,
                    placeholder="e.g. For experiment #3, protein assay...",
                    key=note_key
                )
                if st.button("💾 Save Note", key=f"save_note_{i}"):
                    # Find original entry and update note
                    original_idx = log.index(entry) if entry in log else -1
                    if original_idx >= 0:
                        st.session_state.experiment_log[original_idx]["note"] = note
                        st.success("✅ Note saved!")

    st.markdown("---")

    # ── Actions ────────────────────────────────────────────────────────────
    st.markdown("### ⚙️ Actions")
    col_a1, col_a2, col_a3 = st.columns(3)

    with col_a1:
        if st.button("📋 Copy Log to Clipboard"):
            log_text = format_log_text(filtered)
            st.code(log_text)
            st.caption("Select all text above and copy!")

    with col_a2:
        if st.button("📄 Export as PDF"):
            pdf_path = export_pdf(filtered)
            if pdf_path:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name=f"LabHelp_Log_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf"
                    )

    with col_a3:
        if st.button("🗑️ Clear All Log", type="secondary"):
            st.session_state.experiment_log = []
            st.warning("⚠️ Log cleared!")
            st.rerun()


# ── Format Log as Text ─────────────────────────────────────────────────────
def format_log_text(log):
    lines = []
    lines.append("=" * 60)
    lines.append("LABHELP — EXPERIMENT LOG")
    lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)

    for i, entry in enumerate(log, 1):
        lines.append(f"\n[{i}] {entry['timestamp']}")
        lines.append(f"    Module   : {entry['module']}")
        lines.append(f"    Chemical : {entry['chemical']}")
        lines.append(f"    Result   : {entry['result']}")
        lines.append(f"    Details  : {entry['details']}")
        if entry.get("note"):
            lines.append(f"    Note     : {entry['note']}")
        lines.append("-" * 40)

    return "\n".join(lines)


# ── Export as PDF ──────────────────────────────────────────────────────────
def export_pdf(log):
    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()

        # ── Header ─────────────────────────────────────────────────────────
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 12, "LabHelp - Experiment Log", ln=True, align="C")

        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8,
                 f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
                 ln=True, align="C")
        pdf.cell(0, 8, f"Total Calculations: {len(log)}", ln=True, align="C")

        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        # ── Entries ────────────────────────────────────────────────────────
        for i, entry in enumerate(log, 1):
            # Entry header
            pdf.set_font("Arial", "B", 11)
            pdf.set_fill_color(230, 240, 255)
            pdf.cell(0, 8,
                     f"  [{i}]  {entry['timestamp']}  -  {entry['module']}",
                     ln=True, fill=True)

            # Entry details
            pdf.set_font("Arial", "", 10)
            pdf.set_x(15)
            pdf.cell(0, 7, f"Chemical : {entry['chemical'].replace('—', '-')}", ln=True)
            pdf.set_x(15)
            pdf.cell(0, 7, f"Result   : {entry['result']}", ln=True)
            pdf.set_x(15)

            # Handle long details text
            details = entry['details']
            if len(details) > 80:
                details = details[:80] + "..."
            pdf.cell(0, 7, f"Details  : {details.replace('—', '-')}", ln=True)

            if entry.get("note"):
                pdf.set_x(15)
                pdf.set_font("Arial", "I", 10)
                pdf.cell(0, 7, f"Note     : {entry['note']}", ln=True)

            pdf.ln(3)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)

            # New page if needed
            if pdf.get_y() > 260:
                pdf.add_page()

        # ── Save ───────────────────────────────────────────────────────────
        # ── Save ───────────────────────────────────────────────────────────
        import tempfile
        import os
        filename = f"LabHelp_Log_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        path = os.path.join(tempfile.gettempdir(), filename)
        pdf.output(path)
        return path

    except Exception as e:
        st.error(f"❌ PDF export failed: {e}")
        st.info("💡 Make sure fpdf2 is installed: pip install fpdf2")
        return None