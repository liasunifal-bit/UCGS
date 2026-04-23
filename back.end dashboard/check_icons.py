with open("site nevo.HTML", "r", encoding="utf-8") as f:
    content = f.read()

fa_loaded = "font-awesome" in content.lower() or "fontawesome" in content.lower()
lucide_loaded = "lucide" in content.lower()
print("FontAwesome loaded:", fa_loaded)
print("Lucide loaded:", lucide_loaded)
print("Total chars:", len(content))

# Find head section
head_end = content.find("</head>")
print("---HEAD (first 2000 chars)---")
print(content[:min(head_end, 2000)])

# Find sidebar
sidebar_idx = content.find('id="sidebar"')
if sidebar_idx >= 0:
    print("\n---SIDEBAR START (1500 chars)---")
    print(content[sidebar_idx:sidebar_idx+1500])
else:
    nav_idx = content.find("nav-item")
    if nav_idx > 0:
        print("\n---NAV ITEM (first match, 800 chars)---")
        print(content[nav_idx:nav_idx+800])
    else:
        print("sidebar/nav-item NOT FOUND")
