import os
import re

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_liquid_line(line, page_url):
    # Replace {% if page.url == '...' %}class1{% else %}class2{% endif %} with class1 or class2 based on page_url
    import re
    pattern = r'\{% if page\.url == \'([^\"]*)\' %}([^%]*)\{% else %}([^%]*)%\}'
    def replacement(match):
        url = match.group(1)
        if url == page_url:
            return match.group(2)
        else:
            return match.group(3)
    return re.sub(pattern, replacement, line)

def replace_includes(content, page_url=None):
    include_pattern = r'\{% include ([^%]+) %}'
    while re.search(include_pattern, content):
        match = re.search(include_pattern, content)
        if match:
            include_path = match.group(1).strip()
            full_path = os.path.join('_includes', include_path)
            if os.path.exists(full_path):
                include_content = load_file(full_path)
                content = content.replace(match.group(0), include_content, 1)
            else:
                content = content.replace(match.group(0), f'<!-- Include not found: {include_path} -->', 1)
    return content

def build_site():
    layouts = {}
    for root, dirs, files in os.walk('_layouts'):
        for file in files:
            if file.endswith('.html'):
                layouts[file.replace('.html', '')] = os.path.join(root, file)

    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html') and file not in ['build.py']:
                file_path = os.path.join(root, file)
                content = load_file(file_path)

                # Check if has front matter
                if content.startswith('---\n'):
                    # Split front matter
                    parts = content.split('---\n', 2)
                    if len(parts) >= 3:
                        front_matter = parts[1]
                        body = parts[2]
                        # Parse layout from front_matter, simple
                        layout = None
                        for line in front_matter.split('\n'):
                            if line.strip().startswith('layout:'):
                                layout = line.split(':', 1)[1].strip()

                        if layout in layouts:
                            page_url = '/' if file == 'index.html' else '/' + file
                            layout_content = load_file(layouts[layout])
                            # Replace {{ content }} with body
                            body = process_liquid_line(body, page_url)
                            built_content = layout_content.replace('{{ content }}', body)
                            # Replace includes in built_content
                            built_content = replace_includes(built_content, page_url)
                            # Process liquid in includes
                            built_content = process_liquid_line(built_content, page_url)
                            # Hard code nav classes based on page
                            if file == 'index.html':
                                built_content = built_content.replace('{% if page.url == "/" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'font-semibold text-black')
                                built_content = built_content.replace('{% if page.url == "/about.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/portfolio.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/contact.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                            elif file == 'about.html':
                                built_content = built_content.replace('{% if page.url == "/" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/about.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'font-semibold text-black')
                                built_content = built_content.replace('{% if page.url == "/portfolio.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/contact.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                            elif file == 'portfolio.html':
                                built_content = built_content.replace('{% if page.url == "/" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/about.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/portfolio.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'font-semibold text-black')
                                built_content = built_content.replace('{% if page.url == "/contact.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                            elif file == 'contact.html':
                                built_content = built_content.replace('{% if page.url == "/" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/about.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/portfolio.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/contact.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'font-semibold text-black')
                            elif file == 'services.html':  # Assume services.html exists
                                built_content = built_content.replace('{% if page.url == "/" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/about.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/portfolio.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                                built_content = built_content.replace('{% if page.url == "/contact.html" %}font-semibold text-black{% else %}text-gray-500{% endif %}', 'text-gray-500')
                            # Save to file_path
                            save_file(file_path, built_content)
                            print(f'Built {file_path}')
                        else:
                            print(f'No layout found for {file_path}')
                    else:
                        print(f'Front matter malformed in {file_path}')
                else:
                    # No front matter, perhaps copy as is
                    pass

if __name__ == '__main__':
    build_site()
