"""Quick script to remove emojis from main.py for Windows compatibility"""

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace emojis with text
replacements = {
    '🤖': '',
    '📂': '',
    '✅': '[OK]',
    '🎯': '',
    '🧹': '',
    '⚙️': '',
    '📊': '',
    '📄': '',
    '🎉': '',
    '📁': '',
    '✨': ''
}

for emoji, replacement in replacements.items():
    content = content.replace(emoji, replacement)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed emojis in main.py")
