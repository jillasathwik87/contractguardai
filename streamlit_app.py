
import streamlit as st

from contract_engine import (
    analyze_contract,
    extract_contracts_from_pdf,
    answer_question,
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ContractGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "Dashboard",
    "analysis": None,
    "uploaded_file": None,
    "available_contracts": [],
    "contract_documents": {},
    "selected_contract": "",
    "answer": None,
    "dark_mode": True,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CUSTOM STYLE
# ============================================================

if st.session_state.dark_mode:
    bg = "#0e1117"
    card = "#171b24"
    text = "#f5f7fb"
    muted = "#aeb6c5"
    border = "#2a3040"
else:
    bg = "#f7f9fc"
    card = "#ffffff"
    text = "#111827"
    muted = "#5f6b7a"
    border = "#dfe5ee"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {bg};
        color: {text};
    }}

    [data-testid="stSidebar"] {{
        background: {card};
        border-right: 1px solid {border};
    }}

    .brand {{
        padding: 10px 0 22px 4px;
    }}

    .brand-title {{
        font-size: 27px;
        font-weight: 800;
        margin-bottom: 3px;
    }}

    .brand-subtitle {{
        color: {muted};
        font-size: 13px;
    }}

    .hero {{
        background: linear-gradient(135deg, #18243b, #102b3f);
        border: 1px solid #263a55;
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 22px;
    }}

    .hero h1 {{
        margin: 0;
        font-size: 34px;
        color: white;
    }}

    .hero p {{
        color: #c9d6e8;
        font-size: 15px;
        margin-top: 8px;
    }}

    .section-card {{
        background: {card};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 18px;
    }}

    .small-muted {{
        color: {muted};
        font-size: 13px;
    }}

    .page-title {{
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 4px;
    }}

    .page-subtitle {{
        color: {muted};
        margin-bottom: 22px;
    }}

    div.stButton > button {{
        border-radius: 10px;
        min-height: 42px;
    }}

    .footer {{
        color: {muted};
        font-size: 12px;
        text-align: center;
        padding: 30px 0 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def go_to(page):
    st.session_state.page = page
    st.rerun()


def clear_contract():
    st.session_state.analysis = None
    st.session_state.uploaded_file = None
    st.session_state.available_contracts = []
    st.session_state.contract_documents = {}
    st.session_state.selected_contract = ""
    st.session_state.answer = None


def show_nav_button(label, page):
    if st.button(
        label,
        key=f"nav_{page}",
        use_container_width=True,
    ):
        go_to(page)


def show_compliance_overview(analysis):
    st.subheader("📊 Compliance Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Score", f"{analysis.get('score', 0)}%")

    with c2:
        st.metric("PASS", analysis.get("pass", 0))

    with c3:
        st.metric("MISSING", analysis.get("missing", 0))

    with c4:
        st.metric("FAIL", analysis.get("fail", 0))

    st.write(
        f"**Contract:** {analysis.get('contract_name', 'Uploaded Contract')}"
    )
    st.write(
        f"**Contract Type:** {analysis.get('contract_type', 'Unknown')}"
    )


def show_summary_and_checklist(analysis):
    st.divider()
    st.subheader("📝 Plain-English Summary")

    st.markdown(
        analysis.get("summary", "No summary available.")
    )

    st.divider()
    st.subheader("✅ Compliance Checklist")

    checklist = analysis.get("checklist", [])

    if not checklist:
        st.info("No checklist items were returned.")
        return

    for item in checklist:
        name = item.get("name", "Unknown")
        status = item.get("status", "UNKNOWN")
        description = item.get("description", "")

        if status == "PASS":
            st.success(f"✅ **{name}** — {description}")
        elif status == "MISSING":
            st.warning(f"⚠️ **{name}** — {description}")
        elif status == "FAIL":
            st.error(f"❌ **{name}** — {description}")
        else:
            st.info(f"ℹ️ **{name}** — {description}")


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-title">🛡️ ContractGuard AI</div>
            <div class="brand-subtitle">
                Contract Compliance Assistant
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("NAVIGATION")

    show_nav_button("🏠  Dashboard", "Dashboard")
    show_nav_button("📄  Upload Contract", "Upload Contract")
    show_nav_button("📑  My Contracts", "My Contracts")
    show_nav_button("💬  Ask AI", "Ask AI")
    show_nav_button("⚙️  Settings", "Settings")

    st.divider()

    if st.session_state.analysis:
        st.success("🟢 Contract analyzed")
    else:
        st.info("⚪ No contract analyzed")

    st.caption("ContractGuard AI")
    st.caption("⚖️ Not a substitute for legal advice.")


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>Welcome to ContractGuard AI</h1>
            <p>
                Analyze contracts, understand compliance requirements,
                and ask questions using plain English.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.analysis:
        analysis = st.session_state.analysis
        show_compliance_overview(analysis)

        st.divider()

        left, right = st.columns([2, 1])

        with left:
            st.subheader("📄 Current Contract")
            st.write(
                f"**{analysis.get('contract_name', 'Uploaded Contract')}**"
            )
            st.caption(
                analysis.get("contract_type", "Unknown contract type")
            )

        with right:
            if st.button(
                "📄 Upload Another Contract",
                type="primary",
                use_container_width=True,
                key="dashboard_upload",
            ):
                go_to("Upload Contract")

        st.divider()

        a, b, c = st.columns(3)

        with a:
            if st.button(
                "📝 View Analysis",
                use_container_width=True,
                key="dashboard_analysis",
            ):
                go_to("Upload Contract")

        with b:
            if st.button(
                "💬 Ask AI",
                use_container_width=True,
                key="dashboard_ai",
            ):
                go_to("Ask AI")

        with c:
            if st.button(
                "📑 My Contracts",
                use_container_width=True,
                key="dashboard_contracts",
            ):
                go_to("My Contracts")

    else:
        st.markdown(
            """
            <div class="section-card">
                <h3>📄 No contract analyzed yet</h3>
                <p class="small-muted">
                    Start by uploading a PDF contract. The analysis and
                    compliance results will appear on the Upload Contract page.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "📄 Upload Contract",
            type="primary",
            use_container_width=True,
            key="dashboard_start_upload",
        ):
            go_to("Upload Contract")

    st.markdown(
        """
        <div class="footer">
            ContractGuard AI — Contract Compliance Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# UPLOAD CONTRACT PAGE
# ============================================================

elif st.session_state.page == "Upload Contract":

    st.markdown(
        '<div class="page-title">📄 Upload Contract</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Upload a PDF and analyze it here. '
        'Your compliance results stay on this page.</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF contract",
        type=["pdf"],
        key="main_contract_uploader",
    )

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

        if st.button(
            "🔍 Analyze Contract",
            type="primary",
            use_container_width=True,
            key="upload_analyze_button",
        ):

            with st.spinner("Analyzing contract... Please wait."):

                try:
                    pdf_bytes = uploaded_file.getvalue()

                    contracts = extract_contracts_from_pdf(pdf_bytes)

                    if not contracts:
                        st.error("No contract text could be extracted from this PDF.")
                    elif len(contracts) > 1:
                        st.session_state.available_contracts = list(
                            contracts.keys()
                        )
                        st.session_state.contract_documents = contracts
                        st.session_state.analysis = None
                        st.session_state.answer = None

                        st.info(
                            "This PDF contains multiple contracts. "
                            "Select which contract you want to analyze."
                        )
                    else:
                        contract_name = list(contracts.keys())[0]
                        contract_text = contracts[contract_name]

                        data = analyze_contract(
                            contract_text,
                            contract_name,
                        )

                        st.session_state.analysis = data
                        st.session_state.available_contracts = []
                        st.session_state.contract_documents = contracts
                        st.session_state.selected_contract = contract_name
                        st.session_state.answer = None

                        st.success("✅ Contract analyzed successfully!")

                except Exception as e:
                    st.error(f"Contract analysis failed: {e}")

    # Multiple contract selector belongs to Upload page
    if st.session_state.available_contracts:

        st.divider()
        st.subheader("📑 Select a Contract")

        selected_contract = st.selectbox(
            "Contracts found in this PDF",
            st.session_state.available_contracts,
            key="upload_contract_selector",
        )

        if st.button(
            "📋 Analyze Selected Contract",
            type="primary",
            use_container_width=True,
            key="upload_selected_analyze",
        ):

            with st.spinner("Analyzing selected contract..."):

                try:
                    contract_text = st.session_state.contract_documents[
                        selected_contract
                    ]

                    data = analyze_contract(
                        contract_text,
                        selected_contract,
                    )

                    st.session_state.analysis = data
                    st.session_state.selected_contract = selected_contract
                    st.session_state.available_contracts = []
                    st.session_state.answer = None

                    st.success(
                        f"✅ {selected_contract} analyzed successfully!"
                    )

                except Exception as e:
                    st.error(f"Contract analysis failed: {e}")

    # Results stay on Upload Contract page
    if st.session_state.analysis:

        st.divider()
        show_compliance_overview(st.session_state.analysis)
        show_summary_and_checklist(st.session_state.analysis)

        st.divider()

        if st.button(
            "💬 Ask a Question About This Contract",
            use_container_width=True,
            key="upload_go_ai",
        ):
            go_to("Ask AI")


# ============================================================
# MY CONTRACTS PAGE
# ============================================================

elif st.session_state.page == "My Contracts":

    st.markdown(
        '<div class="page-title">📑 My Contracts</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Contracts available in this current session.</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.contract_documents:
        for name in st.session_state.contract_documents.keys():
            st.markdown(
                f"""
                <div class="section-card">
                    <h4>📄 {name}</h4>
                    <p class="small-muted">Loaded from the current PDF session.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    elif st.session_state.analysis:
        name = st.session_state.analysis.get(
            "contract_name",
            "Uploaded Contract",
        )
        st.markdown(
            f"""
            <div class="section-card">
                <h4>📄 {name}</h4>
                <p class="small-muted">
                    This contract has been analyzed in the current session.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info(
            "No contracts in the current session. "
            "Go to Upload Contract to add one."
        )

    if st.button(
        "📄 Upload Contract",
        type="primary",
        use_container_width=True,
        key="contracts_upload",
    ):
        go_to("Upload Contract")


# ============================================================
# ASK AI PAGE
# ============================================================

elif st.session_state.page == "Ask AI":

    st.markdown(
        '<div class="page-title">💬 Ask AI</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Ask questions about the analyzed contract '
        'and get the relevant source clause.</div>',
        unsafe_allow_html=True,
    )

    analysis = st.session_state.analysis

    if not analysis:
        st.info(
            "Please analyze a contract first from the Upload Contract page."
        )

        if st.button(
            "📄 Go to Upload Contract",
            type="primary",
            use_container_width=True,
            key="ai_upload",
        ):
            go_to("Upload Contract")
    else:
        st.success(
            f"Using: {analysis.get('contract_name', 'Analyzed Contract')}"
        )

        question = st.text_area(
            "Your question",
            placeholder=(
                "Example: What is the confidentiality period?"
            ),
            height=120,
            key="ai_question",
        )

        if st.button(
            "🤖 Ask AI",
            type="primary",
            use_container_width=True,
            key="ask_ai_button",
        ):

            if not question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner(
                    "Searching the contract and generating an answer..."
                ):
                    try:
                        data = answer_question(
                            question,
                            analysis.get("contract_text", ""),
                            analysis.get("clauses", []),
                        )

                        if data.get("success"):
                            st.session_state.answer = data
                        else:
                            st.error(
                                data.get(
                                    "error",
                                    "Could not answer the question.",
                                )
                            )

                    except Exception as e:
                        st.error(f"Error generating answer: {e}")

        if st.session_state.answer:
            answer_data = st.session_state.answer

            st.divider()
            st.subheader("🤖 Answer")

            st.write(
                answer_data.get(
                    "answer",
                    "No answer available.",
                )
            )

            source_clause = answer_data.get(
                "source_clause",
                "",
            )

            if source_clause:
                st.subheader("📌 Source Clause")
                st.code(source_clause, language="text")
                st.caption(
                    "The answer was generated using the retrieved "
                    "contract clause shown above."
                )


# ============================================================
# SETTINGS PAGE
# ============================================================

elif st.session_state.page == "Settings":

    st.markdown(
        '<div class="page-title">⚙️ Settings</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Customize your ContractGuard AI experience.</div>',
        unsafe_allow_html=True,
    )

    st.subheader("🎨 Appearance")

    dark_mode = st.toggle(
        "Dark mode",
        value=st.session_state.dark_mode,
        key="settings_dark_mode",
    )

    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

    st.caption(
        "Dark mode changes the dashboard appearance. "
        "Your contract data and analysis are not affected."
    )

    st.divider()

    st.subheader("🧹 Session Data")

    if st.button(
        "Clear Current Contract & Session",
        use_container_width=True,
        key="settings_clear",
    ):
        clear_contract()
        st.success("Current contract data has been cleared.")
        st.rerun()

    st.divider()

    st.subheader("ℹ️ About ContractGuard AI")

    st.write(
        "ContractGuard AI analyzes uploaded contracts, generates "
        "plain-English explanations, checks compliance rules, and "
        "answers questions using retrieved contract clauses."
    )

    st.warning(
        "⚖️ ContractGuard AI is an assistance tool and is not a substitute "
        "for review by a licensed lawyer."
    )

    st.divider()

    st.subheader("🟢 Application Status")
    st.success("ContractGuard AI engine is available.")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ContractGuard AI — Contract Compliance Assistant"
)
st.caption(
    "⚖️ Not a substitute for a licensed lawyer's review."
)
