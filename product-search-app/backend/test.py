import requests
import json
# API base URL
BASE_URL = "http://localhost:8000"

# 測試 insert_product API
def test_insert():
    product_data = {
        "name": "Sony 無線藍牙耳機 降噪款 WH-1000XM4",
        "price": "5990",
        "link": "https://www.etmall.com.tw/product/123456"
    }

    response = requests.post(f"{BASE_URL}/api/insert_product", json=product_data)
    print("Insert Product Response:")
    print(response.json())

# 測試 search API
def test_search():
    search_data = {
        "keyword": "sony"
    }

    response = requests.post(f"{BASE_URL}/search", json=search_data)
    print("\nSearch Product Response:")
    print(response.json())

if __name__ == "__main__":
    test_insert()
    test_search()
