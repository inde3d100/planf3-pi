# Export HTML — Pi Adapter

Use this workflow when the user asks for a browser-readable preview/export of a canonical Markdown plan.

## Steps

1. **Locate canonical Markdown**
   - Input: `specs/<name>.md`.
   - Output: `specs/<name>.html`.

2. **Create a self-contained HTML file**
   - Include a `<style>` block directly in the file.
   - Do not depend on external CSS or JS.
   - Preserve all plan sections.
   - Render status markers visibly.
   - Link or embed generated images using relative paths like `<name>/images/<slot>.png`.

3. **Keep Markdown canonical**
   - The HTML preview should say which Markdown file it was exported from.
   - Do not treat the HTML as the source of truth for future updates.

4. **Validate**
   - Confirm the HTML file exists.
   - Confirm there are no unreplaced template placeholders such as `{{...}}`.
   - If browser tools are available, optionally screenshot or fetch the file via a local file/server path.

5. **Report**
   - Return Markdown path and HTML path.
