import json
from html.parser import HTMLParser

class Element:
    '''
    Utility class for Parser
    '''
    def __init__(self, name, attr, pos):
        self.name = name.lower()
        attr = dict(attr)
        self.attr = attr
        self.content = ''
        self.pos = pos

    def __repr__(self):
        return self.serialize()

    def serialize(self, as_json=False):
        if as_json:
            return json.dumps({
                'name': self.name,
                'pos': self.pos,
                'attr': self.attr,
                'content': self.content,
            })
        classes = '.'.join(self.attr.get('class', '').split())
        classes = classes and '.' + classes
        id_ = self.attr.get('id', '')
        id_ = id_ and '#'+ id_
        return f'<{self.name}{id_}{classes}>'

    def __contains__(self, value):
        return value in self.content


class Row:
    def __init__(self, elements):
        self.elements = elements
        self._path = None

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, pos):
        return self.elements[pos]

    def serialize(self, as_json=False):
        if as_json:
            return json.dumps([{
                'name': el.name,
                'pos': el.pos,
                'attr': el.attr,
                'content': el.content,
            } for el in self.elements])
        content = self.leaf.content
        content = content if len(content) < 30 else content[:27] + '...'
        path = self.path
        # path = path if len(path) < 80 else '...' + path[-77:]
        return f'{path} {content}'

    def __repr__(self):
        return self.serialize()

    def __iter__(self):
        return iter(self.elements)

    @property
    def path(self):
        if self._path is None:
            self._path = ''.join(str(el) for el in self.elements)
        return self._path

    @property
    def leaf(self):
        return self.elements[-1]


class Flattener(HTMLParser):
    '''
    Flatten html tree into a list of rows
    '''
    _self_closing = set([
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr",
    ])

    def __init__(self, content):
        self.rows = []
        self.stack = []
        super().__init__()
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        pos = 0
        if self.rows:
            prev_row = self.rows[-1]
            if len(prev_row) == 1:
                pos = prev_row[-1].pos + 1
            elif self.stack and prev_row[-2] == self.stack[-1]:
                pos = prev_row[-1].pos + 1
        el = Element(tag, attrs, pos)
        self.stack.append(el)

        # Append current stack into self.rows
        self.rows.append(Row(tuple(self.stack)))
        if el.name in self._self_closing:
            self.stack.pop()

    def handle_endtag(self, tag):

        # We could in theory simply call pop, but some pages do not
        # like to close all their tags, so keep popping until we find
        # the correct tag
        while self.stack:
            leaf = self.stack and self.stack[-1]
            self.stack.pop()
            if tag == leaf.name:
                break

    def handle_data(self, content):
        content = content.strip()
        if not content:
            return
        if not self.stack:
            return
        leaf = self.stack[-1]
        leaf.content += content

    def __iter__(self):
        return iter(self.rows)

if __name__ == '__main__':
    import os
    import argparse
    import urllib.request

    parser = argparse.ArgumentParser(description='Flattener')
    parser.add_argument('url', help='Url to load')
    parser.add_argument('--json', help='Json output', action='store_true')
    args = parser.parse_args()

    if os.path.isfile(args.url):
        content = open(args.url, 'r').read()
    else:
        req = urllib.request.Request(args.url)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode()

    parser = Flattener(content)
    for row in parser:
        print(row.serialize(args.json))
