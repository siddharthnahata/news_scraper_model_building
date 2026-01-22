def generic_news_wrapper(
    seen_url: set,
    fetch_listing_func,
    fetch_detail_func
):
    articles = fetch_listing_func()
    final_data = []

    for article in articles:
        url = article["url"]

        if url in seen_url:
            continue

        pub_time, pub_content = fetch_detail_func(url)

        if pub_time is None or pub_content is None:
            continue

        final_data.append({
            "title": article["title"],
            "content": pub_content,
            "pub_time": pub_time,
            "url": url
        })

    return final_data
