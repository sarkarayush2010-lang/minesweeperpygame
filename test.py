# clean_code.py
filename = "snek.py"

with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

# Replace all non-breaking spaces (\xa0) with regular spaces
cleaned_content = content.replace("\xa0", " ")

with open(filename, "w", encoding="utf-8") as f:
    f.write(cleaned_content)

print(f"Successfully cleaned {filename}!")