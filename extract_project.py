import os
import re

# Paste Gemini output here ↓↓↓
gemini_output = """# (User: Paste the project output block here)"""

# Create folders
os.makedirs("data", exist_ok=True)
os.makedirs("src", exist_ok=True)

files = re.split(r"### FILE: ", gemini_output)[1:]

for file in files:
    lines = file.strip().split("\n")
    if not lines:
        continue
        
    filename = lines[0].strip()
    content = "\n".join(lines[1:])

    # Remove code block markers if present
    content = content.replace("```python", "").replace("```csv", "").replace("```", "").strip()

    filepath = filename

    # Ensure subdirectories exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created: {filepath}")
