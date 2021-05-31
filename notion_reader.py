import typing

from utils.utils import Utils

if not Utils.check_module_installed("notion"):
    raise Exception("Pls call 'pip install notion' first!")

from typing import List
from notion.block import PageBlock
from notion.client import NotionClient
from config import Config
from notion_page import NotionPage

NOTION_CLIENT = None


class NotionReader:

    @staticmethod
    def get_client() -> NotionClient:
        global NOTION_CLIENT
        if not NOTION_CLIENT:
            NOTION_CLIENT = NotionClient(token_v2=Config.token_v2())
        return NOTION_CLIENT

    @staticmethod
    def read_main_page() -> PageBlock:
        print("#read_main_page")
        return NotionReader.get_client().get_block(Config.blog_url())

    @staticmethod
    def handle_post() -> List[NotionPage]:
        print("#handle_post")
        print("read all pages from main page")
        page_blocks = NotionReader._read_post_pages()

        print("parse all pages")
        notion_pages = []
        for page in page_blocks:
            notion_pages.append(NotionReader._parse_page(page))

        print("Done\n\n")
        return notion_pages

    @staticmethod
    def handle_page_with_title(page_title: str) -> typing.Optional[NotionPage]:
        print("#handle_page_with_title: " + page_title)
        pages = NotionReader._read_post_pages()
        find_one = Utils.find_one(pages, lambda it: it.title == page_title)
        if not find_one:
            return None
        return NotionReader._parse_page(find_one)

    @staticmethod
    def handle_single_page(page) -> NotionPage:
        print("#handle_single_page")
        return NotionReader._parse_page(page)

    @staticmethod
    def _read_post_pages() -> typing.List[PageBlock]:
        # get all pages
        main_page = NotionReader.read_main_page()
        page_blocks = []
        NotionReader._recurse_read_page(page_blocks, main_page)

        # filter by config
        titles = Config.page_titles()
        if len(titles) < 1 or titles == ['all']:
            return page_blocks
        return [it for it in page_blocks if it.title in titles]

    @staticmethod
    def _recurse_read_page(page_blocks: typing.List[PageBlock], page: PageBlock):
        if page and page.type == 'page':
            page_blocks.append(page)

        if page.children:
            for subpage in page.children:
                if subpage.type == 'page':
                    NotionReader._recurse_read_page(page_blocks, subpage)

        pass

    @staticmethod
    def _parse_page(page: PageBlock) -> NotionPage:
        print("parse page, id = " + page.id)
        notion_page = NotionPage()
        notion_page.parse(page)
        return notion_page




