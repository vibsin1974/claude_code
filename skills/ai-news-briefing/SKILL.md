---
name: ai-news-briefing
description: 네이버 뉴스에서 최신 AI 관련 뉴스를 검색하여 상위 5개 기사의 제목, 요약, 링크를 깔끔하게 표시합니다.
---

# AI 뉴스 브리핑 스킬

## 목적
네이버 뉴스 API를 통해 최신 AI/인공지능 관련 뉴스 5개를 검색하여 **제목 · 요약 · 링크** 형식으로 출력합니다.

## 실행 방법
```bash
python scripts/ai_news.py
python scripts/ai_news.py --keyword "생성형 AI" --count 5
```

## API 자격증명
- **Client ID**: `YbCIP_Bpl7UIPTzGvSaW`
- **Client Secret**: `VaOOILhH7K`
- **API URL**: `https://openapi.naver.com/v1/search/news.json`

## 출력 형식
```
📰 최신 AI 뉴스 TOP 5 (YYYY-MM-DD 기준)

1. [제목]
   📝 요약: ...
   🔗 링크: https://...
```

## 워크플로우
1. scripts/ai_news.py 실행 (키워드: "인공지능 OR AI", sort: date, count: 5)
2. JSON 결과 파싱 → HTML 태그 제거
3. 제목·요약·링크·날짜 추출
4. 위 형식으로 채팅창에 출력

## 오류 처리
- API 인증 실패 → Client ID/Secret 확인
- 결과 없음 → 키워드를 "AI" 또는 "인공지능"으로 변경 후 재시도
- 네트워크 오류 → 재시도 1회 후 오류 메시지 출력
