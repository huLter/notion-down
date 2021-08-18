import os
import unittest
from pprint import pprint

from notion_client import Client, client

from utils.utils import Utils


class NotionCiTest(unittest.TestCase):

    def setUp(self):
        if not Utils.check_module_installed("notion-client"):
            raise Exception('Install notion client first: pip install notion-client')
        self.notion = Client(auth=os.environ["NOTION_TOKEN"])

    def test_get_users(self):
        list_users_response = self.notion.users.list()
        pprint(list_users_response)
        self.assertIsNotNone(list_users_response)
        self.assertEqual('list', list_users_response['object'])
        users = list_users_response['results']
        self.assertTrue(len(users) >= 0)
        pass

    def test_search_data_base(self):
        search_database = self.notion.search(filter={"property": "object", "value": "database"})
        pprint(search_database)
        self.assertIsNotNone(search_database)
        pass

    def test_search_page(self):
        rsp = self.notion.search(filter={"property": "object", "value": "page"})
        pprint(rsp)
        self.assertIsNotNone(rsp)
        self.assertEqual('list', rsp['object'])
        pages = rsp['results']
        self.assertTrue(len(pages) >= 0)
        pass

    def test_list_page(self):
        """
        Page {
            id,
            url,
            properties: [str : Block]
        }
        Block {
            type,
            (type): str/list/dict
        }
        """
        rsp = self.notion.search(filter={"property": "object", "value": "page"})
        pprint(rsp)
        self.assertEqual('list', rsp['object'])
        pages = rsp['results']
        self.assertTrue(len(pages) >= 0)

        for page in pages:
            self.assertEqual('page', page['object'])
            page_id = page['id']
            page_url = page['url']
            page_properties = page['properties']
            if 'title' in page_properties:
                title_property = page_properties['title']
                self.assertEqual('title', title_property['type'])
                titles = title_property['title']
                self.assertTrue(len(titles) >= 0)
        pass

    def test_list_page_blocks(self):
        rsp = self.notion.search(filter={"property": "object", "value": "page"})
        pprint(rsp)
        self.assertEqual('list', rsp['object'])
        pages = rsp['results']
        self.assertTrue(len(pages) >= 0)

        page = Utils.find_one(pages, lambda it: it['id'] == '440de7dc-a898-40b6-b3ba-b13d2aa92a34')

        self.assertEqual('page', page['object'])
        page_id = page['id']
        rsp = self.notion.blocks.children.list(page_id)
        self.assertIsNotNone(rsp)
        self.assertEqual('list', rsp['object'])
        blocks = rsp['results']
        for block in blocks:
            self.assertEqual('block', block['object'])
            block_id = block['id']
            block_type = block['type']
            block_content = block[(block_type)]
        pass