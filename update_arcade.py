import os
import subprocess

# 1. Scan for all .swf files in the directory
game_files = [f for f in os.listdir('.') if f.endswith('.swf')]

# 2. Build the new dropdown HTML content
dropdown_options = []
for file in sorted(game_files):
    # Turn "super_mario.swf" into "Super Mario" for a clean display name
    clean_name = file.replace('.swf', '').replace('_', ' ').replace('-', ' ').title()
    dropdown_options.append(f'            <option value="{file}">{clean_name}</option>')

options_html = "\n".join(dropdown_options)

# 3. Read your template HTML file
# (We look for standard split markers to know where to drop the list)
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Split the file using marker comments so we don't overwrite your whole layout
    start_marker = "<!-- START GAMES DROPDOWN -->"
    end_marker = "<!-- END GAMES DROPDOWN -->"
    
    if start_marker in html_content and end_marker in html_content:
        before = html_content.split(start_marker)[0]
        after = html_content.split(end_marker)[1]
        
        # Piece it back together with the fresh roster
        updated_html = f"{before}{start_marker}\n{options_html}\n        {end_marker}{after}"
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(updated_html)
        print("✓ index.html dropdown updated successfully!")
        
        # 4. Automatically run your Git deployment sequence
        print("Pushing updates to GitHub...")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update arcade roster"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✓ Successfully deployed live!")
        
    else:
        print("Error: Could not find the required comment markers in your index.html file.")
        print(f"Please add '{start_marker}' and '{end_marker}' around your <option> tags.")

except Exception as e:
    print(f"An error occurred: {e}")
    