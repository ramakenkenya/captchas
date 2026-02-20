import re

with open("index.html", "r") as f:
    html = f.read()

# 1. Insert getIcon and update renderMap
get_icon_code = """
        function getIcon(levelName) {
            const icons = {
                'Distorted Text': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 7 4 4 20 4 20 7"></polyline><line x1="9" y1="20" x2="15" y2="20"></line><line x1="12" y1="4" x2="12" y2="20"></line></svg>',
                'Image Grid': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>',
                'Single Image Click': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="3"></circle></svg>',
                'Challenge-Gated Checkbox': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"></polyline><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>',
                'Audio Digits': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>',
                'Math / Logic': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="8" y1="6" x2="16" y2="6"></line><line x1="16" y1="14" x2="16" y2="18"></line><line x1="16" y1="10" x2="16" y2="10"></line><line x1="8" y1="10" x2="8" y2="10"></line><line x1="8" y1="14" x2="8" y2="14"></line><line x1="8" y1="18" x2="8" y2="18"></line><line x1="12" y1="10" x2="12" y2="10"></line><line x1="12" y1="14" x2="12" y2="14"></line><line x1="12" y1="18" x2="12" y2="18"></line></svg>',
                'Jigsaw Slider': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19.439 7.85c-.049.322.059.648.289.878l1.568 1.568c.47.47.706 1.087.706 1.704s-.235 1.233-.706 1.704l-1.611 1.611a.98.98 0 0 1-.837.276c-.47-.07-.802-.48-.968-.925a2.501 2.501 0 1 0-3.214 3.214c.446.166.855.497.925.968a.979.979 0 0 1-.276.837l-1.61 1.611c-.946.946-2.463.946-3.409 0L8.73 19.73a.98.98 0 0 1-.276-.837c.07-.47.48-.802.925-.968a2.501 2.501 0 1 0-3.214-3.214c-.166-.446-.497-.855-.968-.925a.979.979 0 0 1-.837-.276L2.749 11.9a2.41 2.41 0 0 1 0-3.409l1.568-1.568a.98.98 0 0 1 .878-.289c.49.106.84.58.986 1.054a2.5 2.5 0 1 0 3.364-3.364c-.474-.146-.948-.496-1.054-.986a.98.98 0 0 1 .289-.878l1.568-1.568c.946-.946 2.463-.946 3.409 0l1.568 1.568a.98.98 0 0 1 .289.878c-.106.49-.58.84-1.054 1.986a2.5 2.5 0 1 0 3.364 3.364c.146.474.496.948.986 1.054z"></path></svg>',
                'Rotate to Upright': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="21.5 2 21.5 7 16.5 7"></polyline><polyline points="2.5 22 2.5 17 7.5 17"></polyline><path d="M2 12c0-5.5 4.5-10 10-10 4.2 0 7.8 2.6 9.3 6.3"></path><path d="M22 12c0 5.5-4.5 10-10 10-4.2 0-7.8-2.6-9.3-6.3"></path></svg>',
                'Shape Matching': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="8" height="8" rx="2" ry="2"></rect><circle cx="16.5" cy="7.5" r="4.5"></circle><line x1="3" y1="21" x2="11" y2="13"></line><line x1="11" y1="21" x2="3" y2="13"></line><path d="M15 21l3-6 3 6z"></path></svg>',
                'Gamified Puzzle': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2" ry="2"></rect><path d="M6 12h4"></path><path d="M8 10v4"></path><line x1="15" y1="13" x2="15.01" y2="13"></line><line x1="18" y1="11" x2="18.01" y2="11"></line></svg>',
                'Behavioral Biometrics': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l7.07 16.97 2.51-7.39 7.39-2.51L3 3z"></path><path d="M13 13l6 6"></path></svg>',
                'Escalation Ladder': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>'
            };
            return icons[levelName] || '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle></svg>';
        }

        function renderMap() {"""

render_map_target = "function renderMap() {"
html = html.replace(render_map_target, get_icon_code)

old_card_gen = "card.innerHTML = `\n        ${iconHTML}\n        <div class=\"level-num\">Level ${lvl.id}</div>"
new_card_gen = "let typeIconHTML = `<div class=\"level-type-icon\" style=\"position: absolute; top: 1.5rem; right: ${isCompleted ? '3.5rem' : '1.5rem'}; opacity: 0.3; color: var(--text-main); pointer-events: none; transition: right 0.3s;\">${getIcon(lvl.name)}</div>`;\n\n                card.innerHTML = `\n        ${iconHTML}\n        ${typeIconHTML}\n        <div class=\"level-num\">Level ${lvl.id}</div>"
html = html.replace(old_card_gen, new_card_gen)


# 2. Extract LEVELS array and filter out unwanted, re-id the remaining
levels_start = html.find("const LEVELS = [")
levels_end = html.find("];\\n\\n        // INIT", levels_start)

if levels_end == -1: 
    levels_end = html.find("        ];", levels_start)

levels_str = html[levels_start:levels_end+10]

import ast
def parse_levels(l_str):
    import re
    # We will split it by "            {\n                id:"
    parts = l_str.split("            {\n                id:")
    prefix = parts[0]
    items = []
    
    for p in parts[1:]:
        # ' id: X, name: ... '
        num_match = re.search(r"^\s*(\d+),", p)
        if num_match:
            old_id = int(num_match.group(1))
            items.append((old_id, "            {\n                id:" + p))
        else:
            items.append((-1, "            {\n                id:" + p))
    return prefix, items

prefix, items = parse_levels(levels_str)
remove_ids = {5, 6, 9, 15, 16, 17, 19}
keep_items = []
for old_id, text in items:
    if old_id not in remove_ids:
        keep_items.append((old_id, text))

new_items_text = []
for new_id, (old_id, item_text) in enumerate(keep_items, start=1):
    # replace the id
    item_text = re.sub(r"(^\s*\{\s*\n\s*id:\s*)\d+(,\s*name:)", rf"\g<1>{new_id}\g<2>", item_text, count=1)
    new_items_text.append(item_text)

# We need to rejoin them carefully
# The last item might have a trailing comma, but the split was splitting at '{\n id:'. Let's look closely at how they are separated.
# Each item ends with "            }," or "            }"
# If we remove the last item (19), we need to ensure the new last item (18 -> 12) ends nicely, but a trailing comma is fine.
# Let's remove any trailing comma from the very last item in new_items_text just in case!

if len(new_items_text) > 0:
    new_items_text[-1] = re.sub(r",\s*$", "\n", new_items_text[-1].rstrip())

new_levels_str = prefix + "".join(new_items_text)

# We might have left a trailing comma if the previous string was joined.
# Wait, each `p` inside `parts` ends with `},\n`
# Actually `\n            {\n                id:` splits before the `{`.
# So each item starts with that, and ends with `},\n` except maybe the last one.
# So `"".join(new_items_text)` string is mostly correct.

html = html.replace(levels_str, new_levels_str)

# One edge case: remove trailing comma on the new last item before '];'
def fix_trailing(match):
    return match.group(1) + "\n        ];"
html = re.sub(r"},\s*\];", fix_trailing, html)

with open("index.html", "w") as f:
    f.write(html)

print("success")
