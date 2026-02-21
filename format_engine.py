from jinja2 import Template

class FormatEngine:
    def __init__(self):
        self.html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Influencer Intelligence Report</title>
            <style>
                body { font-family: sans-serif; }
                .section { margin-bottom: 20px; }
                .narrative-tracker { border: 1px solid #ccc; padding: 10px; }
                .accelerating { color: green; }
                .decaying { color: red; }
            </style>
        </head>
        <body>
            <h1>AI Influencer Intelligence Report</h1>

            <div class="section">
                <h2>Content</h2>
                <div class="content">
                    {{ content }}
                </div>
            </div>

            <div class="section narrative-tracker">
                <h2>Narrative Tracker</h2>
                <div class="tracker-column">
                    <h3>Accelerating Trends</h3>
                    <ul>
                    {% for item in accelerating_trends %}
                        <li class="accelerating">{{ item.name }}</li>
                    {% endfor %}
                    </ul>
                </div>
                <div class="tracker-column">
                    <h3>Decaying Trends</h3>
                    <ul>
                    {% for item in decaying_trends %}
                        <li class="decaying">{{ item.name }}</li>
                    {% endfor %}
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """

    def generate_html(self, content, narrative_trends):
        """
        Generates an HTML report including the Narrative Tracker.

        Args:
            content (str): The main body content.
            narrative_trends (list): A list of dicts, e.g., [{'name': '...', 'status': 'Accelerating'}, ...]
        """
        accelerating = [t for t in narrative_trends if t.get('status') == 'Accelerating']
        decaying = [t for t in narrative_trends if t.get('status') == 'Decaying']

        template = Template(self.html_template)
        return template.render(
            content=content,
            accelerating_trends=accelerating,
            decaying_trends=decaying
        )

    def generate_markdown(self, content, narrative_trends):
        """
        Generates a Markdown report including the Narrative Tracker.
        """
        accelerating = [t for t in narrative_trends if t.get('status') == 'Accelerating']
        decaying = [t for t in narrative_trends if t.get('status') == 'Decaying']

        md_output = f"# AI Influencer Intelligence Report\n\n"
        md_output += f"## Content\n\n{content}\n\n"
        md_output += f"## Narrative Tracker\n\n"

        md_output += "### Accelerating Trends\n"
        for item in accelerating:
            md_output += f"- {item['name']}\n"

        md_output += "\n### Decaying Trends\n"
        for item in decaying:
            md_output += f"- {item['name']}\n"

        return md_output

# Example usage
if __name__ == "__main__":
    engine = FormatEngine()
    content = "This is the latest analysis on AI trends."
    trends = [
        {'name': 'Agentic Workflows', 'status': 'Accelerating'},
        {'name': 'Prompt Engineering Hype', 'status': 'Decaying'}
    ]

    print("HTML Output:")
    print(engine.generate_html(content, trends))
    print("\nMarkdown Output:")
    print(engine.generate_markdown(content, trends))
