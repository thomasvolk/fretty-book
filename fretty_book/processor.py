# -*- coding: utf-8 -*-

import re
from fretty import generate_svg, write_image
import os


class DocumentProcessor:
    def __init__(self, embedded=True, png_images=False, output_file=None):
        self.embedded = embedded
        self.png_images = png_images
        self.output_file = output_file

    @property
    def document_dir(self):
        return os.path.dirname(self.output_file) if self.output_file else '.'

    @property
    def image_extension(self):
        return 'png' if self.png_images else 'svg'

    def process_file(self, input_file):
        with open(input_file) as f:
            return self.process_text(f.read())

    def process_text(self, input):
        return self._process(input)

    def _process(self, input):
        return input

    def _generate(self, markup, attrs):
        lines = markup.strip().split('\n')
        return generate_svg(
            lines,
            width=attrs.get('width'),
            height=attrs.get('height'),
            embedded=self.embedded,
            drawing_color=attrs.get('drawing_color', 'black'),
            label_color=attrs.get('label_color', 'white'),
        )

    def _external_image(self, index, svg):
        name = f"fretty-{index}.{self.image_extension}"
        return write_image(name, svg, target_path=self.document_dir)


class HTMLDocumentProcessor(DocumentProcessor):
    def _process(self, html_input):
        import lxml.html

        doc = lxml.html.document_fromstring(html_input)
        for idx, node in enumerate(doc.findall(".//fretty")):
            svg = self._generate(node.text, dict(node.attrib))
            if self.embedded:
                replace_node = lxml.html.fromstring(svg)
            else:
                replace_node = lxml.html.fromstring(f'<img src="{self._external_image(idx, svg)}" />')
            node.getparent().replace(node, replace_node)
        return lxml.html.tostring(doc, encoding='unicode')


class XHTMLDocumentProcessor(DocumentProcessor):
    def _process(self, xhtml_input):
        from xml.dom.minidom import parseString

        dom = parseString(xhtml_input)
        for idx, node in enumerate(list(dom.getElementsByTagName("fretty"))):
            markup = ''.join(child.data for child in node.childNodes)
            attrs = {node.attributes.item(i).name: node.attributes.item(i).value
                     for i in range(node.attributes.length)}
            svg = self._generate(markup, attrs)
            if self.embedded:
                replace_node = parseString(svg)
            else:
                replace_node = parseString(f'<img src="{self._external_image(idx, svg)}" />')
            node.parentNode.replaceChild(replace_node.documentElement, node)
        return dom.toxml()


class MarkdownDocumentProcessor(DocumentProcessor):
    _BLOCK = re.compile(r'```fretty([^\n]*)\n(.*?)```', re.DOTALL)

    @staticmethod
    def _parse_attrs(attr_str):
        return dict(re.findall(r'(\w+)=(\S+)', attr_str))

    def _process(self, text):
        count = 0

        def replace(m):
            nonlocal count
            attrs = self._parse_attrs(m.group(1))
            svg = self._generate(m.group(2), attrs)
            idx = count
            count += 1
            if self.embedded:
                return svg
            return f'![fretty]({self._external_image(idx, svg)})'

        return self._BLOCK.sub(replace, text)


class OrgDocumentProcessor(DocumentProcessor):
    _BLOCK = re.compile(r'#\+begin_src fretty([^\n]*)\n(.*?)#\+end_src', re.DOTALL | re.IGNORECASE)

    @staticmethod
    def _parse_attrs(attr_str):
        return dict(re.findall(r':(\w+)\s+(\S+)', attr_str))

    def _process(self, text):
        count = 0

        def replace(m):
            nonlocal count
            attrs = self._parse_attrs(m.group(1))
            svg = self._generate(m.group(2), attrs)
            idx = count
            count += 1
            if self.embedded:
                return f'#+begin_export html\n{svg}\n#+end_export'
            return f'[[file:{self._external_image(idx, svg)}]]'

        return self._BLOCK.sub(replace, text)
