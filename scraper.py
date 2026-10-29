
def scrape_books(url):
    if not check_robots_permission(url):
        print("Scraping not permitted or permission unverified.")
        return

    headers = {"User-Agent": USER_AGENT}

    try:
        # One request for the page, with a timeout
        time.sleep(2)

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 429:
            print("Rate limit reached. Stopping.")
            return

        if response.status_code == 403:
            print("Access forbidden. Stopping.")
            return

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select("article.product_pod")

        with open("books.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Price", "Availability"])

            count = 0

            for book in books:
                title = book.h3.a.get("title", "").strip()
                price = book.select_one(".price_color")
                availability = book.select_one(".availability")

                if not title or price is None or availability is None:
                    continue

                writer.writerow([
                    title,
                    price.get_text(strip=True),
                    availability.get_text(strip=True)
                ])
                count += 1

        print(f"Saved {count} records to books.csv")

    except requests.RequestException as error:
        print("Request failed:", error)
