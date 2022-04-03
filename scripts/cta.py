import os
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from io import StringIO


CTA_ARRIVALS = {
    'base_url': 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?',
    'key': os.environ['CTA_API_KEY']
}

def main():
    stpid = 30023
    resp = requests.get(CTA_ARRIVALS['base_url'], params=dict(
        # mapid=None,
        # mapid=40120,
        # stpid=None,
        stpid=stpid,
        # https://www.transitchicago.com/traintracker/arrivaltimes/?sid=40120
        # max=None,
        # rt=None,
        key=CTA_ARRIVALS['key'],
    ))
    
    # Parse XML response
    tree = ET.parse(StringIO(resp.text))
    root = tree.getroot()
    arrt = root.find('./eta/arrT')
    stcode = root.find('./errCd')
    if int(stcode.text) > 0:
        # TODO
        assert 0, resp.text

    # 20220402 23:20:25
    arr_dt = datetime.strptime(arrt.text, "%Y%m%d %H:%M:%S")
    stopdur = (arr_dt - datetime.now()).seconds
    print(f"{stopdur=}")

if __name__ == '__main__':
    main()