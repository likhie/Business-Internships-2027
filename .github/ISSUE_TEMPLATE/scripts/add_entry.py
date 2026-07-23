import os
import re

issue_body = os.environ.get("ISSUE_BODY", "")

def extract_field(label, text):
    match = re.search(f"### {label}\\s*\\n\\s*(.+)", text)
    return match.group(1).strip() if match else ""

company = extract_field("Company Name", issue_body)
role = extract_field("Internship Role Title", issue_body)
category = extract_field("Industry Category", issue_body)
location = extract_field("Location", issue_body)
link = extract_field("Direct Application Link", issue_body)

if company and role and link:
    new_row = f"| **{company}** | {role} | {location} | [Apply Here]({link}) | Just added |\n"
    
    with open("README.md", "r") as f:
        content = f.read()
    
    # Section header matching
    header_map = {
        "Product Management": "## 📦 Product Management",
        "Marketing & Growth": "## 📈 Marketing & Growth",
        "Sales & Business Development": "## 🤝 Sales & Business Development",
        "Strategy, Analytics & Operations": "## 📊 Strategy, Analytics & Operations",
        "MBA & Graduate": "## 🎓 MBA & Graduate Internships"
    }

    target_header = header_map.get(category, "## 📦 Product Management")
    
    if target_header in content:
        parts = content.split(target_header)
        # Find table header ending in the second part
        table_end = parts[1].find("| :--- | :--- | :--- | :--- | :--- |\n") + len("| :--- | :--- | :--- | :--- | :--- |\n")
        updated_content = parts[0] + target_header + parts[1][:table_end] + new_row + parts[1][table_end:]
        
        with open("README.md", "w") as f:
            f.write(updated_content)
