import os
import json
import requests
from datetime import datetime, timedelta, timezone

# --- 設定エリア ---
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
# 日本のTop Headlinesで使える正確なカテゴリー名に合わせます [cite: 2026-02-27]
CATEGORIES = {
    "テクノロジー": "technology",
    "ビジネス": "business",
    "サイエンス": "science",
    "エンタメ": "entertainment",
    "健康": "health"
}

def main():
    jst = timezone(timedelta(hours=+9), 'JST')
    now_jst = datetime.now(jst)
    results = {"updated_at": now_jst.strftime("%Y/%m/%d %H:%M"), "categories": {}}

    for display_name, api_cat in CATEGORIES.items():
        print(f"取得中: {display_name}...")
        # 注目：'everything' ではなく 'top-headlines' を使用し、国を 'jp' に指定します [cite: 2026-02-27]
        url = (
            f"https://newsapi.org/v2/top-headlines?"
            f"country=jp&"
            f"category={api_cat}&"
            f"pageSize=5&"
            f"apiKey={NEWS_API_KEY}"
        )
        
        try:
            response = requests.get(url)
            data = response.json()
            
            articles = []
            if data.get("status") == "ok":
                for item in data.get("articles", []):
                    # 削除済み記事や説明文がないものをスキップ
                    if item.get("title") == "[Removed]" or not item.get("url"):
                        continue
                    
                    articles.append({
                        "title": item.get("title"),
                        "link": item.get("url"),
                        "source": item.get("source", {}).get("name", "不明"),
                        "summary": item.get("description") or "（詳細説明はありません。リンク先をご確認ください）"
                    })
            
            if articles:
                results["categories"][display_name] = articles
            
        except Exception as e:
            print(f"Error in {display_name}: {e}")

    # ファイル保存
    with open("latest_news.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("✨ ニュースデータの更新が完了しました。")

if __name__ == "__main__":
    main()