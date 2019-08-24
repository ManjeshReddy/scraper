import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}


def get_total_pages(catagory_url):
    response = requests.get(catagory_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('li', class_='a-disabled')
    total_pages = links[1]
    return int(total_pages.get_text())


def get_total_items_in_page(page_url):
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    all_links = soup.find_all('a', {'class': 'a-link-normal a-text-normal'}, {'target': '_blank'})
    return int(len(all_links))


def get_all_url_list(page_url):
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all('a', {'class': 'a-link-normal a-text-normal'}, {'target': '_blank'})
    return links


def get_price_of_item(item_url):
    response = requests.get(item_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    if soup.find(id="priceblock_ourprice") is None:
        if soup.find(id="priceblock_saleprice") is None:
            return "₹ 0"
        else:
            return soup.find(id="priceblock_saleprice").get_text()
    else:
        return soup.find(id="priceblock_ourprice").get_text()



catagory_url1 = "https://www.amazon.in/s?i=amazon-devices&page={0}"
catagory_url = "https://www.amazon.in/s?k=bike+parts&i=automotive&rh=n%3A5257472031&page={0}"
total_pages = get_total_pages(catagory_url)
counter = 0
for page in range(1, total_pages + 1):
    page_url = catagory_url.format(page)
    url_list = get_all_url_list(page_url)
    for link in url_list:
        url = "https://www.amazon.in{0}".format(link.get('href'))
        print(url)
        page = requests.get(url, headers=headers)
        if page.status_code == 404:
            continue
        price = get_price_of_item(url)
        print(price)
        counter += 1

print("Total items = ", counter)