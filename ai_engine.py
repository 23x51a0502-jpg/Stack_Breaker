import os
from groq import Groq
from dotenv import load_dotenv
import requests
import imageio
from moviepy import ImageSequenceClip
import numpy as np
import time

load_dotenv()

class AIEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API Key not found. Please provide it in the sidebar or .env file.")
        self.client = Groq(api_key=self.api_key)

    def generate_screenplay(self, prompt, context=""):
        system_prompt = """You are an expert screenwriter. Generate a screenplay segment based on the user's idea. 
        Use standard Fountain or Screenplay format (SCENE HEADING, ACTION, CHARACTER, DIALOGUE).
        Keep it cinematic and engaging."""
        
        full_prompt = f"Idea: {prompt}\nContext: {context}"
        return self._get_completion(system_prompt, full_prompt)

    def generate_character_profile(self, name, description):
        system_prompt = """You are a master of character development. Create a deep, multidimensional character profile.
        Include: Backstory, Core Motivations, External/Internal Conflicts, and Personality Traits."""
        
        full_prompt = f"Character Name: {name}\nDescription/Archetype: {description}"
        return self._get_completion(system_prompt, full_prompt)

    def generate_sound_design(self, scene_description):
        system_prompt = """You are an award-winning Sound Designer. Create a 'Sonic Blueprint' for the given scene.
        Detail the Ambient Atmosphere, Foley Effects, Musical Cues, and Sound Transitions."""
        
        full_prompt = f"Scene Description: {scene_description}"
        return self._get_completion(system_prompt, full_prompt)

    def generate_ml_labels(self, sonic_blueprint):
        """Extracts ML dataset labels (keyword audio events) from a sound design blueprint."""
        system_prompt = """You are an AI Audio Engineer. Analyze the provided sound design blueprint and extract exactly 5-7 short, 
        distinct audio event labels that would be useful for tagging an ML dataset. 
        Examples: 'Thunder', 'Heavy Rain', 'Footsteps on Gravel', 'Distant Siren', 'Door Creak'.
        Return ONLY the labels as a comma-separated list. No ands, no periods, no introductory text."""
        
        full_prompt = f"Sound Design Blueprint:\n{sonic_blueprint}"
        return self._get_completion(system_prompt, full_prompt)

    def generate_video_prompt(self, visual_idea, style="Cinematic"):
        system_prompt = """You are a Visual Effects Supervisor and AI Video Expert. 
        Create a detailed, high-quality prompt for a 10-second AI video clip.
        Include: camera movement (pan, tilt, zoom, drone), lighting (golden hour, neon, volumetric), 
        cinematic style, and specific visual details. Ensure it's optimized for tools like Runway Gen-3, Kling, or Luma."""
        
        full_prompt = f"Visual Idea: {visual_idea}\nPreferred Style: {style}"
        return self._get_completion(system_prompt, full_prompt)

    def get_video_production_data(self, visual_idea):
        system_prompt = """You are a Technical Director. Create a JSON-like technical specification for a 10-second AI video render.
        Include: Frame Rate, Resolution, Motion Bucket, Seed, and Camera Path Coordinates."""
        
        full_prompt = f"Visual Idea: {visual_idea}"
        return self._get_completion(system_prompt, full_prompt)

    def generate_motion_script(self, visual_idea):
        system_prompt = """You are an AI Animation Director. Create a '10-Second Motion Script'.
        Break the 10 seconds into 2-second intervals.
        For each interval, describe:
        1. Character Action (e.g., 'Walking straight', 'Approaching bed')
        2. Camera Movement (e.g., 'Tracking shot', 'Close-up on face')
        3. Lighting/VFX changes."""
        
        full_prompt = f"Visual Idea: {visual_idea}"
        return self._get_completion(system_prompt, full_prompt)

    def generate_multi_frame_storyboard(self, visual_idea):
        system_prompt = """You are a Storyboard Artist. Break down the user's 10-second video idea into exactly 4 cinematic 'Beats'.
        For each beat, provide:
        1. Timestamp (e.g., '0-2s')
        2. Visual Description (vivid details on composition/colors)
        3. Search Keywords (3-5 comma-separated keywords for identifying this scene visually)
        
        Return the response in a structured text format that can be easily parsed (Title: Beat 1, Timestamp: 0-2s, Visual: ..., Keywords: ...)."""
        
        full_prompt = f"Video Idea: {visual_idea}"
        return self._get_completion(system_prompt, full_prompt)

    def analyze_face_identity(self, image_desc="Actor Face"):
        system_prompt = """You are a Biometric Identity Architect. Based on the description of an actor's face, generate a 'Visual Identity Profile'.
        Include: Facial Structure (e.g., sharp jawline), Eye Shape/Color, Distinguishing Features, and 'Cinematic Aura' (the vibe they project, e.g., Heroic, Villainous, Enigmatic).
        Format the output clearly with headers."""
        
        full_prompt = f"Actor Face Description: {image_desc}"
        return self._get_completion(system_prompt, full_prompt)

    def generate_face_anchored_script(self, visual_profile, genre="Neo-Noir"):
        system_prompt = f"""You are a Screenwriter who writes specifically for actors' unique visual types. 
        Based on the provided 'Visual Identity Profile', generate a short, intense script segment (3-4 lines of dialogue + action) 
        that perfectly utilizes this actor's specific 'aura' and physical features.
        Genre: {genre}"""
        
        full_prompt = f"Visual Identity Profile:\n{visual_profile}"
        return self._get_completion(system_prompt, full_prompt)

    def generate_ai_video(self, prompt, status_callback=None):
        """Generates a 5-second cinematic video using Pollinations.ai and MoviePy."""
        # 1. Generate 5 variations for keyframes to simulate motion
        system_prompt = """Generate 5 unique cinematic descriptions for a 5-second sequence based on the user's prompt. 
        Each should describe a slight variation in camera, lighting, or action to simulate motion. 
        Return ONLY the list of 5 descriptions separated by '|'. No other text."""
        
        variations_raw = self._get_completion(system_prompt, prompt)
        variations = [v.strip() for v in variations_raw.split('|') if v.strip()][:5]
        
        if len(variations) < 5:
            variations = [prompt] * 5
            
        # 2. Download Images
        frames_dir = "v_temp_frames"
        os.makedirs(frames_dir, exist_ok=True)
        frame_paths = []
        
        for i, val in enumerate(variations):
            if status_callback:
                status_callback(f"Synthesizing Frame {i+1}/5: {val[:50]}...")
            
            clean_val = "".join([c if c.isalnum() or c == " " else "" for c in val]).replace(" ", "%20")
            url = f"https://image.pollinations.ai/prompt/{clean_val}?width=1024&height=576&nologo=true&seed={int(time.time())+i}"
            
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    path = os.path.join(frames_dir, f"frame_{i}.jpg")
                    with open(path, "wb") as f:
                        f.write(response.content)
                    frame_paths.append(path)
            except Exception as e:
                print(f"Error downloading frame {i}: {e}")
                
        if not frame_paths:
            return None, "Failed to generate visual frames."
            
        # 3. Stitch into Video
        try:
            if status_callback:
                status_callback("Finalizing Cinematic Render (Stitching 5s Sequence)...")
            
            # Create a 5-second clip (1 FPS to ensure it lasts 5 seconds with 5 frames)
            clip = ImageSequenceClip(frame_paths, fps=1)
            output_path = "generated_video.mp4"
            clip.write_videofile(output_path, codec="libx264", audio=False, verbose=False, logger=None)
            
            # Simple cleanup
            for p in frame_paths:
                try: os.remove(p)
                except: pass
            
            return output_path, None
        except Exception as e:
            return None, f"Video Stitching Error: {str(e)}"

    def generate_production_blueprint(self, project_idea, category):
        """Generates specific pre-production plans based on category."""
        prompts = {
            "Script Finalization": "You are a Script Doctor and Editor. Review and finalize the given scene/concept. Focus on pacing, dialogue rhythm, and emotional impact. Provide a polished 'Final Draft' version.",
            "Budget Planning": "You are a Line Producer. Create a detailed Budget Plan for this project. Include Estimated Totals, Department Breakdown, and Contingency Plans.",
            "Casting Studio": "You are a Casting Director. Create a Casting Call for the project. Detail key roles, personality requirements, physical descriptions, and 'Casting Aura' for each actor.",
            "Location Scout": "You are a Location Manager. Detail the Scouting Report for the project. Specify scene locations, desired aesthetic, lighting requirements, and technical accessibility.",
            "Storyboard Preparation": "You are a Storyboard Artist. Break down the project/scene into visual beats. Describe composition, camera angles, and key actions for each frame.",
            "Costume & Makeup": "You are a Costume Designer and Makeup Artist. Create a Visual Style Guide for character attire and SFX makeup. Detail fabric types, color palettes, and transformative makeup requirements.",
            "Schedule Planning": "You are a 1st Assistant Director (AD). Create a Production Schedule. Detail shooting days, scene blocks, and logical workflow for maximum efficiency.",
            "Crew Selection": "You are a Producer. Identify the necessary 'Head of Departments' (Director, DOP, Editor, etc.) and specify the required skill set and creative vision for each."
        }
        
        system_prompt = prompts.get(category, "You are a Film Production Expert. Provide detailed planning for the given project.")
        full_prompt = f"Project Concept/Scene: {project_idea}\nCategory: {category}"
        return self._get_completion(system_prompt, full_prompt)

    def _get_completion(self, system_message, user_message):
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=2048,
                top_p=1,
                stream=False,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
