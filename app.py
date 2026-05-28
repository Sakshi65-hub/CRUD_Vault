import streamlit as st
from pathlib import Path
import os
import time

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FileVault",
    page_icon="🗂️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg:       #0d0f14;
    --surface:  #141720;
    --border:   #232738;
    --accent:   #5cffb1;
    --accent2:  #3d7fff;
    --danger:   #ff4f6d;
    --warn:     #ffb347;
    --text:     #e8eaf0;
    --muted:    #6b7194;
    --radius:   14px;
}

/* ── Global Reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }

/* ── Hero Banner ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 70% 50% at 50% 0%, rgba(92,255,177,.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 6vw, 4rem);
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 .5rem;
    line-height: 1;
}
.hero-sub {
    font-size: .85rem;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 0;
}

/* ── Op Cards (4 across) ── */
.op-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 2rem 0 2.5rem;
}
.op-card {
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem .8rem;
    text-align: center;
    cursor: pointer;
    transition: all .25s ease;
    background: var(--surface);
    position: relative;
    overflow: hidden;
}
.op-card::after {
    content: '';
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity .25s;
    border-radius: inherit;
}
.op-card.create::after { background: rgba(92,255,177,.07); }
.op-card.read::after   { background: rgba(61,127,255,.07); }
.op-card.update::after { background: rgba(255,179,71,.07); }
.op-card.delete::after { background: rgba(255,79,109,.07); }
.op-card:hover::after  { opacity: 1; }

.op-card.create { border-color: rgba(92,255,177,.35); }
.op-card.read   { border-color: rgba(61,127,255,.35); }
.op-card.update { border-color: rgba(255,179,71,.35); }
.op-card.delete { border-color: rgba(255,79,109,.35); }

.op-icon { font-size: 1.8rem; display: block; margin-bottom: .5rem; }
.op-label {
    font-family: 'Syne', sans-serif;
    font-size: .8rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.op-card.create .op-label { color: var(--accent); }
.op-card.read   .op-label { color: var(--accent2); }
.op-card.update .op-label { color: var(--warn); }
.op-card.delete .op-label { color: var(--danger); }

/* ── Panel ── */
.panel {
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    background: var(--surface);
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
}
.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 1.2rem;
    display: flex;
    align-items: center;
    gap: .6rem;
}

/* ── Inputs ── */
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stRadio"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: .78rem !important;
    color: var(--muted) !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #0d0f14 !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .92rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(92,255,177,.12) !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    width: 100%;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    font-size: .85rem !important;
    padding: .65rem 1rem !important;
    transition: all .2s ease !important;
    border: none !important;
}
.create-btn [data-testid="stButton"] > button {
    background: linear-gradient(135deg, #5cffb1, #3aefaa) !important;
    color: #0d0f14 !important;
}
.read-btn [data-testid="stButton"] > button {
    background: linear-gradient(135deg, #3d7fff, #2260e0) !important;
    color: #fff !important;
}
.update-btn [data-testid="stButton"] > button {
    background: linear-gradient(135deg, #ffb347, #e89530) !important;
    color: #0d0f14 !important;
}
.delete-btn [data-testid="stButton"] > button {
    background: linear-gradient(135deg, #ff4f6d, #e0324e) !important;
    color: #fff !important;
}

/* ── Output Box ── */
.output-box {
    background: #080a0f;
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    font-family: 'DM Mono', monospace;
    font-size: .88rem;
    line-height: 1.7;
    white-space: pre-wrap;
    color: var(--text);
    min-height: 80px;
    margin-top: 1rem;
    position: relative;
}
.output-box .tag {
    font-size: .7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--muted);
    margin-bottom: .5rem;
    display: block;
}

/* ── Alerts ── */
.alert {
    border-radius: 10px;
    padding: .9rem 1.2rem;
    font-size: .88rem;
    margin-top: .8rem;
    border-left: 4px solid;
    display: flex;
    align-items: center;
    gap: .6rem;
}
.alert.success { background: rgba(92,255,177,.08); border-color: var(--accent); color: var(--accent); }
.alert.error   { background: rgba(255,79,109,.08); border-color: var(--danger); color: var(--danger); }
.alert.info    { background: rgba(61,127,255,.08); border-color: var(--accent2); color: var(--accent2); }

/* ── File List ── */
.file-pill {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: .3rem .7rem;
    font-size: .8rem;
    margin: .3rem;
    color: var(--muted);
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* ── Radio ── */
[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 10px !important;
}
[data-testid="stRadio"] label {
    background: #0d0f14;
    border: 1.5px solid var(--border);
    border-radius: 8px;
    padding: .5rem .9rem;
    cursor: pointer;
    transition: border-color .2s;
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: .9rem !important;
    color: var(--text) !important;
}
[data-testid="stRadio"] label:has(input:checked) {
    border-color: var(--warn) !important;
    background: rgba(255,179,71,.07) !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    font-size: .75rem;
    color: var(--muted);
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State ───────────────────────────────────────────────────────────
if "active_op" not in st.session_state:
    st.session_state.active_op = "Create"


# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-title">FileVault</p>
    <p class="hero-sub">⚡ File Management System &nbsp;·&nbsp; Python + Streamlit</p>
</div>
""", unsafe_allow_html=True)


# ─── Operation Selector (tabs styled as cards) ───────────────────────────────
ops = ["Create", "Read", "Update", "Delete"]
icons = {"Create": "✦", "Read": "◈", "Update": "⟳", "Delete": "✕"}
cls   = {"Create": "create", "Read": "read", "Update": "update", "Delete": "delete"}

tab1, tab2, tab3, tab4 = st.tabs(["✦  Create", "◈  Read", "⟳  Update", "✕  Delete"])


# ═══════════════════════════════════════════════════════════════════════════════
# CREATE
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title"><span style="color:var(--accent)">✦</span>&nbsp; Create New File</p>', unsafe_allow_html=True)

    filename = st.text_input("File Name", placeholder="e.g.  notes.txt", key="c_name")
    content  = st.text_area("Content", placeholder="Start writing your file content here...", height=160, key="c_content")

    st.markdown('<div class="create-btn">', unsafe_allow_html=True)
    if st.button("Create File", key="create_btn"):
        if not filename.strip():
            st.markdown('<div class="alert error">⚠ Please enter a file name.</div>', unsafe_allow_html=True)
        else:
            path = Path(filename.strip())
            if path.exists():
                st.markdown(f'<div class="alert error">✕ &nbsp;<code>{filename}</code> already exists.</div>', unsafe_allow_html=True)
            else:
                try:
                    with open(path, "w") as f:
                        f.write(content)
                    st.markdown(f'<div class="alert success">✓ &nbsp;<code>{filename}</code> created successfully — {len(content)} chars written.</div>', unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.markdown(f'<div class="alert error">✕ &nbsp;{e}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# READ
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title"><span style="color:var(--accent2)">◈</span>&nbsp; Read File</p>', unsafe_allow_html=True)

    filename_r = st.text_input("File Name", placeholder="e.g.  notes.txt", key="r_name")

    st.markdown('<div class="read-btn">', unsafe_allow_html=True)
    if st.button("Read File", key="read_btn"):
        if not filename_r.strip():
            st.markdown('<div class="alert error">⚠ Please enter a file name.</div>', unsafe_allow_html=True)
        else:
            path = Path(filename_r.strip())
            if not path.exists():
                st.markdown(f'<div class="alert error">✕ &nbsp;<code>{filename_r}</code> does not exist.</div>', unsafe_allow_html=True)
            else:
                try:
                    content = path.read_text()
                    size    = path.stat().st_size
                    lines   = content.count('\n') + 1
                    st.markdown(f'<div class="alert info">◈ &nbsp;<code>{filename_r}</code> · {size} bytes · {lines} lines</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="output-box"><span class="tag">— file content —</span>{content if content else "<em style=\'color:var(--muted)\'>Empty file</em>"}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="alert error">✕ &nbsp;{e}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# UPDATE
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title"><span style="color:var(--warn)">⟳</span>&nbsp; Update File</p>', unsafe_allow_html=True)

    filename_u = st.text_input("File Name", placeholder="e.g.  notes.txt", key="u_name")
    operation  = st.radio(
        "Operation",
        ["Rename", "Append Content", "Overwrite Content"],
        horizontal=True,
        key="u_op"
    )

    if operation == "Rename":
        new_name = st.text_input("New File Name", placeholder="e.g.  renamed.txt", key="u_newname")
    else:
        new_data = st.text_area(
            "Content to " + ("append" if operation == "Append Content" else "overwrite with"),
            height=130,
            key="u_data"
        )

    st.markdown('<div class="update-btn">', unsafe_allow_html=True)
    if st.button("Apply Update", key="update_btn"):
        if not filename_u.strip():
            st.markdown('<div class="alert error">⚠ Please enter a file name.</div>', unsafe_allow_html=True)
        else:
            path = Path(filename_u.strip())
            if not path.exists():
                st.markdown(f'<div class="alert error">✕ &nbsp;<code>{filename_u}</code> does not exist.</div>', unsafe_allow_html=True)
            else:
                try:
                    if operation == "Rename":
                        if not new_name.strip():
                            st.markdown('<div class="alert error">⚠ Please enter a new file name.</div>', unsafe_allow_html=True)
                        else:
                            new_path = Path(new_name.strip())
                            if new_path.exists():
                                st.markdown(f'<div class="alert error">✕ &nbsp;<code>{new_name}</code> already exists.</div>', unsafe_allow_html=True)
                            else:
                                path.rename(new_path)
                                st.markdown(f'<div class="alert success">✓ &nbsp;Renamed to <code>{new_name}</code> successfully.</div>', unsafe_allow_html=True)
                    elif operation == "Append Content":
                        with open(path, "a") as f:
                            f.write("\n" + new_data)
                        st.markdown(f'<div class="alert success">✓ &nbsp;Content appended to <code>{filename_u}</code>.</div>', unsafe_allow_html=True)
                    else:
                        with open(path, "w") as f:
                            f.write(new_data)
                        st.markdown(f'<div class="alert success">✓ &nbsp;<code>{filename_u}</code> overwritten successfully.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="alert error">✕ &nbsp;{e}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DELETE
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title"><span style="color:var(--danger)">✕</span>&nbsp; Delete File</p>', unsafe_allow_html=True)

    filename_d = st.text_input("File Name", placeholder="e.g.  notes.txt", key="d_name")
    confirm    = st.checkbox("I understand this action is **permanent** and cannot be undone", key="d_confirm")

    st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
    if st.button("Delete File", key="delete_btn"):
        if not filename_d.strip():
            st.markdown('<div class="alert error">⚠ Please enter a file name.</div>', unsafe_allow_html=True)
        elif not confirm:
            st.markdown('<div class="alert error">⚠ Please confirm the deletion checkbox first.</div>', unsafe_allow_html=True)
        else:
            path = Path(filename_d.strip())
            if not path.exists():
                st.markdown(f'<div class="alert error">✕ &nbsp;<code>{filename_d}</code> does not exist.</div>', unsafe_allow_html=True)
            else:
                try:
                    path.unlink()
                    st.markdown(f'<div class="alert success">✓ &nbsp;<code>{filename_d}</code> deleted successfully.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="alert error">✕ &nbsp;{e}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── Files in current directory ──────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<p style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:.85rem;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:.8rem;">📂 &nbsp;Files in Working Directory</p>', unsafe_allow_html=True)

files = [f for f in Path(".").iterdir() if f.is_file()]
if files:
    pills = "".join(f'<span class="file-pill">📄 {f.name}</span>' for f in sorted(files))
    st.markdown(pills, unsafe_allow_html=True)
else:
    st.markdown('<p style="color:var(--muted);font-size:.85rem;">No files yet — create one above!</p>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with Python &amp; Streamlit &nbsp;·&nbsp; FileVault v1.0
</div>
""", unsafe_allow_html=True)
