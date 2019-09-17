#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os
import sys

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

default_template = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <meta name="date" content="%date%" scheme="YYYY-MM-DD">
        <meta name="viewport" content="width=device-width" />
        <title>%title%</title>
        <link rel="stylesheet" href="%root_path%style.css" type="text/css"
         media="screen" title="no title" charset="utf-8">
        <link rel="stylesheet" href="%root_path%pygmentize.css" type="text/css"
         media="screen" title="no title" charset="utf-8">
    </head>
    <body>

%content%

    </body>
</html>
"""


class LinkInlineProcessor(markdown.inlinepatterns.LinkInlineProcessor):
    """Fix wiki links"""

    def getLink(self, *args, **kwargs):
        href, title, index, handled = super().getLink(*args, **kwargs)
        if not href.startswith("http") and not href.endswith(".html"):
            href += ".html"
        return href, title, index, handled


def main():

    FORCE = sys.argv[1]  # noqa - not supported
    SYNTAX = sys.argv[2]
    EXTENSION = sys.argv[3]  # noqa - not supported
    OUTPUT_DIR = sys.argv[4]
    INPUT_FILE = sys.argv[5]
    CSS_FILE = sys.argv[6]  # noqa - not supported
    TEMPLATE_PATH = sys.argv[7]
    TEMPLATE_DEFAULT = sys.argv[8]
    TEMPLATE_EXT = sys.argv[9]
    ROOT_PATH = sys.argv[10]

    # Only markdown is supported
    if SYNTAX != "markdown":
        sys.stderr.write("Unsupported syntax: " + SYNTAX)
        sys.exit(1)

    # Asign template
    template = default_template
    template_file = (
        os.path.join(TEMPLATE_PATH, TEMPLATE_DEFAULT) + TEMPLATE_EXT
    )
    if os.path.isfile(template_file):
        with open(template_file, "rb") as f:
            template = f.read().decode()

    # Get output filename
    filename, _ = os.path.splitext(os.path.basename(INPUT_FILE))
    output_file = os.path.join(OUTPUT_DIR, filename + ".html")

    extensions = ["fenced_code", "tables"]
    extensions += os.getenv("VIMWIKI_MARKDOWN_EXTENSIONS", "").split(",")
    extensions = set([e for e in extensions if e] + [CodeHiliteExtension()])

    # Setup markdown parser
    md = markdown.Markdown(extensions=extensions)
    md.inlinePatterns.deregister("link")
    md.inlinePatterns.register(
        LinkInlineProcessor(markdown.inlinepatterns.LINK_RE, md), "link", 160
    )

    with open(INPUT_FILE, "rb") as f:
        content = ""
        placeholders = {}

        # Retrieve vimwiki placeholders
        for line in f:
            line = line.decode()[:-1]
            if line.startswith("%nohtml"):
                sys.exit(0)
            elif line.startswith("%title"):
                placeholders["%title%"] = line[7:]
            elif line.startswith("%date"):
                placeholders["%date%"] = line[6:]
            elif line.startswith("%template"):
                placeholders["template"] = line[10:]
            else:
                content += line + "\n"

        # Set default values
        if "%title%" not in placeholders:
            placeholders["%title%"] = filename
        if "%date%" not in placeholders:
            placeholders["%date%"] = datetime.datetime.today().strftime(
                "%Y-%m-%d"
            )
        if "template" in placeholders:
            t = placeholders.pop("template")
            template_file = os.path.join(TEMPLATE_PATH, t) + TEMPLATE_EXT
            if os.path.isfile(template_file):
                with open(template_file, "rb") as f:
                    template = f.read().decode()

        # Parse template
        for placeholder, value in placeholders.items():
            template = template.replace(placeholder, value)
        template = template.replace(
            "%root_path%", ROOT_PATH if ROOT_PATH != "-" else "./"
        )

        # Parse content
        content = md.convert(content)

        # Merge template
        template = template.replace("%content%", content)

    with open(output_file, "wb") as o:
        o.write(template.encode())


if __name__ == "__main__":
    main()
