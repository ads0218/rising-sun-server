import requests
import json
from pprint import pprint
from lxml import html
import requests
from app_server.models.realestate_model import Realestate
from app_server.common.instances.db import db
from app_server.common.instances.celery import celery


cateids = {
    "000000": "아파트",
    "000001": "아파트분양권",
    "000002": "주상복합",
    "000003": "주상복합분양권",
    "000004": "오피스텔/도시형",
    "000005": "오피스텔/도시형분양권",
    "000006": "재개발",
    "000007": "재건축",
    "000008": "단독/다가구",
    "000009": "원룸/투룸/쓰리룸",
    "000010": "하숙/고시원/잠만잘분",
    "000011": "빌라/연립/다세대",
    "000012": "전원/농가주택",
    "100000": "빌딩",
    "100001": "상가주택",
    "100002": "상가점포",
    "100003": "사무실",
    "100004": "토지/임야",
    "100005": "공장/창고",
    "100006": "숙박/콘도/펜션",
    "100007": "상가건물",
    "109998": "경매",
    "109999": "기타"
}

def crawl_kcrbds(cateids, npg=1):
    base_url = 'http://ss.kcrbds.co.kr'
    url = 'http://ss.kcrbds.co.kr/find/getList.si.ajax.php'
    params = {
        'domainkey': '47',
        'gcateid': '09',
        'cateids': cateids,  # '100004',
        'trans': None,
        'areaid': '001006',
        'containareaid': None,
        'offertype': None,
        'al': None,
        'ah': None,
        'pl': None,
        'ph': None,
        'buildtype': None,
        'propose_business': None,
        'npg': npg,
        'spg': '1',
        'tmpareaid': '001006',
        'spl': None,
        'sph': None,
        's_p3': None
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'caid=0010; __utma=70776074.766544971.1485501165.1485501165.1485501165.1; __utmc=70776074; __utmz=70776074.1485501165.1.1.utmcsr=icross.co.kr|utmccn=(referral)|utmcmd=referral|utmcct=/index.icross; rvo0=1296851386%7C%25uC784%25uC57C%7C%25uB9E4%25uB9E4%7C%253C%2573%2570%2561%256E%253E%2531%2536%2532%2533%25u33A1%253C%2F%2573%2570%2561%256E%253E%7C%2531%2532%2537%252C%2530%2530%2530%25uB9CC%25uC6D0%7C%2520%25uC11C%25uC0B0%25uC2DC%2520%25uC778%25uC9C0%25uBA74; i_key=824455bd1d067162e4ae4ca71d42336d; __utma=58374312.733175157.1485501170.1485501170.1485668744.2; __utmb=58374312.60.10.1485668744; __utmc=58374312; __utmz=58374312.1485668744.2.2.utmcsr=kcrbds.co.kr|utmccn=(referral)|utmcmd=referral|utmcct=/loading/icross_main_move.php; level=9; THIS_PAGE=http%3A%2F%2Fss.kcrbds.co.kr%2Ffind%2FfindSi.php%3Fcateids%3D100004%26trans%3D1%26areaid%3D001006; kcrbds_ak=001006%7Csskcr; pkcrid=sskcr',
        'Origin': 'http://ss.kcrbds.co.kr',
        'Referer': 'http://ss.kcrbds.co.kr/find/findSi.php?cateids=100001&trans=1&areaid=001006',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    resp = requests.post(url=url, data=params, headers=headers, timeout=3)
    content_res = resp.content.decode('euc-kr')
    content_res_json = json.loads(content_res)
    if content_res_json['list'] is None:
        return False
    item_list = []
    for each_item in content_res_json['list']:
        item_obj = {}
        item_obj['size'] = each_item['area1']
        item_obj['cate'] = each_item['cate_name']
        item_obj['date'] = each_item['date']
        item_obj['dong'] = each_item['dong']
        item_obj['dong_title'] = each_item['dong_title']
        item_obj['list_title'] = each_item['list_title']
        item_obj['name'] = each_item['name']
        item_obj['img'] = each_item['img']
        item_obj['price'] = each_item['price']
        item_obj['price_title'] = each_item['price_title']
        item_obj['tel'] = each_item['tel']
        item_obj['trans_name'] = each_item['trans_name']
        item_obj['view_title'] = each_item['view_title']
        item_obj['view_url'] = base_url + each_item['view_url'][2:]
        pprint(item_obj)
        item_list.append(item_obj)
        print('-------------')

    for each_item in item_list:
        if db.session.query(Realestate).filter_by(link=each_item['view_title']).first() is not None:
            continue
        realestate = Realestate(
            source='gyocharo',
            item_type=each_item['cate'],
            sale_type=each_item['trans_name'],
            price=each_item['price'],
            size=each_item['size'],
            address=each_item['dong'],
            contact=each_item['name'] + ' ' + each_item['tel'],
            link=each_item['view_url'],
            description=each_item['list_title'],
            title=each_item['view_title']
        )
        db.session.add(realestate)
    db.session.commit()

    if len(item_list) == 20:
        # Crawl Next Page
        return True
    else:
        return False

def crawl_cate_pages(cateid):
    page = 1
    crawl_next_page = True
    while crawl_next_page:
        crawl_next_page = crawl_kcrbds(cateid, page)
        page += 1

def crawl_cates():
    for cateid, catename in cateids.items():
        crawl_cate_pages(cateid)

@celery.task
def crawl_gyocharo():
    crawl_cates()