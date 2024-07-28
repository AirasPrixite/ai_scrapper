import json
import os
import csv
from scrapegraphai.graphs import SmartScraperGraph
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
graph_config = {
    "llm": {
        "api_key": openai_api_key,
        "model": "gpt-4o-mini",
    },
    "verbose": True,
    "headless": False,
}


def json_to_csv(json_data, csv_filename):
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        products = json_data.get("products", [])
        if len(products) > 0:
            headers = products[0].keys()
            csv_writer.writerow(headers)
            for item in products:
                csv_writer.writerow(item.values())


def main():
    url = input("Enter the URL of the page to scrape: ").strip()
    smart_scraper_graph = SmartScraperGraph(
        prompt="""This page contains a list of products. Per each product,
         scrape the following fields for each product: product code, full price, 
         price, currency, itemurl, imageurl, product category, product subcategory, product name. 
         The product code is a numeric string that can be found in the item url. 
         \Full price is the price of the product without discounts, if any.
           If there is no discount, use the only price shown. 
           Price is the product price after discounts: if there's no discount, use the only product price available.
             Currency is the ISO code of the currency used to display prices on this page. 
             Imageurl is the URL of the image of the product, used as a thumbnail on this page.""",
        source=url,
        config=graph_config,
    )
    result = smart_scraper_graph.run()
    json_structure = json.dumps(result, indent=4)
    json_data = json.loads(json_structure)
    csv_filename = "products_from_json.csv"
    json_to_csv(json_data, csv_filename)
    print(f"JSON data has been written to {csv_filename}")


if __name__ == "__main__":
    main()
