import streamlit as st

st.set_page_config(
    page_title="Barter Club Hub",
    page_icon="🔁",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
defaults = {
    "current_user": None,
    "current_account_type": None,
    "creator_accounts": {},
    "business_accounts": {},
    "connections": [],
    "selected_target": "Creators",
    "auth_page": "login",
    "signup_role": "Creator",
    "forced_page": None,
    "barter_posts": [
        {
            "owner_name": "EloiseKNYC",
            "account_type": "Creator",
            "target_type": "Business",
            "offer": "TikTok Post",
            "want": "Beauty Products",
            "location": "New York, NY",
            "bio": "NYC creator focused on lifestyle, family finds, and local gems."
        },
        {
            "owner_name": "Glow Studio",
            "account_type": "Business",
            "target_type": "Creator",
            "offer": "Beauty Products",
            "want": "Instagram Reel",
            "location": "Miami, FL",
            "bio": "Beauty brand looking for creators to feature our products."
        },
        {
            "owner_name": "Street Social",
            "account_type": "Business",
            "target_type": "Business",
            "offer": "Clothing",
            "want": "Accessories",
            "location": "Los Angeles, CA",
            "bio": "Streetwear label open to product-based brand exchanges."
        },
        {
            "owner_name": "Creator Jay",
            "account_type": "Creator",
            "target_type": "Creator",
            "offer": "UGC Content",
            "want": "Clothing",
            "location": "Chicago, IL",
            "bio": "Lifestyle creator open to creator-to-creator swaps."
        }
    ]
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# CONSTANTS
# -----------------------------
offer_options = [
    "TikTok Post",
    "Instagram Reel",
    "UGC Content",
    "Brand Exposure",
    "Clothing",
    "Beauty Products",
    "Accessories",
    "Physical Goods"
]

creator_platforms = ["TikTok", "Instagram", "YouTube", "Other"]
business_store_types = ["Online Store", "Brick & Mortar", "Both", "Other"]
connection_options = ["Creators", "Businesses", "Both"]

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.auth-wrap {
    max-width: 460px;
    margin: 0 auto;
    padding-top: 1rem;
}

.logo-box {
    text-align: center;
    margin-bottom: 1.25rem;
}

.logo-box h1 {
    margin-bottom: 0.25rem;
}

.logo-box p {
    color: #94a3b8;
    margin-top: 0;
}

.auth-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
}

.soft-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 16px;
}

.card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.match-card {
    background: linear-gradient(180deg, #111827 0%, #0b1220 100%);
    border: 1px solid #1f2937;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 8px 26px rgba(0,0,0,0.18);
}

.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 10px;
}

.muted {
    color: #94a3b8;
    font-size: 0.95rem;
}

.big-stat {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 18px;
    padding: 16px;
    text-align: center;
}

.big-stat h3 {
    margin: 0;
    font-size: 1.8rem;
}

.big-stat p {
    margin: 6px 0 0 0;
    color: #94a3b8;
    font-size: 0.9rem;
}

.step-card {
    background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
    border: 1px solid #1f2937;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 18px;
}

.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: #1e293b;
    border: 1px solid #334155;
    font-size: 0.8rem;
    color: #cbd5e1;
    margin-bottom: 10px;
}

.score-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: #172554;
    border: 1px solid #1d4ed8;
    color: #dbeafe;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 12px;
}

.reason-box {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 12px;
    margin-top: 14px;
    margin-bottom: 14px;
}

.cta-box {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 18px;
    margin-top: 12px;
}

.filter-box {
    background: #0b1220;
    border: 1px solid #1f2937;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HELPERS
# -----------------------------
def get_current_profile():
    if not st.session_state.current_user or not st.session_state.current_account_type:
        return None

    if st.session_state.current_account_type == "Creator":
        return st.session_state.creator_accounts.get(st.session_state.current_user)
    return st.session_state.business_accounts.get(st.session_state.current_user)

def login_user(username, account_type):
    st.session_state.current_user = username
    st.session_state.current_account_type = account_type

def logout_user():
    st.session_state.current_user = None
    st.session_state.current_account_type = None
    st.session_state.auth_page = "login"

def get_user_connections(current_name):
    return [
        c for c in st.session_state.connections
        if c["from"] == current_name or c["to"] == current_name
    ]

def score_match(profile, post, target_connection):
    score = 0
    reasons = []

    target_account_type = "Creator" if target_connection == "Creators" else "Business"
    if post["account_type"] == target_account_type:
        score += 25
        reasons.append(f"They are a {target_account_type.lower()}, which matches your selected lane.")

    if post["offer"] == profile["primary_want"]:
        score += 35
        reasons.append(f"They offer {post['offer']}, which matches what you want.")

    if post["want"] == profile["primary_offer"]:
        score += 35
        reasons.append(f"They want {post['want']}, which matches what you offer.")

    if post["offer"] == profile["primary_want"] and post["want"] == profile["primary_offer"]:
        score += 5
        reasons.append("This is a strong two-way barter fit.")

    return score, reasons

def get_matches(profile, target_connection, min_score=25):
    matches = []

    for post in st.session_state.barter_posts:
        if post["owner_name"] == profile["display_name"]:
            continue

        if target_connection == "Both":
            role_match = True
        else:
            target_account_type = "Creator" if target_connection == "Creators" else "Business"
            role_match = post["account_type"] == target_account_type

        score = 0
        reasons = []

        if role_match:
            score += 25
            if target_connection == "Both":
                reasons.append(f"They are a {post['account_type'].lower()}, and you’re open to both account types.")
            else:
                reasons.append(f"They are a {post['account_type'].lower()}, which matches your selected lane.")

        if post["offer"] == profile["primary_want"]:
            score += 35
            reasons.append(f"They offer {post['offer']}, which matches what you want.")

        if post["want"] == profile["primary_offer"]:
            score += 35
            reasons.append(f"They want {post['want']}, which matches what you offer.")

        if post["offer"] == profile["primary_want"] and post["want"] == profile["primary_offer"]:
            score += 5
            reasons.append("This is a strong two-way barter fit.")

        if score >= min_score:
            enriched = post.copy()
            enriched["match_score"] = score
            enriched["why_match"] = reasons
            matches.append(enriched)

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches

def render_match_card(match, idx):
    st.markdown(f"""
    <div class="match-card">
        <div class="score-badge">Match Score: {match['match_score']}%</div>
        <div class="section-title">{match['owner_name']}</div>
        <div class="muted">{match['account_type']} • {match['location']}</div>
        <br>
        <strong>Bio:</strong> {match['bio']}<br><br>
        <strong>Offers:</strong> {match['offer']}<br>
        <strong>Wants:</strong> {match['want']}
        <div class="reason-box">
            <strong>Why this match fits:</strong><br>
            {"<br>".join([f"• {reason}" for reason in match["why_match"]])}
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# AUTH SCREENS
# -----------------------------
profile = get_current_profile()

if not profile:
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="logo-box">
        <h1>Barter Club Hub 🔁</h1>
        <p>A curated platform for creators and businesses to exchange value.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.auth_page == "login":
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.subheader("Log In")

        login_account_type = st.selectbox("Account Type", ["Creator", "Business"])
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type="password")

        if st.button("Log In", use_container_width=True):
            if login_account_type == "Creator":
                if login_username in st.session_state.creator_accounts:
                    saved = st.session_state.creator_accounts[login_username]
                    if saved["password"] == login_password:
                        login_user(login_username, "Creator")
                        st.rerun()
                    else:
                        st.error("Wrong password.")
                else:
                    st.error("Creator account not found.")
            else:
                if login_username in st.session_state.business_accounts:
                    saved = st.session_state.business_accounts[login_username]
                    if saved["password"] == login_password:
                        login_user(login_username, "Business")
                        st.rerun()
                    else:
                        st.error("Wrong password.")
                else:
                    st.error("Business account not found.")

        st.markdown("---")
        if st.button("Create Account", use_container_width=True):
            st.session_state.auth_page = "signup"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.auth_page == "signup":
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.subheader("Create Account")

        signup_role = st.radio("Choose Account Type", ["Creator", "Business"])
        st.session_state.signup_role = signup_role

        if signup_role == "Creator":
            st.info("Creator accounts have a faster sign-up process.")

            creator_username = st.text_input("Username", key="creator_username")
            creator_password = st.text_input("Password", type="password", key="creator_password")
            creator_display_name = st.text_input("Creator Name / Brand", key="creator_display_name")
            creator_location = st.text_input("Location", key="creator_location")
            creator_bio = st.text_area("Short Bio", key="creator_bio")
            creator_platform = st.selectbox("Main Platform", creator_platforms, key="creator_platform")
            creator_audience_size = st.text_input("Audience Size", key="creator_audience_size")
            creator_offer = st.selectbox("Primary Offer", offer_options, key="creator_offer")
            creator_want = st.selectbox("Primary Want", offer_options, key="creator_want")

            if st.button("Create Creator Account", use_container_width=True):
                if not creator_username or not creator_password or not creator_display_name:
                    st.error("Fill in username, password, and creator name.")
                elif creator_username in st.session_state.creator_accounts:
                    st.error("That creator username already exists.")
                else:
                    st.session_state.creator_accounts[creator_username] = {
                        "username": creator_username,
                        "password": creator_password,
                        "display_name": creator_display_name,
                        "account_type": "Creator",
                        "location": creator_location,
                        "bio": creator_bio,
                        "main_platform": creator_platform,
                        "audience_size": creator_audience_size,
                        "primary_offer": creator_offer,
                        "primary_want": creator_want,
                        "verification_status": "Not Required"
                    }
                    login_user(creator_username, "Creator")
                    st.rerun()

        else:
            st.warning("Business accounts are reviewed more carefully on Barter Club Hub.")

            business_username = st.text_input("Username", key="business_username")
            business_password = st.text_input("Password", type="password", key="business_password")
            business_display_name = st.text_input("Business Name", key="business_display_name")
            business_location = st.text_input("Business Location", key="business_location")
            business_bio = st.text_area("Business Bio", key="business_bio")
            business_website = st.text_input("Website", key="business_website")
            business_email = st.text_input("Business Email", key="business_email")
            business_store_type = st.selectbox("Store Type", business_store_types, key="business_store_type")
            business_offer = st.selectbox("Primary Offer", offer_options, key="business_offer")
            business_want = st.selectbox("Primary Want", offer_options, key="business_want")

            st.caption("Businesses should have a real online presence and identifiable contact details.")

            if st.button("Create Business Account", use_container_width=True):
                if not business_username or not business_password or not business_display_name:
                    st.error("Fill in username, password, and business name.")
                elif not business_website or not business_email:
                    st.error("Business accounts require a website and business email.")
                elif business_username in st.session_state.business_accounts:
                    st.error("That business username already exists.")
                else:
                    st.session_state.business_accounts[business_username] = {
                        "username": business_username,
                        "password": business_password,
                        "display_name": business_display_name,
                        "account_type": "Business",
                        "location": business_location,
                        "bio": business_bio,
                        "website": business_website,
                        "business_email": business_email,
                        "store_type": business_store_type,
                        "primary_offer": business_offer,
                        "primary_want": business_want,
                        "verification_status": "Pending Review"
                    }
                    login_user(business_username, "Business")
                    st.rerun()

        st.markdown("---")
        if st.button("Back to Log In", use_container_width=True):
            st.session_state.auth_page = "login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# -----------------------------
# MAIN APP
# -----------------------------
st.title("Barter Club Hub 🔁")
st.caption("A curated platform for creators and businesses to exchange value.")
st.warning("No money transactions. No custom work. Only real, existing value.")

with st.sidebar:
    st.title("Barter Club Hub")
    st.success(f"{profile['display_name']} • {profile['account_type']}")
    st.caption(f"Verification: {profile['verification_status']}")

    if st.button("Log Out", use_container_width=True):
        logout_user()
        st.rerun()

    page = st.radio(
        "Navigate",
        ["Dashboard", "Profile", "New Offer", "Matches", "Connections", "Settings"]
    )

# -----------------------------
# DASHBOARD
# -----------------------------
if page == "Dashboard":
    current_connections = get_user_connections(profile["display_name"])
    active_offers = [x for x in st.session_state.barter_posts if x["owner_name"] == profile["display_name"]]
    recommended_matches = get_matches(profile, st.session_state.selected_target)

    st.subheader(f"Welcome back, {profile['display_name']}")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="big-stat">
            <h3>{len(active_offers)}</h3>
            <p>Active Offers</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="big-stat">
            <h3>{len(current_connections)}</h3>
            <p>Connections</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="big-stat">
            <h3>{len(recommended_matches)}</h3>
            <p>Current Match Suggestions</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Your next move")

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown("""
        <div class="step-card">
            <div class="badge">STEP 1</div>
            <div class="section-title">Choose who you want to connect with</div>
            <div class="muted">Pick your lane first so Barter Club Hub can show more relevant matches.</div>
        </div>
        """, unsafe_allow_html=True)

        choice_left, choice_right = st.columns(2)
        with choice_left:
            if st.button("Connect with Creators", use_container_width=True):
                st.session_state.selected_target = "Creators"
                st.rerun()
        with choice_right:
            if st.button("Connect with Businesses", use_container_width=True):
                st.session_state.selected_target = "Businesses"
                st.rerun()

        st.markdown(f"""
        <div class="cta-box">
            <strong>Current lane:</strong> {st.session_state.selected_target}<br>
            <span class="muted">Your primary offer is <strong>{profile['primary_offer']}</strong> and your primary want is <strong>{profile['primary_want']}</strong>.</span>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="step-card">
            <div class="badge">STEP 2</div>
            <div class="section-title">Best current matches</div>
            <div class="muted">A quick preview of your strongest opportunities right now.</div>
        </div>
        """, unsafe_allow_html=True)

        preview_matches = recommended_matches[:2]

        if not preview_matches:
            st.info("No strong matches yet.")
        else:
            for match in preview_matches:
                st.markdown(f"""
                <div class="soft-card">
                    <div class="section-title">{match['owner_name']}</div>
                    <div class="muted">Score: {match['match_score']}% • {match['account_type']}</div>
                    <br>
                    <strong>Offers:</strong> {match['offer']}<br>
                    <strong>Wants:</strong> {match['want']}
                </div>
                """, unsafe_allow_html=True)

        if st.button("Open Full Matches", use_container_width=True):
            st.session_state.forced_page = "Matches"
            st.rerun()

# -----------------------------
# PROFILE
# -----------------------------
elif page == "Profile":
    st.subheader("Your Profile")

    if profile["account_type"] == "Creator":
        st.markdown(f"""
        <div class="soft-card">
            <div class="section-title">{profile['display_name']}</div>
            <div class="muted">Creator • {profile['location']}</div>
            <br>
            <strong>Bio:</strong> {profile['bio']}<br>
            <strong>Main Platform:</strong> {profile['main_platform']}<br>
            <strong>Audience Size:</strong> {profile['audience_size']}<br>
            <strong>Primary Offer:</strong> {profile['primary_offer']}<br>
            <strong>Primary Want:</strong> {profile['primary_want']}<br>
            <strong>Verification:</strong> {profile['verification_status']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="soft-card">
            <div class="section-title">{profile['display_name']}</div>
            <div class="muted">Business • {profile['location']}</div>
            <br>
            <strong>Bio:</strong> {profile['bio']}<br>
            <strong>Website:</strong> {profile['website']}<br>
            <strong>Business Email:</strong> {profile['business_email']}<br>
            <strong>Store Type:</strong> {profile['store_type']}<br>
            <strong>Primary Offer:</strong> {profile['primary_offer']}<br>
            <strong>Primary Want:</strong> {profile['primary_want']}<br>
            <strong>Verification:</strong> {profile['verification_status']}
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# NEW OFFER
# -----------------------------
elif page == "New Offer":
    st.subheader("Create a New Offer")

    st.markdown("""
    <div class="filter-box">
        Post a clear barter position so the system can recommend better matches.
    </div>
    """, unsafe_allow_html=True)

    target_connection = st.selectbox("Who do you want to connect with?", connection_options)
    col1, col2 = st.columns(2)

    with col1:
        offer = st.selectbox("What are you offering?", offer_options, key="post_offer")
    with col2:
        want = st.selectbox("What do you want in return?", offer_options, key="post_want")

    if st.button("Post Offer", use_container_width=True):
        st.session_state.barter_posts.append({
            "owner_name": profile["display_name"],
            "account_type": profile["account_type"],
            "target_type": target_connection[:-1] if target_connection.endswith("s") else target_connection,
            "offer": offer,
            "want": want,
            "location": profile["location"],
            "bio": profile["bio"]
        })
        st.success("Offer posted.")

# -----------------------------
# MATCHES
# -----------------------------
elif page == "Matches":
    st.subheader("Recommended Matches")

    filter_col1, filter_col2 = st.columns([1.2, 1])

    with filter_col1:
        target_connection = st.selectbox(
            "Who do you want to connect with?",
            connection_options,
            index=connection_options.index(st.session_state.selected_target)
        )

    with filter_col2:
        min_score = st.slider("Minimum match score", 25, 100, 25, 5)

    matches = get_matches(profile, target_connection, min_score=min_score)

    st.markdown("""
    <div class="filter-box">
        <strong>How matches are ranked:</strong> role fit + what they offer vs what you want + what they want vs what you offer.
    </div>
    """, unsafe_allow_html=True)

    if not matches:
        st.info("No strong matches yet. Try lowering the score filter or posting a new offer.")
    else:
        st.caption(f"Showing {len(matches)} match(es) for {target_connection.lower()}.")

        for i, match in enumerate(matches):
            render_match_card(match, i)

            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button(f"Connect with {match['owner_name']} 🤝", key=f"connect_{i}", use_container_width=True):
                    st.session_state.connections.append({
                        "from": profile["display_name"],
                        "to": match["owner_name"],
                        "status": "Pending"
                    })
                    st.success(f"Connection request sent to {match['owner_name']}.")
            with c2:
                st.button(f"Save for Later ☆", key=f"save_{i}", use_container_width=True)

# -----------------------------
# CONNECTIONS
# -----------------------------
elif page == "Connections":
    st.subheader("Connections")

    user_connections = get_user_connections(profile["display_name"])

    if not user_connections:
        st.info("No connections yet.")
    else:
        for c in user_connections:
            other_party = c["to"] if c["from"] == profile["display_name"] else c["from"]
            st.markdown(f"""
            <div class="soft-card">
                <div class="section-title">{other_party}</div>
                <div class="muted">Status: {c['status']}</div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------
# SETTINGS
# -----------------------------
elif page == "Settings":
    st.subheader("Settings")
    st.info("Real account settings will live here later.")

# -----------------------------
# FORCED PAGE NAV
# -----------------------------
if st.session_state.forced_page:
    forced = st.session_state.forced_page
    st.session_state.forced_page = None
    if forced != page:
        st.rerun()
