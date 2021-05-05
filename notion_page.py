import os

from notion.block import CodeBlock, ImageBlock, TextBlock, DividerBlock

from config import Config
from utils.utils import Utils


class PageBaseBlock:
    def __init__(self):
        self.id = 'unknown'
        self.type = 'unknown'

    def write_block(self):
        return """<!-- unsupported page block
type: {}
{}
-->""".format(self.type, self._wip_msg())

    def _wip_msg(self):
        return "notion id: " + self.id


class PageTocBlock(PageBaseBlock):
    def __init__(self):
        super().__init__()
        self.type = 'table_of_contents'
        self.page_blocks = []

    def write_block(self):
        '''
        # Table of Contents
        -. [Example](#example)
        -. [Example2](#example2)
        -.   [Third Example](#third-example)
        -.   [Fourth Example](#fourth-examplehttpwwwfourthexamplecom)
        '''

        block_lines = []
        for block in self.page_blocks:
            if block.type == "header":
                block_lines.append(" - [{}](#{})".format(block.text, block.text))
            if block.type == "sub_header":
                block_lines.append(" - {}[{}](#{})".format('&nbsp;' * 4, block.text, block.text))
            if block.type == "sub_sub_header":
                block_lines.append(" - {}[{}](#{})".format('&nbsp;' * 8, block.text, block.text))

        return ("# Table of Contents\n" + "\n".join(block_lines)) if len(block_lines) > 0 else ""


class PageTextBlock(PageBaseBlock):
    def __init__(self):
        super().__init__()
        self.type = 'text'
        self.text = ''

    def write_block(self):
        return self.text


class PageEnterBlock(PageTextBlock):
    def __init__(self):
        super().__init__()
        self.type = 'enter'
        self.text = '\n'

    def write_block(self):
        return self.text


class PageDividerBlock(PageTextBlock):
    def __init__(self):
        super().__init__()
        self.type = 'divider'
        self.text = '---'

    def write_block(self):
        return self.text


class PageNumberedListBlock(PageTextBlock):
    def __init__(self):
        super().__init__()
        self.type = 'numbered_list'
        self.text = ''

    def write_block(self):
        return '0. {}'.format(self.text)


class PageBulletedListBlock(PageTextBlock):
    def __init__(self):
        super().__init__()
        self.type = 'bulleted_list'
        self.text = ''

    def write_block(self):
        return ' - {}'.format(self.text)


class PageQuoteBlock(PageTextBlock):
    def __init__(self):
        super().__init__()
        self.type = 'quote'
        self.text = ''

    def write_block(self):
        return '> {}'.format(self.text)


class PageCalloutBlock(PageTextBlock):
    def __init__(self):
        super().__init__()
        self.type = 'callout'
        self.text = ''

    def write_block(self):
        lines = str(self.text).split("\n")
        return '> ' + "> ".join(lines)


class PageHeaderBlock(PageTextBlock):
    def __init__(self):
        super().__init__()
        self.type = 'header'
        self.text = ''

    def write_block(self):
        return '# {}'.format(self.text)


class PageSubHeaderBlock(PageTextBlock):
    def __init__(self):
        super().__init__()
        self.type = 'sub_header'
        self.text = ''

    def write_block(self):
        return '## {}'.format(self.text)


class PageSubSubHeaderBlock(PageTextBlock):
    def __init__(self):
        super().__init__()
        self.type = 'sub_sub_header'
        self.text = ''

    def write_block(self):
        return '### {}'.format(self.text)


class PageCodeBlock(PageTextBlock):
    def __init__(self):
        super().__init__()
        self.type = 'code'
        self.text = ''
        self.lang = ''

    def write_block(self):
        return """```{}
{}
```
""".format(self.lang, self.text)


class PageImageBlock(PageBaseBlock):
    def __init__(self):
        super().__init__()
        self.text = 'image'
        self.image_caption = ''
        self.image_url = ''
        self.image_file = ''

    def write_block(self):
        return "![{}]({})".format(self.image_caption, self.image_url)


# noinspection PyBroadException
class NotionPage:
    """
    relative_path = None
    title = ''
    date = ''
    properties = {}
    blocks = []
    """

    def __init__(self):
        self.id = ''
        self.title = ''
        self.blocks = []
        self.properties = {}

        self.mapping = {
            "text": self._parse_text,
            "image": self._parse_image,
            "divider": self._parse_divider,
            "numbered_list": self._parse_numbered_list,
            "bulleted_list": self._parse_bulleted_list,
            "quote": self._parse_quote,
            "callout": self._parse_callout,
            "header": self._parse_header,
            "sub_header": self._parse_sub_header,
            "sub_sub_header": self._parse_sub_sub_header,
            "code": self._parse_code,
            "table_of_contents": self._parse_toc,
        }

    def is_markdown_able(self):
        return self.get_title() is not None  # and self.get_date() is not None

    def is_output_able(self):
        return self.get_file_name() is not None

    def get_identify(self):
        return "[{}]{}".format(self.id, self.get_title())

    def get_title(self):
        if 'Title' in self.properties:
            try:
                value = str(self.properties['Title'])
                if len(value) > 0:
                    return value
            except Exception as e:
                print(e)

        if len(self.title) > 0:
            return self.title
        return None

    def get_date(self):
        if 'Date' in self.properties:
            try:
                value = str(self.properties['Date'])
                if len(value) > 0:
                    return value
            except Exception as e:
                print(e)
        return None

    def get_category(self):
        if 'Category' in self.properties:
            try:
                return str(self.properties['Category'])
            except Exception as e:
                print(e)
        return None

    def get_tag(self):
        if 'Tag' in self.properties:
            try:
                return str(self.properties['Tag'])
            except Exception as e:
                print(e)
        return None

    def is_published(self):
        if 'Published' in self.properties:
            try:
                return str(self.properties['Published']) in [
                    'true',
                    '1',
                    't',
                    'y',
                    'yes',
                    'yeah',
                    'yup',
                    'certainly',
                    'uh-huh'
                ]
            except Exception as e:
                print(e)
        return False

    def get_file_dir(self):
        if 'FileLocate' in self.properties:
            try:
                value = str(self.properties['FileLocate'])
                if len(value) > 0:
                    return value
            except Exception as e:
                print(e)
        return None

    def get_file_name(self):
        if 'FileName' in self.properties:
            try:
                value = str(self.properties['FileName'])
                if len(value) > 0:
                    return value
            except Exception as e:
                print(e)

        if len(self.get_title()) > 0:
            return self.get_title()
        if len(self.id) > 0:
            return self.id
        return None

    def parse(self, page):
        self.id = str(page.id)
        self.title = str(page.title)

        # parse page blocks
        for block in page.children:
            if block.type in self.mapping:
                self.mapping[block.type].__call__(block)
                continue
            # Basic Block Parsing
            self._parse_basic(block)
        pass

    def _parse_basic(self, block):
        page_block = PageBaseBlock()
        page_block.id = block.id
        page_block.type = block.type
        self.blocks.append(page_block)

    def _parse_text(self, block):
        if len(str(block.title).strip()) == 0:
            self.blocks.append(PageEnterBlock())
            return
        page_block = PageTextBlock()
        page_block.type = block.id
        page_block.type = block.type
        page_block.text = block.title
        self.blocks.append(page_block)
        pass

    def _parse_image(self, block):
        image_id = block.id
        image_caption = str(block.caption)
        image_url = str(block.source)
        temp_file = os.path.join(Config.output(), "assets/image", image_id + "_" + image_caption, ".jpg")

        page_block = PageImageBlock()
        page_block.type = block.id
        page_block.type = block.type
        page_block.image_caption = image_caption
        page_block.image_url = image_url
        page_block.image_file = temp_file
        self.blocks.append(page_block)

    def _parse_divider(self, block):
        page_block = PageDividerBlock()
        page_block.id = block.id
        page_block.type = block.type
        self.blocks.append(page_block)

    def _parse_properties(self, block):
        content = block.title
        symbol = '[properties]'
        if symbol in content:
            content_properties = content[content.rfind(symbol) + len(symbol):]
            lines = str(content_properties).split("\n")
            for line in lines:
                if '=' in line:
                    idx = line.find('=')
                    key = line[:idx].strip()
                    value = line[idx + len('='):].strip()
                    self.properties[key] = value

    def _parse_code(self, block: CodeBlock):
        content = block.title
        symbol = '[properties]'
        if symbol in content:
            self._parse_properties(block)
            return

        page_block = PageCodeBlock()
        page_block.id = block.id
        page_block.type = block.type
        page_block.text = block.title
        page_block.lang = block.language
        self.blocks.append(page_block)

    def _parse_numbered_list(self, block):
        page_block = PageNumberedListBlock()
        page_block.id = block.id
        page_block.type = block.type
        page_block.text = block.title
        self.blocks.append(page_block)

    def _parse_bulleted_list(self, block):
        page_block = PageBulletedListBlock()
        page_block.id = block.id
        page_block.type = block.type
        page_block.text = block.title
        self.blocks.append(page_block)

    def _parse_quote(self, block):
        page_block = PageQuoteBlock()
        page_block.id = block.id
        page_block.type = block.type
        page_block.text = block.title
        self.blocks.append(page_block)

    def _parse_callout(self, block):
        page_block = PageCalloutBlock()
        page_block.id = block.id
        page_block.type = block.type
        page_block.text = block.title
        self.blocks.append(page_block)

    def _parse_header(self, block):
        page_block = PageHeaderBlock()
        page_block.id = block.id
        page_block.type = block.type
        page_block.text = block.title
        self.blocks.append(page_block)

    def _parse_sub_header(self, block):
        page_block = PageSubHeaderBlock()
        page_block.id = block.id
        page_block.type = block.type
        page_block.text = block.title
        self.blocks.append(page_block)

    def _parse_sub_sub_header(self, block):
        page_block = PageSubSubHeaderBlock()
        page_block.id = block.id
        page_block.type = block.type
        page_block.text = block.title
        self.blocks.append(page_block)

    def _parse_toc(self, block):
        page_block = PageTocBlock()
        page_block.id = block.id
        page_block.type = block.type
        page_block.page_blocks = self.blocks
        self.blocks.append(page_block)

    def _parse_stub(self, block):
        page_block = PageBaseBlock()
        page_block.id = block.id
        page_block.type = block.type
        page_block.text = block.title
        self.blocks.append(page_block)
        raise Exception('Stub!')
