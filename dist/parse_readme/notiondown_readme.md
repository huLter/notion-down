
![Page Cover](https://www.notion.so/image/https%3A%252F%252Fwww.notion.so%252Fimages%252Fpage-cover%252Fnasa_buzz_aldrin_on_the_moon.jpg)

# Notion Down

![](https://circleci.com/gh/kaedea/notion-down.svg?style=shield&circle-token=9f4dc656e94d8deccd362e52400c96e709c7e8b3)

[Notion Down](https://github.com/kaedea/notion-down), python tools that convert Notion blog pages into Markdown files, along with intergation to build static webpages such as Hexo.  It's inspiration and goal is to __avoid separation  of writting__ by keep writting drafts or posts within [notion.so](http://notion.so) and then publish them into MD webpages automatically. 



## Features

What can notion-down do now:

 - Notion pages to MarkDown files
     - ~~Basic Notion PageBlocks parsing~~
     - ~~Notion images refer & download~~
     - ~~Notion nested list blocks~~
     - ~~Notion obfuscated-links parsing~~
     - ~~Notion table block (Collection)~~
     - Notion subpage link parsing
 - Advanced Notion PageBlocks support
     - ~~Pullquote Blocks~~
     - Notion page embed blocks
     - Image source replacing
 - Writing optimized integration
     - ~~Noton custom `ShortCode` blocks that control parametered MD files generating~~
     - ~~Mixed CN-EN text separation format~~ ([by pangu](https://github.com/vinta/pangu))
     - ~~Spelling inspect~~ (by [pycorrector](https://github.com/shibing624/pycorrector))
 - HEXO Integration
     - ~~HEXO page properties config~~
     - HEXO generate
     - HEXO tags plugin

## Hot It Works

![NotionDown Workflows](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/21da4ef8-bdce-4d8a-8691-8d6cf4e726cd/NotionDown.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210530%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210530T114622Z&X-Amz-Expires=86400&X-Amz-Signature=e1b8959a42396f6127e1e30a2269b7ea87d8e88600359d3be69ce4177b402ccd&X-Amz-SignedHeaders=host)

NotionDown read Notion pages data using [notion-py](https://github.com/jamalex/notion-py), and then write pages into MD files.

### Basic usage

> notion-down >> Notion APIs (notion-py) >> Notion pages data >> generating MD files

### Advanced usage

> WebHook >> notion-down >> Notion APIs (notion-py) >> Notion pages data >> generating MD files >> Copy into Hexo source >> generating webpages >> push to GitHub pages

## Getting Started

Set `notion_token_v2` at System ENV or `config.py` first, and then check the following procedures. <br>Check [here](https://github.com/kaedea/notion-down/blob/master/dist/parse_readme/notiondown_gettokenv2.md) to get notion_token_v2.

### UnitTest Examples

See unitest cases at `/test`.

### CI Build Script

See building script at `/.circleci/config.yaml`.

### Showcases

See the usage showcase jobs at [/jobs](/jobs), and jobs outputs at [/dist](/dist).

 - [README generating](/jobs/parse_readme/)
 - [Notion sample post generating](/jobs/parse_sample_posts/)
 - Hexo public generating (WIP)

---

> This page is generated by [notion-down](https://github.com/kaedea/notion-down) from [notion.so NotionDown-README](https://www.notion.so/kaedea/NotionDown-README-d3463f3d398743879d663caf87efa029).




<!-- Generated by NotionPageWriter
notion-down.version = 0.0.1
notion-down.revision = b'9b7981c'
-->