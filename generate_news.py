import os
import json
import requests
from datetime import datetime, timedelta, timezone

# --- 設定エリア ---
# ローカルテスト用（""の中にキーを入れれば手元でテストできます）
NEWS_API_KEY = os.environ.get("NEWS_API_KEY") or "8f420153afc4432383558764541310d4"
CATEGORIES = ["テクノロジー", "ビジネス", "サイエンス", "エンタメ", "健康"]

def main():
    jst = timezone(timedelta(hours=+9), 'JST')
    now_jst = datetime.now(jst)
    results = {"updated_at": now_jst.strftime("%Y/%m/%d %H:%M"), "categories": {}}

    for cat_name in CATEGORIES:
        print(f"取得中: {cat_name}...")
        # 日本語ニュースを新着順に5件取得 [cite: 2026-02-26]
        url = f"https://newsapi.org/v2/everything?q={cat_name}&language=ja&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            articles = []
            if data.get("status") == "ok":
                for item in data.get("articles", []):
                    # 説明文(description)をサマリーとして使用 [cite: 2026-02-26]
                    desc = item.get("description") or "※詳細な説明文はありません。"
                    articles.append({
                        "title": item.get("title"),
                        "link": item.get("url"),
                        "source": item.get("source", {}).get("name", "不明"),
                        "summary": desc 
                    })
            
            if articles:
                results["categories"][cat_name] = articles
            
        except Exception as e:
            print(f"Error in {cat_name}: {e}")

    with open("latest_news.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("✨ news2: ニュースデータの更新が完了しました。")

if __name__ == "__main__":
    main()