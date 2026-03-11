import os
import re

app_dir = r"e:\Projects\agmis\backend\app"

count = 0
for root, _, files in os.walk(app_dir):
    for file in files:
        if file.endswith(('.html', '.css', '.py')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            orig = content
            # General CSS hex and words
            content = re.sub(r'(color\s*:\s*)#fff(fff)?\b', r'\g<1>#000000', content, flags=re.IGNORECASE)
            content = re.sub(r'(color\s*:\s*)white\b', r'\g<1>#000000', content, flags=re.IGNORECASE)
            content = re.sub(r'(color\s*:\s*)#ffffff\b', r'\g<1>#000000', content, flags=re.IGNORECASE)
            
            # Matplotlib / chart.js string values
            content = re.sub(r"color\s*:\s*'#fff(fff)?'", "color: '#000000'", content, flags=re.IGNORECASE)
            content = re.sub(r"color\s*:\s*'white'", "color: '#000000'", content, flags=re.IGNORECASE)
            
            # rgba / rgb white transparent values - change them to black transparent/solid
            content = re.sub(r'(color\s*:\s*)rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*[^)]+\)', r'\g<1>#000000', content, flags=re.IGNORECASE)

            # Change `--text-muted`, `--cyan`, etc., to black 
            # If the user really wants *all* text to be black, we can overrule `--text-muted` and `--text-secondary`
            # and var(...) references in HTML elements' "color" styling if they're not already black.
            # E.g. color: #000000 -> color: #000000
            
            # It's better to just change the definitions in style.css or let the var be #000000
            # Let's replace var(--text-muted) to #000000
            content = re.sub(r'color\s*:\s*var\(--text-muted\)', 'color: #000000', content, flags=re.IGNORECASE)
            content = re.sub(r'color\s*:\s*var\(--text-secondary\)', 'color: #000000', content, flags=re.IGNORECASE)
            content = re.sub(r'color\s*:\s*var\(--text-primary\)', 'color: #000000', content, flags=re.IGNORECASE)

            # Also replace inline styling colors matching "white" or "fff" without space
            content = re.sub(r'color:#000000(fff)?\b', 'color:#000000', content, flags=re.IGNORECASE)
            content = re.sub(r'color:#000000\b', 'color:#000000', content, flags=re.IGNORECASE)

            if content != orig:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                
print(f"Replaced text colors in {count} files.")
