import requests
import json
from pprint import pprint
from lxml import html
from app_server.models.realestate_model import Realestate
from app_server.common.instances.db import db
from app_server.common.instances.celery import celery

import requests
import asyncio
import re

base_url = 'http://land.findall.co.kr'
def crawl_cateids():
    url = 'http://land.findall.co.kr/land_new/subLand.asp?hidSectionCd=1&hidSearchGbn=area&hidFindcode=3000221&selMetro=%C3%E6%B3%B2&selCity=%BC%AD%BB%EA%BD%C3'
    resp = requests.get(url)
    tree = html.fromstring(resp.content)
    lists = tree.xpath('//ul[@class="depth3_list"]/li/a')
    cateid_list = []
    for each_cate in lists:
        href = each_cate.attrib['href']
        substr_href = href[href.find('hidFindcode='):]
        hidFindcode = substr_href[12:substr_href.find('&')]
        cateid_list.append({
            'cate_name': each_cate.text_content(),
            'cate_id': hidFindcode
        })
    return cateid_list

def crawl_items(cateid, page=1):
    url = 'http://land.findall.co.kr/land_new/subLand.asp?hidSearchGbn=area&hidSectionCd=' + str(cateid) + \
          '&selMetro=%C3%E6%B3%B2&selCity=%BC%AD%BB%EA%BD%C3&page=' + str(page)
    # url = 'http://land.findall.co.kr/land_new/subLand.asp?hidSearchGbn=area&hidFindcode=' + cateid + \
    #       '&selMetro=%C3%E6%B3%B2&selCity=%BC%AD%BB%EA%BD%C3&page=' + str(page)
    resp = requests.get(url)
    tree = html.fromstring(resp.content)
    type_tree_lists = tree.xpath('//*[@id="spCommonList"]/div[2]/table/thead/tr/th')
    type_lists = []
    for each_cate in type_tree_lists:
        type_lists.append(each_cate.attrib['class'])
    print(type_lists)
    pages_tree = tree.xpath('//div[@class="pgSt"]/*')[1:-1]
    print('pages_tree', pages_tree)
    current_page_flag = False
    next_page_available = False
    for each_page_item in pages_tree:
        if current_page_flag:
            next_page_available = True
        if each_page_item.tag == 'strong':
            current_page_flag = True

    item_tree_lists = tree.xpath('//*[@id="spCommonList"]/div[2]/table/tbody/tr')
    item_list = []
    for each_item_idx in range(int(len(item_tree_lists) / 2)):
        item_header_idx = each_item_idx * 2
        item_footer_idx = each_item_idx * 2 + 1
        item_info_tree = item_tree_lists[item_header_idx].xpath('td')
        item_specific_info_tree = item_tree_lists[item_footer_idx].xpath('td')
        item_obj = {}
        item_obj[type_lists[0]] = item_info_tree[0].xpath('*/span')[-1].text_content()
        item_obj[type_lists[1]] = item_info_tree[1].text_content().strip()
        item_obj['url'] = base_url + item_info_tree[1].xpath('a')[0].attrib['href']
        for type_idx in range(2, len(type_lists)):
            item_obj[type_lists[type_idx ]] = item_info_tree[type_idx ].text_content().strip()

        item_obj['specific'] = re.sub('[\t\n\r]', '', item_specific_info_tree[0].text_content().strip())
        item_list.append(item_obj)

    for each_item in item_list:
        if db.session.query(Realestate).filter_by(link=each_item['url']).first() is not None:
            continue
        realestate = Realestate(
            source='byerook',
            item_type=each_item['type'],
            price=each_item['price'],
            size=each_item['area'],
            address=each_item['address'],
            contact=each_item['tel'],
            link=each_item['url'],
            description=each_item['specific'],
        )
        db.session.add(realestate)
    db.session.commit()

    return next_page_available

@celery.task
def crawl_byerook():
    for each_sec_id in range(1, 6):
        page = 1
        crawl_next_page = True
        while crawl_next_page:
            print('section id', each_sec_id)
            print('page', page)
            crawl_next_page = crawl_items(each_sec_id, page)
            page += 1
