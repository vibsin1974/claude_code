#!/usr/bin/env python3
"""
AI 뉴스 브리핑 - 네이버 뉴스 API를 통해 최신 AI 뉴스 5개를 검색합니다.
"""

import urllib.request
import urllib.parse
import json
import re
import argparse
from datetime import datetime

CLIENT_ID = "YbCIP_Bpl7UIPTzGvSaW"
CLIENT_SECRET = "VaOOILhH7K"
API_URL = "https://openapi.naver.com/v1/search/news.json"


def clean_html(text):
    """HTML 태그 및 특수문자 제거"""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&#039;', "'").replace('&apos;', "'")
    return text.strip()


def format_date(pub_date_str):
    """날짜 포맷 변환 (RFC 2822 → YYYY-MM-DD)"""
    try:
        dt = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S +0900")
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return pub_date_str


def search_news(keyword="인공지능", count=5, sort="date"):
    """네이버 뉴스 API 검색"""
    params = urllib.parse.urlencode({
        "query": keyword,
        "display": count,
        "start": 1,
        "sort": sort
    })
    url = f"{API_URL}?{params}"

    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", CLIENT_SECRET)

    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data.get("items", [])


def print_news(articles, keyword):
    """뉴스 결과 출력"""
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n📰 최신 AI 뉴스 TOP {len(articles)}  ({today} 기준 · 키워드: {keyword})")
    print("=" * 60)

    for i, item in enumerate(articles, 1):
        title = clean_html(item.get("title", "제목 없음"))
        desc = clean_html(item.get("description", "요약 없음"))
        link = item.get("originallink") or item.get("link", "")
        pub_date = format_date(item.get("pubDate", ""))

        print(f"\n{i}. {title}")
        print(f"   📅 {pub_date}")
        print(f"   📝 {desc[:120]}{'...' if len(desc) > 120 else ''}")
        print(f"   🔗 {link}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="네이버 뉴스 AI 브리핑")
    parser.add_argument("--keyword", default="인공지능", help="검색 키워드 (기본: 인공지능)")
    parser.add_argument("--count", type=int, default=5, help="검색 결과 수 (기본: 5)")
    parser.add_argument("--sort", default="date", choices=["date", "sim"], help="정렬 기준")
    args = parser.parse_args()

    try:
        articles = search_news(keyword=args.keyword, count=args.count, sort=args.sort)
        if not articles:
            print(f"[결과 없음] '{args.keyword}' 키워드로 검색된 뉴스가 없습니다.")
            return
        print_news(articles, args.keyword)
    except urllib.error.HTTPError as e:
        print(f"[API 오류] HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"[네트워크 오류] {e.reason}")
    except Exception as e:
        print(f"[오류] {e}")


if __name__ == "__main__":
    main()
