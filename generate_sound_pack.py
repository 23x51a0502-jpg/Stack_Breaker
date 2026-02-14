from ai_engine import AIEngine
import os

api_key = "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"
ai = AIEngine(api_key=api_key)

scenes = {
    "Jungle Temple": "Jungle temple environment with wind, insects, thunder, and footsteps. 10 seconds, realistic, cinematic, immersive.",
    "Cyberpunk Street": "Cyberpunk street at night with rain, footsteps, traffic, and one vehicle passing. 10 seconds, realistic, cinematic, immersive.",
    "Emotional Mood": "Mood sound: Emotional. Soft piano and wind. 10 seconds, studio quality, cinematic.",
    "Horror Mood": "Mood sound: Horror. Low bass and whisper. 10 seconds, studio quality, cinematic.",
    "Action Mood": "Mood sound: Action. Fast drums and explosion. 10 seconds, studio quality, cinematic.",
    "Sci-fi Mood": "Mood sound: Sci-fi. Futuristic synth and digital beeps. 10 seconds, studio quality, cinematic."
}

results = {}

print("--- Generating Sound Design Pack ---")
for name, Prompt in scenes.items():
    print(f"Generating for {name}...")
    blueprint = ai.generate_sound_design(Prompt)
    results[name] = blueprint

print("\n--- ML Dataset Labels ---")
labels = ["Rain", "Footsteps", "Thunder", "Vehicle", "Wind", "Breathing", "Door Open"]
print(f"Expected Labels: {', '.join(labels)}")

# Write to a temporary file to be picked up by the agent
with open("sound_pack_results.txt", "w", encoding="utf-8") as f:
    for name, blueprint in results.items():
        f.write(f"### {name}\n{blueprint}\n\n")
    f.write("### ML Dataset Labels\n")
    f.write(", ".join(labels))
