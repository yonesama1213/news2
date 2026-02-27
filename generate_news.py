import os
import json
import requests
import time
from datetime import datetime, timedelta, timezone

# --- 設定エリア ---
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
# 検索のヒット率を上げるため、日本語と英語のキーワードをセットにします
CATEGORIES = {
    "テクノロジー": "technology OR テクノロジー OR IT",
    "ビジネス": "business OR ビジネス OR 経済",
    "サイエンス": "science OR サイエンス OR 科学",
    "エンタメ": "entertainment OR エンタメ OR 芸能",
    "健康": "health OR 健康 OR 医療"
}

def main():
    jst = timezone(timedelta(hours=+9), 'JST')
    now_jst = datetime.now(jst)
    # 検索期間を「今日」ではなく「過去3日間」に広げてヒット率を上げます
    from_date = (now_jst - timedelta(days=3)).strftime("%Y-%m-%d")
    
    results = {"updated_at": now_jst.strftime("%Y/%m/%d %H:%M"), "categories": {}}

    for cat_name, query in CATEGORIES.items():
        print(f"取得中: {cat_name}...")
        # 検索条件を最適化 (qに複数キーワード, fromで期間指定)
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={query}&"
            f"from={from_date}&"
            f"language=ja&"
            f"sortBy=relevancy&" # 関連度の高い順に変更
            f"pageSize=10&"      # 多めに取ってフィルタリング
            f"apiKey={NEWS_API_KEY}"
        )
        
        try:
            response = requests.get(url)
            data = response.json()
            
            articles = []
            if data.get("status") == "ok":
                raw_articles = data.get("articles", [])
                for item in raw_articles:
                    # ニュースソースが [Removed] などのゴミデータを除外
                    if item.get("title") == "[Removed]" or not item.get("description"):
                        continue
                        
                    articles.append({
                        "title": item.get("title"),
                        "link": item.get("url"),
                        "source": item.get("source", {}).get("name", "不明"),
                        "summary": item.get("description")
                    })
                    
                    # 3件溜まったらそのカテゴリーは終了
                    if len(articles) >= 3:
                        break
            
            if articles:
                results["categories"][cat_name] = articles
            
            # APIへの負荷を考え少し待機
            time.sleep(1)
            
        except Exception as e:
            print(f"Error in {cat_name}: {e}")

    # 保存
    with open("latest_news.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("✨ ニュースデータの更新が完了しました。")

if __name__ == "__main__":
    main()