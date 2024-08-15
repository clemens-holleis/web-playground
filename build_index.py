from logging import root
from pathlib import Path
import urllib.parse
from textwrap import dedent, indent


class IndexBuilder:
    def __init__(self) -> None:
        self.root = Path(__file__).parent
        self.template = (self.root / 'index.twig').read_text()
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
    def html_links(self) -> str:
        raw = [f"""
                <li>
                    <a href="{url}">{name}</ul>
                </li>
                """
                for name, url in self.link_names_urls
            ]
        return indent(dedent("".join(raw)), "       ").strip()
    
    def build(self):
        self.index.write_text(
            self.template.replace('{{list}}', self.html_links)
        )

if __name__ == "__main__":
    IndexBuilder().build()
