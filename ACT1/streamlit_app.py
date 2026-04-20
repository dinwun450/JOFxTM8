import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import html

st.set_page_config(page_title="Nagoro Skirmish - Casualty Report", layout="wide")

STATUS_COLORS = {
    "Online": "#29B5E8",
    "Unknown": "#D45B90",
    "Injured": "#FF9F36",
    "Offline": "#8A999E",
}

st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #E0E0E0;
        padding: 0.6rem 0 0.2rem;
    }
    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #888;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #2a2a4a;
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
    }
    .metric-card h2 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .metric-card p {
        margin: 0.3rem 0 0;
        font-size: 0.85rem;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #ccc;
        border-bottom: 2px solid #333;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #2a2a4a;
        border-radius: 10px;
        overflow: hidden;
    }
    .lore-block {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #2a2a4a;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        line-height: 1.7;
        color: #ccc;
        white-space: pre-wrap;
        font-family: 'Courier New', 'Fira Code', monospace;
        font-size: 0.85rem;
    }
    .lore-file-title {
        font-size: 1rem;
        font-weight: 700;
        color: #E0E0E0;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

session = get_active_session()

with st.sidebar:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d0d1a 0%, #1a1a2e 40%, #16213e 100%);
            border-right: 1px solid #2a2a4a;
        }
        .sidebar-title {
            text-align: center;
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #E0E0E0;
            padding: 1.2rem 0 0.2rem;
        }
        .sidebar-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #4a4a6a, transparent);
            margin: 0.8rem 1rem;
        }
        .sidebar-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #666;
            padding: 0 0.5rem;
            margin-bottom: 0.5rem;
        }
        div[data-testid="stSidebar"] button[kind="secondary"] {
            background: transparent;
            border: 1px solid #2a2a4a;
            border-radius: 10px;
            color: #aaa;
            width: 100%;
            padding: 0.6rem 1rem;
            text-align: left;
            transition: all 0.2s ease;
            margin-bottom: 0.3rem;
        }
        div[data-testid="stSidebar"] button[kind="secondary"]:hover {
            background: rgba(255,255,255,0.05);
            border-color: #4a4a6a;
            color: #E0E0E0;
        }
        div[data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(135deg, #1e3a5f, #2a5298);
            border: 1px solid #3a6ad4;
            border-radius: 10px;
            color: #fff;
            width: 100%;
            padding: 0.6rem 1rem;
            text-align: left;
            font-weight: 600;
            margin-bottom: 0.3rem;
        }
        .sidebar-footer {
            position: fixed;
            bottom: 1rem;
            font-size: 0.7rem;
            color: #444;
            text-align: center;
            width: 100%;
            letter-spacing: 1px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-title">Nagoro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Sections</div>', unsafe_allow_html=True)

    pages = {
        "casualties": "Casualties & Motives",
        "lore": "Lore",
    }

    if "page" not in st.session_state:
        st.session_state.page = "casualties"

    for key, label in pages.items():
        btn_type = "primary" if st.session_state.page == key else "secondary"
        if st.button(label, key=f"nav_{key}", type=btn_type, use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-footer">TME_DB &middot; ACT 1</div>', unsafe_allow_html=True)

page = st.session_state.page

if page == "casualties":
    st.markdown('<div class="main-title">Battle of Nagoro</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Snowflaker Casualty &amp; Status Report</div>',
        unsafe_allow_html=True,
    )

    df = session.sql("SELECT * FROM TME_DB.ACT1.BATTLE_OF_NAGORO_STATS").to_pandas()

    total = len(df)
    online = len(df[df["STATUS"] == "Online"])
    unknown = len(df[df["STATUS"] == "Unknown"])
    injured = len(df[df["STATUS"] == "Injured"])
    offline = len(df[df["STATUS"] == "Offline"])

    metrics = [
        (total, "Total Personnel", "#E0E0E0"),
        (online, "Online", STATUS_COLORS["Online"]),
        (unknown, "Unknown / Vaporized", STATUS_COLORS["Unknown"]),
        (injured, "Injured", STATUS_COLORS["Injured"]),
        (offline, "Offline", STATUS_COLORS["Offline"]),
    ]

    cols = st.columns(len(metrics))
    for col, (val, label, color) in zip(cols, metrics):
        col.markdown(
            f"""
            <div class="metric-card">
                <h2 style="color:{color}">{val}</h2>
                <p>{label}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-header">Casualties by Status</div>', unsafe_allow_html=True)
        status_counts = df.groupby("STATUS").size().reset_index(name="COUNT")
        status_order = ["Online", "Injured", "Unknown", "Offline"]
        status_counts["STATUS"] = pd.Categorical(status_counts["STATUS"], categories=status_order, ordered=True)
        status_counts = status_counts.sort_values("STATUS")
        st.vega_lite_chart(
            status_counts,
            {
                "mark": {"type": "bar", "cornerRadiusTopLeft": 6, "cornerRadiusTopRight": 6},
                "encoding": {
                    "x": {"field": "STATUS", "type": "nominal", "sort": status_order, "title": "Status"},
                    "y": {"field": "COUNT", "type": "quantitative", "title": "Count"},
                    "color": {
                        "field": "STATUS",
                        "type": "nominal",
                        "scale": {
                            "domain": list(STATUS_COLORS.keys()),
                            "range": list(STATUS_COLORS.values()),
                        },
                        "legend": None,
                    },
                },
            },
            use_container_width=True,
        )

    with right:
        st.markdown('<div class="section-header">Breakdown by Role</div>', unsafe_allow_html=True)
        role_status = df.groupby(["ROLE", "STATUS"]).size().reset_index(name="COUNT")
        st.vega_lite_chart(
            role_status,
            {
                "mark": {"type": "bar", "cornerRadiusTopLeft": 6, "cornerRadiusTopRight": 6},
                "encoding": {
                    "x": {"field": "ROLE", "type": "nominal", "title": "Role"},
                    "y": {"field": "COUNT", "type": "quantitative", "title": "Count"},
                    "color": {
                        "field": "STATUS",
                        "type": "nominal",
                        "scale": {
                            "domain": list(STATUS_COLORS.keys()),
                            "range": list(STATUS_COLORS.values()),
                        },
                    },
                    "xOffset": {"field": "STATUS", "type": "nominal"},
                },
            },
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Personnel Roster</div>', unsafe_allow_html=True)

    col_search, col_role, col_status = st.columns([2, 1, 1])
    with col_search:
        search = st.text_input("Search by Name or ID", placeholder="e.g. Mayeria or SFL-04")
    with col_role:
        roles = st.multiselect("Role", options=sorted(df["ROLE"].unique()), default=sorted(df["ROLE"].unique()))
    with col_status:
        statuses = st.multiselect("Status", options=sorted(df["STATUS"].unique()), default=sorted(df["STATUS"].unique()))

    filtered = df[(df["ROLE"].isin(roles)) & (df["STATUS"].isin(statuses))].copy()
    if search:
        mask = filtered["NAME"].str.contains(search, case=False, na=False) | filtered["SF_ID"].str.contains(search, case=False, na=False)
        filtered = filtered[mask]

    st.dataframe(
        filtered[["SF_ID", "NAME", "ROLE", "STATUS", "DESCRIPTION"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "SF_ID": st.column_config.TextColumn("ID", width="small"),
            "NAME": st.column_config.TextColumn("Name", width="medium"),
            "ROLE": st.column_config.TextColumn("Role", width="medium"),
            "STATUS": st.column_config.TextColumn("Status", width="small"),
            "DESCRIPTION": st.column_config.TextColumn("Details", width="large"),
        },
    )

    st.caption(f"Showing {len(filtered)} of {len(df)} personnel")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Ariya\'s Motives — Intelligence Report</div>', unsafe_allow_html=True)

    with session.file.get_stream("@TME_DB.ACT1.NAGOROFILES/ariya_intelligence_theories.txt") as f:
        ariya_contents = f.read().decode("utf-8")
    st.markdown(f'<div class="lore-block">{html.escape(ariya_contents)}</div>', unsafe_allow_html=True)

elif page == "lore":
    st.markdown('<div class="main-title">Act 1 — Lore</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">The story behind Jino &amp; Friends x Tokyo Magnitude 8</div>',
        unsafe_allow_html=True,
    )

    lore_files = [
        ("@TME_DB.ACT1.ACT1_LORE/jino_and_friends_x_tokyo_magnitude_8_ep1_prelude.txt", "Episode 1 — Prelude"),
        ("@TME_DB.ACT1.ACT1_LORE/jino_and_friends_x_tokyo_magnitude_8_ep1.txt", "Episode 1"),
    ]

    for stage_path, title in lore_files:
        with session.file.get_stream(stage_path) as f:
            text = f.read().decode("utf-8")
        st.markdown(f'<div class="lore-file-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="lore-block">{html.escape(text)}</div>', unsafe_allow_html=True)
