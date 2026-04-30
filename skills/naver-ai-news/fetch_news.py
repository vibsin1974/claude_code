import urllib.request, urllib.parse, json, os, sys

def fetch_ai_news(query='인공지능 AI', count=5):
    client_id     = os.environ.get('NAVER_CLIENT_ID')
    client_secret = os.environ.get('NAVER_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise EnvironmentError("환경변수 NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET이 설정되지 않았습니다.")
    
    encoded = urllib.parse.quote(query)
    url = f'https://openapi.naver.com/v1/search/news.json?query={encoded}&display={count}&sort=date'
    
    req = urllib.request.Request(url, headers={
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    })
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read().decode('utf-8'))
    
    results = []
    for item in data.get('items', []):
        import re, html
        title = html.unescape(re.sub(r'<[^>]+>', '', item.get('title', '')))
        desc  = html.unescape(re.sub(r'<[^>]+>', '', item.get('description', '')))
        link  = item.get('originallink') or item.get('link', '')
        date  = item.get('pubDate', '')[:16]
        results.append({'title': title, 'summary': desc, 'link': link, 'date': date})
    
    return results

if __name__ == '__main__':
    query = sys.argv[1] if len(sys.argv) > 1 else '인공지능 AI'
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    news = fetch_ai_news(query, count)
    print(f'📰 최신 AI 뉴스 [{query}]\n')
    for i, n in enumerate(news, 1):
        print(f'{i}. {n["title"]}')
        print(f'   📍 {n["date"]}')
        print(f'   💬 {n["summary"]}')
        print(f'   🔗 {n["link"]}')
        print()
