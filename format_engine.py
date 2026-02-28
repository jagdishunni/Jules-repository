import jinja2

class FormatEngine:
    def __init__(self):
        pass

    def render_html(self, data, template_string):
        """
        Renders HTML using a Jinja2 template string and data.
        """
        try:
            template = jinja2.Template(template_string)
            return template.render(**data)
        except Exception as e:
            return f"Error rendering HTML: {str(e)}"

    def render_markdown(self, data):
        """
        Renders a Markdown representation of the data.
        """
        md_output = ""

        # Handle title
        if 'title' in data:
            md_output += f"# {data['title']}\n\n"

        # Handle description or summary if present
        if 'summary' in data:
            md_output += f"**Summary:** {data['summary']}\n\n"

        # Handle main content
        if 'content' in data:
            md_output += f"{data['content']}\n\n"

        # Handle sections if it's a list of sections
        if 'sections' in data and isinstance(data['sections'], list):
            for section in data['sections']:
                if isinstance(section, dict):
                    if 'heading' in section:
                        md_output += f"## {section['heading']}\n\n"
                    if 'body' in section:
                        md_output += f"{section['body']}\n\n"
                else:
                    md_output += f"{section}\n\n"

        return md_output
