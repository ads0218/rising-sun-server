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

base_url = 'http://land.naver.com'
def crawl_cateids():
    url = 'http://land.naver.com/article/divisionInfo.nhn?rletTypeCd=D01&tradeTypeCd=&hscpTypeCd=&cortarNo=4421000000&articleOrderCode='
    resp = requests.get(url)
    tree = html.fromstring(resp.content)
    lists = tree.xpath('//div[@id="top_rlet_tp"]/li/a')
    cateid_list = []
    for each_cate in lists:
        cate_id = each_cate.attrib['tpcd']
        cate_name = each_cate.text_content()
        cateid_list.append({
            'cate_name': cate_name,
            'cate_id': cate_id
        })
    return cateid_list

def strip_str(input_text):
    return re.sub('[\t\n\r]', '', input_text.strip())

index_type = {
    0: 'sale_type',
    1: 'sale_cate',
    2: 'register_date',
    3: 'item_name',
    4: 'size',
    5: 'floor',
    6: 'price',
    7: 'contact'
}

def strip(content):
    return re.sub('[\t\n\r\xa0]', '', content.strip())

def crawl_items(cateid, page=1):

    url = 'http://land.naver.com/article/divisionInfo.nhn?rletTypeCd=' + cateid + \
          '&tradeTypeCd=all&hscpTypeCd=&cortarNo=4421000000&articleOrderCode=&page='+str(page) + \
          '&location=1364#_content_list_target'
    resp = requests.get(url)
    tree = html.fromstring(resp.content)
    item_tree_lists = tree.xpath('//*[@class="sale_list _tb_site_img NE=a:cpm"]/tbody/tr')
    page_tree_lists = tree.xpath('//div[@class="paginate"]/.')
    pages_tree = page_tree_lists[0].getchildren()
    current_page_flag = False
    next_page_available = False
    for each_page_item in pages_tree:
        if current_page_flag:
            next_page_available = True
        if each_page_item.tag == 'strong':
            current_page_flag = True

    item_list = []
    for each_item_idx in range(int(len(item_tree_lists) / 2)):
        item_header_idx = each_item_idx * 2
        item_footer_idx = each_item_idx * 2 + 1
        item_info_tree = item_tree_lists[item_header_idx].xpath('td')
        item_specific_info_tree = item_tree_lists[item_footer_idx].xpath('td')
        item_obj = {}
        for idx, each_td in enumerate(item_info_tree):
            if idx == 3:
                # link
                a_list = each_td.xpath('div/a')
                if len(a_list) == 2:
                    item_obj['link'] = base_url + '/' + (a_list[1].attrib['href'])
            item_obj[index_type[idx]] = strip_str(each_td.text_content())
        item_obj['specific'] = (strip(item_specific_info_tree[0].text_content()))
        item_list.append(item_obj)

    for each_item in item_list:
        if db.session.query(Realestate).filter_by(link=each_item['link']).first() is not None:
            continue
        realestate = Realestate(
            source='naver',
            item_type=each_item['sale_cate'],
            sale_type=each_item['sale_type'],
            price=each_item['price'],
            size=each_item['size'],
            contact=each_item['contact'],
            floor=each_item['floor'],
            link=each_item['link'],
            description=each_item['specific'],
            title=each_item['item_name'],
            register_date=each_item['register_date']
        )
        db.session.add(realestate)
    db.session.commit()

    return next_page_available

@celery.task
def crawl_naver():
    cate_list = crawl_cateids()
    for each_cate in cate_list:
        page = 1
        crawl_next_page = True
        while crawl_next_page:
            print('cate name : ', each_cate['cate_name'])
            print('page : ', page)
            crawl_next_page = crawl_items(each_cate['cate_id'], page)
            page += 1
