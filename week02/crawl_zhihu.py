import requests
from queue import Queue
import json


def crawl(topic):

    url = f'https://www.zhihu.com/api/v4/questions/{topic}/answers?include=data[*].is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata[*].mark_infos[*].url%3Bdata[*].author.follower_count%2Cbadge[*].topics%3Bsettings.table_of_content.enabled%3B&limit=20&offset=0&platform=desktop&sort_by=default'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

    dataQueue = Queue()
    parseQueue = Queue()

    dataQueue.put(url)
    is_end = False
    while not is_end and not dataQueue.empty():
        next_url = dataQueue.get()
        raw_re = requests.get(next_url, headers=headers).text
        raw_dict = json.loads(raw_re)

        is_end = raw_dict['paging']['is_end']
        next_url = raw_dict['paging']['next']
        dataQueue.put(next_url)
        parseQueue.put(raw_dict['data'])


    with open('book.json', 'a', encoding='utf-8') as f:
        json_dict = {}
        while not parseQueue.empty():
            raw_data = parseQueue.get()
            for data in raw_data:
                name = data['author']['name']
                comment = data['excerpt']

                response = {
                    name: comment
                }

                json_dict.update(response)
        json.dump(json_dict, fp=f, ensure_ascii=False)

if __name__ == '__main__':
    topic = input('topic number')
    crawl(topic)