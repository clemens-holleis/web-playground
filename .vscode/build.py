#!/usr/bin/env python3

from pathlib import Path
import urllib.parse
from textwrap import dedent, indent

INDENT = lambda x=1 : " "*(4*x)
class IndexBuilder:
    def __init__(self) -> None:
        print('starting build')
        self.root = Path(__file__).parent.parent
        self.index = (self.root / 'index.html')

    @property
    def index_files(self) -> list[Path]:
        return [file for file in self.root.rglob("index.html") if file.parent != self.root]

    @property
    def rel_index_files_str(self) -> list[str]:
        return [str(file.relative_to(self.root)) for file in self.index_files]

    @property
    def link_names_urls(self) -> list[tuple[str, str]]:
        return [(file.rsplit('/',maxsplit=1)[0].replace('/', ' > '), urllib.parse.quote(file)) for file in self.rel_index_files_str]
    
    @property
    def template(self) -> str:
        txt = self.index.read_text()
        a,b,_ = txt.partition('<ul>')
        _,c,d = txt.rpartition('</ul>')

        return f'{a}{b}%%list%%{INDENT(1)}{c}{d}'


    @property
    def html_links(self) -> str:
        raw = [f"""
                <li>
                    <a href="{url}">{name}</a>
                </li>
                """
                for name, url in self.link_names_urls
            ]
        return indent(dedent("".join(raw)), INDENT(2))
    
    def build(self):
        self.index.write_text(
            self.template.replace('%%list%%', self.html_links)
        )

if __name__ == "__main__":
    IndexBuilder().build()
