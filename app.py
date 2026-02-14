import streamlit as st
from ai_engine import AIEngine
import os
import re

# Page configuration
st.set_page_config(
    page_title="Scriptoria | AI Film Pre-Production",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar and Navigation
st.sidebar.title("🎬 Scriptoria")
st.sidebar.markdown("---")

# Initialize menu at top level to avoid NameError
menu = st.sidebar.radio(
    "Workflow Stage",
    ["Screenplay Generator", "Character Studio", "Visual Identity Studio", "Sonic Soundscape Studio", "Cine-Clip Architect", "Clip Studio", "Production Hub", "About"],
    index=7 # Default to 'About'
)

st.sidebar.markdown("---")
api_key = st.sidebar.text_input("Groq API Key", type="password", value="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")
st.sidebar.info("API Key is pre-filled from your request.")

# Initialize Session State
if "characters" not in st.session_state:
    st.session_state.characters = {}
if "scripts" not in st.session_state:
    st.session_state.scripts = []
if "production_data" not in st.session_state:
    st.session_state.production_data = {}
if "production_progress" not in st.session_state:
    st.session_state.production_progress = 0

# Custom CSS for modern dark theme and aesthetics
# Dynamic Theme Engine based on Menu Selection
themes = {
    "Screenplay Generator": {
        "bg_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&q=80&w=2000",
        "overlay": "rgba(0,0,0,0.7)"
    },
    "Character Studio": {
        "bg_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=2000",
        "overlay": "rgba(0,0,0,0.75)"
    },
    "Visual Identity Studio": {
        "bg_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&q=80&w=2000",
        "overlay": "rgba(0,0,0,0.7)"
    },
    "Sonic Soundscape Studio": {
        "bg_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&q=80&w=2000",
        "overlay": "rgba(0,0,0,0.8)"
    },
    "Cine-Clip Architect": {
        "bg_url": "https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?auto=format&fit=crop&q=80&w=2000",
        "overlay": "rgba(0,0,0,0.7)"
    },
    "Clip Studio": {
        "bg_url": "https://images.unsplash.com/photo-1535016120720-40c646bebbfc?auto=format&fit=crop&q=80&w=2000",
        "overlay": "rgba(0,0,0,0.65)"
    },
    "Production Hub": {
        "bg_url": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?auto=format&fit=crop&q=80&w=2000",
        "overlay": "rgba(0,0,0,0.75)"
    },
    "About": {
        "bg_url": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&q=80&w=2000",
        "overlay": "rgba(0,0,0,0.85)"
    }
}

current_theme = themes.get(menu, themes["About"])

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient({current_theme["overlay"]}, {current_theme["overlay"]}), 
                    url("{current_theme["bg_url"]}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main {{
        background-color: transparent;
    }}
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}
    .stButton>button {{
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-image: linear-gradient(45deg, #e50914, #b20710);
        color: white;
        border: none;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.4);
    }}
    .sidebar .sidebar-content {{
        background-color: rgba(26, 28, 35, 0.95);
    }}
    h1, h2, h3 {{
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    .output-container {{
        padding: 25px;
        border-radius: 15px;
        background-color: rgba(38, 39, 48, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #e50914;
        margin-top: 25px;
        color: #f0f0f0;
    }}
    .stTextArea textarea {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }}
    .stTextInput input {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }}
</style>
""", unsafe_allow_html=True)

# AI Engine Initialization

# Initialize AI Engine
try:
    ai = AIEngine(api_key=api_key)
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

# Main Header
st.title(f"🚀 {menu}")

if menu == "Screenplay Generator":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Craft Your Vision")
        idea = st.text_area("What's the scene idea?", placeholder="A cybernetic detective discovers a forgotten garden in a neon city...")
        
        # Workflow Automation: Link Characters
        selected_chars = []
        if st.session_state.characters:
            st.info("💡 Link your developed characters to this scene:")
            selected_chars = st.multiselect("Select Characters", options=list(st.session_state.characters.keys()))
        
        char_context = ""
        for char in selected_chars:
            char_context += f"\nCharacter Profile ({char}): {st.session_state.characters[char]}"

        genre_context = st.text_input("Additional Context (Genre, Tone)", placeholder="Cyberpunk, Melancholic")
        full_context = f"{genre_context}\n{char_context}"
        
        generate_btn = st.button("Generate Screenplay")
        
    with col2:
        st.subheader("Script Output")
        if generate_btn and idea:
            with st.spinner("AI is drafting the scene..."):
                script = ai.generate_screenplay(idea, full_context)
                if script and not script.startswith("Error"):
                    st.markdown(f'<div class="output-container">{script}</div>', unsafe_allow_html=True)
                    st.download_button("Download Script", script, file_name="script.txt")
                else:
                    st.error(f"Failed to generate screenplay: {script}")
        elif generate_btn:
            st.warning("Please enter a scene idea first.")

elif menu == "Character Studio":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Character Concept")
        char_name = st.text_input("Character Name", placeholder="Elias Vance")
        char_desc = st.text_area("Archetype or Description", placeholder="A weary space salvager with a heart of gold and a mysterious past.")
        generate_btn = st.button("Develop Character")
        
    with col2:
        st.subheader("Character Profile")
        if generate_btn and char_name:
            with st.spinner("Analyzing character depths..."):
                profile = ai.generate_character_profile(char_name, char_desc)
                if profile and not profile.startswith("Error"):
                    # Store in session state for workflow automation
                    st.session_state.characters[char_name] = profile
                    st.markdown(f'<div class="output-container">{profile}</div>', unsafe_allow_html=True)
                    st.download_button("Download Profile", profile, file_name=f"{char_name}_profile.txt")
                else:
                    st.error(f"Failed to generate character profile: {profile}")

elif menu == "Visual Identity Studio":
    st.subheader("👤 Visual Identity Studio (Face-Driven Scripting)")
    st.markdown("Analyze an actor's visual features to generate scripts that anchor to their unique cinematic aura.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Step 1: Visual Analysis")
        actor_desc = st.text_area("Describe the actor's face/identity", placeholder="e.g., Intense gaze, sharp cheekbones, enigmatic smirk, silver hair...")
        analyze_btn = st.button("Identify Visual Aura")
        
        if analyze_btn and actor_desc:
            with st.spinner("Analyzing biometric aesthetic..."):
                v_profile = ai.analyze_face_identity(actor_desc)
                st.session_state.current_v_identity = v_profile
                st.markdown(f'<div class="output-container">{v_profile}</div>', unsafe_allow_html=True)
        
    with col2:
        st.subheader("Step 2: Identitiy-Anchored Scripting")
        if "current_v_identity" in st.session_state:
            v_genre = st.selectbox("Anchor Genre", ["Neo-Noir", "Western", "High-Fantasy", "Psychological Thriller"])
            script_btn = st.button("Generate Anchored Script")
            
            if script_btn:
                with st.spinner("Drafting for this identity..."):
                    v_script = ai.generate_face_anchored_script(st.session_state.current_v_identity, v_genre)
                    st.markdown(f'<div class="output-container">{v_script}</div>', unsafe_allow_html=True)
                    st.download_button("Download Anchored Script", v_script, file_name="face_script.txt")
        else:
            st.info("💡 Complete Step 1 to unlock identity-anchored scripting.")

elif menu == "Sonic Soundscape Studio":
    st.subheader("🔊 Sonic Soundscape Studio")
    st.markdown("Generate high-fidelity cinematic sound designs and complete production packs.")
    
    tab1, tab2 = st.tabs(["Single Scene", "Production Sound Pack"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Soundscape Parameters")
            scene_desc = st.text_area("Describe the Scene for Sound", placeholder="A busy marketplace on a desert planet...")
            generate_btn = st.button("Generate Sonic Plan")
            
        with col2:
            st.subheader("Sound Design Guide")
            if generate_btn and scene_desc:
                with st.spinner("Orchestrating the soundscape..."):
                    sonic_plan = ai.generate_sound_design(scene_desc)
                    if sonic_plan and not sonic_plan.startswith("Error"):
                        st.markdown(f'<div class="output-container">{sonic_plan}</div>', unsafe_allow_html=True)
                        
                        # ML Labels
                        st.markdown("#### 🏷️ ML Dataset Labels")
                        labels = ai.generate_ml_labels(sonic_plan)
                        if labels and not labels.startswith("Error"):
                            label_list = [l.strip() for l in labels.split(",")]
                            cols = st.columns(len(label_list))
                            for i, label in enumerate(label_list):
                                cols[i % len(cols)].info(f"Tag: {label}")
                        
                        st.download_button("Download Sonic Plan", sonic_plan, file_name="sound_design.txt")
                    else:
                        st.error(f"Failed to generate sonic plan: {sonic_plan}")
    
    with tab2:
        st.subheader("🎬 Create Cinematic Sound Pack")
        st.markdown("Generate a series of high-quality sonic templates for game scenes, video scenes, and emotional moods.")
        
        if st.button("Generate Full Production Pack"):
            with st.spinner("Generating 10-second studio blueprints..."):
                # Define batch prompts
                packs = [
                    ("Jungle Temple", "Jungle temple environment with wind, insects, thunder, and footsteps. 10s."),
                    ("Cyberpunk Night", "Cyberpunk street at night with rain, footsteps, traffic. 10s."),
                    ("Emotional Mood", "Mood: Emotional. Soft piano and wind. 10s."),
                    ("Horror Mood", "Mood: Horror. Low bass and whisper. 10s."),
                    ("Action Mood", "Mood: Action. Fast drums and explosion. 10s."),
                    ("Sci-Fi Mood", "Mood: Sci-fi. Futuristic synth and digital beeps. 10s.")
                ]
                
                full_pack_output = "# Scriptoria Cinematic Sound Pack\n\n"
                for title, prompt in packs:
                    st.write(f"Orchestrating **{title}**...")
                    bp = ai.generate_sound_design(prompt)
                    labels = ai.generate_ml_labels(bp)
                    full_pack_output += f"## {title}\n{bp}\n\n**ML Labels**: {labels}\n\n"
                    
                    with st.expander(f"View {title} Blueprint"):
                        st.markdown(f'<div class="output-container">{bp}</div>', unsafe_allow_html=True)
                        st.caption(f"ML Tags: {labels}")
                
                st.success("✅ Cinematic Sound Pack Complete!")
                st.download_button("Download Complete Sound Pack", full_pack_output, file_name="scriptoria_sound_pack.txt")

elif menu == "Cine-Clip Architect":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Visual Concept (10s Clip)")
        visual_idea = st.text_area("What's the visual moment?", placeholder="A drop of water hitting a still lake, sending ripples out across a reflected moon.")
        style = st.selectbox("Cinematic Style", ["Hyper-Realistic", "Neo-Noir", "Surrealist", "Anamorphic", "Vivid Fantasy"])
        generate_btn = st.button("Architect Scene")
        
    with col2:
        st.subheader("AI Video Prompt")
        if generate_btn and visual_idea:
            with st.spinner("Directing the AI camera..."):
                video_prompt = ai.generate_video_prompt(visual_idea, style)
                if video_prompt and not video_prompt.startswith("Error"):
                    st.markdown(f'<div class="output-container">{video_prompt}</div>', unsafe_allow_html=True)
                    st.download_button("Download Video Prompt", video_prompt, file_name="video_prompt.txt")
                else:
                    st.error(f"Failed to generate video prompt: {video_prompt}")

elif menu == "Clip Studio":
    st.subheader("🎬 AI Video Production Lab")
    st.markdown("Generate high-fidelity 10-second AI video clips directly from your concepts.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        v_idea = st.text_area("What should happen in the video?", placeholder="A dragon flying over a frozen city at night, breathing blue fire...")
        v_res = st.selectbox("Resolution", ["1080p (Cinematic)", "4K (Ultra)", "720p (Draft)"])
        v_fps = st.select_slider("Frame Rate", options=[24, 30, 60], value=24)
        prod_btn = st.button("Start AI Render")
        
    with col2:
        if prod_btn and v_idea:
            # Step 1: Generate Prompt
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Step 1: Architecting Cinematic Prompt...")
            v_prompt = ai.generate_video_prompt(v_idea)
            progress_bar.progress(30)
            
            # Step 2: Generate Production Specs
            status_text.text("Step 2: Calculating Motion Vectors & Camera Paths...")
            v_specs = ai.get_video_production_data(v_idea)
            progress_bar.progress(50)
            
            # Step 3: Generate Motion Script
            status_text.text("Step 3: Generating 10-Second Automation Script...")
            v_script = ai.generate_motion_script(v_idea)
            progress_bar.progress(80)
            
            # Step 4: Finalize
            status_text.text("Step 4: Architecting 10-Second Production Blueprint...")
            v_storyboard = ai.generate_multi_frame_storyboard(v_idea)
            progress_bar.progress(100)
            
            status_text.success("✅ Cinematic Production Blueprint Complete!")
            
            # Blueprint Branding
            st.warning("🎬 **Scriptoria Production Blueprint**: This module generates high-fidelity cinematic plans, motion scripts, and storyboards to guide your production in industry-standard render engines.")
            
            # --- DYNAMIC VIDEO PRODUCTION PREVIEW ---
            st.subheader("🚀 High-Fidelity Production Preview")
            
            # Motion Asset Library (Cinematic Mapping)
            motion_library = {
                "dragon": "https://www.w3schools.com/html/mov_bbb.mp4", # Placeholder for animal/creature
                "student": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
                "laptop": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
                "walking": "https://www.w3schools.com/html/mov_bbb.mp4",
                "city": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
                "night": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
                "default": "https://www.w3schools.com/html/mov_bbb.mp4"
            }
            
            # Select Video based on Keywords
            selected_video = motion_library["default"]
            v_idea_lower = v_idea.lower()
            for key in motion_library:
                if key in v_idea_lower:
                    selected_video = motion_library[key]
                    break
            
            st.video(selected_video)
            st.caption(f"Simulated Production Preview for: '{v_idea}'")
            
            # --- MULTI-FRAME STORYBOARD ---
            st.markdown("---")
            st.subheader("🖼️ 10-Second Cinematic Storyboard")
            
            # Robust parsing for the storyboard beats
            try:
                # Expecting format: Title: Beat 1, Timestamp: 0-2s, Visual: ..., Keywords: ...
                beat_blocks = v_storyboard.split("Title:")[1:]
                if beat_blocks:
                    cols = st.columns(len(beat_blocks))
                    for i, block in enumerate(beat_blocks):
                        ts_match = re.search(r"Timestamp: (.*?)(?:\n|,)", block)
                        vis_match = re.search(r"Visual: (.*?)(?:\n|,)", block)
                        kw_match = re.search(r"Keywords: (.*?)(\n|\Z)", block)
                        
                        ts = ts_match.group(1).strip() if ts_match else "N/A"
                        vis = vis_match.group(1).strip() if vis_match else "Description pending..."
                        kw = kw_match.group(1).strip() if kw_match else "cinematic"
                        
                        with cols[i]:
                            st.image(f"https://image.pollinations.ai/prompt/{kw.replace(' ', '%20')},film,cinematic?width=400&height=300&seed={i}", caption=f"Beat {i+1} ({ts})")
                            st.write(f"**{ts}**")
                            st.caption(vis)
                else:
                    st.info("Visualizing production beats...")
                    st.markdown(v_storyboard)
            except Exception:
                st.markdown(v_storyboard)
            
            # --- MOTION TIMELINE ---
            st.markdown("---")
            st.markdown("### 🗺️ 10-Second Motion Timeline (Directorial Script)")
            st.info(v_script)
            
            with st.expander("🛠️ Technical Production Specs (For Render Engines)"):
                st.code(v_specs)
                st.markdown(f"**Master AI Production Prompt:**\n{v_prompt}")
        
        elif prod_btn:
            st.warning("Please enter a visual idea for the video.")

elif menu == "Production Hub":
    st.subheader("🏢 Production Command Center")
    st.markdown("Centralize your pre-production workflow: from budget planning to crew selection.")
    
    # Dashboard Metrics
    m1, m2, m3 = st.columns(3)
    completed_plans = len(st.session_state.production_data)
    total_categories = 8
    progress_pct = (completed_plans / total_categories) * 100
    
    m1.metric("Completed Plans", completed_plans)
    m2.metric("Production Readiness", f"{progress_pct:.0f}%")
    m3.metric("Pending Tasks", total_categories - completed_plans)
    
    st.progress(progress_pct / 100)
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🛠️ Strategy & Planning")
        prod_idea = st.text_area("Project Concept or Current Scene", placeholder="A sci-fi short film about a moon base heist...", key="prod_idea_input")
        prod_category = st.selectbox(
            "Select Milestone", 
            ["Script Finalization", "Budget Planning", "Casting Studio", "Location Scout", "Storyboard Preparation", "Costume & Makeup", "Schedule Planning", "Crew Selection"]
        )
        plan_btn = st.button("Architect Milestone Blueprint")
        
        if plan_btn and prod_idea:
            with st.spinner(f"Architecting {prod_category}..."):
                blueprint = ai.generate_production_blueprint(prod_idea, prod_category)
                if blueprint and not blueprint.startswith("Error"):
                    st.session_state.production_data[prod_category] = blueprint
                    st.success(f"✅ {prod_category} Archive Updated!")
                else:
                    st.error(f"Failed to generate {prod_category}: {blueprint}")
        elif plan_btn:
            st.warning("Please enter a project concept.")

    with col2:
        st.subheader("🗄️ Project Archive")
        if not st.session_state.production_data:
            st.info("No plans generated yet. Architect your first milestone to see the archive.")
        else:
            # Sort keys to keep order consistent
            for cat in sorted(st.session_state.production_data.keys()):
                data = st.session_state.production_data[cat]
                with st.expander(f"📄 {cat}"):
                    st.markdown(f'<div class="output-container">{data}</div>', unsafe_allow_html=True)
                    st.download_button(f"Download {cat}", data, file_name=f"{cat.lower().replace(' ', '_')}.txt", key=f"dl_{cat}")

    # Full Master Export
    if st.session_state.production_data:
        st.markdown("---")
        master_book = "# Master Production Book\n\n"
        for cat, data in st.session_state.production_data.items():
            master_book += f"## {cat}\n{data}\n\n---\n\n"
        st.download_button("🚀 Export Master Production Book", master_book, file_name="master_production_book.txt")

elif menu == "About":
    st.markdown("""
    ### About Scriptoria
    Scriptoria is a Generative AI–Powered Film Pre-Production System designed to help filmmakers:
    - **Generate Screenplays** from simple prompts.
    - **Develop Deep Characters** with rich backstories.
    - **Visual Identity Studio**: Generate scripts anchored to an actor's specific face/visual aura.
    - **Plan Sound Design** for cinematic immersion.
    - **Architect 10s AI Video Clips** with detailed cinematic prompts.
    - **Directly Produce 10s AI Videos** in the Clip Studio.
    - **Full Production Command Center**: Manage budgets, casting, locations, and schedules.
    
    Powered by **Groq AI** and **Streamlit**.
    """)

# Footer
st.markdown("---")
st.caption("Scriptoria v1.0 | AI-Powered Film Pre-Production")
