#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

template = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width" />
        <title>{title}</title>
        <link rel="stylesheet" href="style.css" type="text/css"
         media="screen" title="no title" charset="utf-8">
        <link rel="stylesheet" href="pygmentize.css" type="text/css"
         media="screen" title="no title" charset="utf-8">
    </head>
    <body>

{body}

    </body>
</html>
"""


class LinkInlineProcessor(markdown.inlinepatterns.LinkInlineProcessor):
    """Fix wiki links.

    If link text and href are equals and href doesn't provide `.html`
    extention then add it.
    """

    def handleMatch(self, *args, **kwargs):
        el, m, index = super().handleMatch(*args, **kwargs)
        href = el.get("href")
        if el.text == href and not href.endswith(".html"):
            el.set("href", href + ".html")
        return el, m, index


def main():
    args = sys.argv

    output_dir = args[4]
    file_path = args[5]
    filename, extention = os.path.splitext(os.path.basename(file_path))
    output_file = os.path.join(output_dir, filename + ".html")

    md = markdown.Markdown(extensions=["fenced_code", CodeHiliteExtension()])
    md.inlinePatterns.deregister("link")
    md.inlinePatterns.register(
        LinkInlineProcessor(markdown.inlinepatterns.LINK_RE, md), "link", 160
    )

    with open(file_path, "rb") as f:
        output = template.format(
            body=md.convert(f.read().decode()), title=filename
        )

    with open(output_file, "wb") as o:
        o.write(output.encode())


if __name__ == "__main__":
    main()
