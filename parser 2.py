import csv
import time
from typing import Union
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from error_checking import search_and_check_description, search_and_check_discount, search_and_check_link_image, \
    search_and_check_path_bread_crumbs, search_and_check_price, search_and_check_title__of_product, \
    search_and_check_type_of_product, search_and_check_vendor_code
import datetime
FILE_NAME = "goods.csv"


def start_selenium_session():
    options = selenium.webdriver.chrome.options.Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--headless')
    return selenium.webdriver.Chrome('chromedriver.exe', options=options)


def getting_product_data_from_page(data_from_selenium, link: str, volume: Union[str, None]) -> dict:
    """
    Запонение словаря данными о товаре со страницы
    :param data_from_selenium:
    :param link:
    :param volume:
    :return:
    """
    dict_info_good = {
        search_and_check_vendor_code(data_from_selenium):
            {
                "path_bread_crumbs": search_and_check_path_bread_crumbs(data_from_selenium=data_from_selenium),
                "unit": search_and_check_type_of_product(data_from_selenium=data_from_selenium),
                "title": search_and_check_title__of_product(data_from_selenium=data_from_selenium),
                "price": search_and_check_price(data_from_selenium=data_from_selenium),
                "discount": search_and_check_discount(data_from_selenium=data_from_selenium),
                'link_image': search_and_check_link_image(data_from_selenium=data_from_selenium),
                'product_description': search_and_check_description(data_from_selenium=data_from_selenium),
                'volume': volume,
                'link': link,
                'art': search_and_check_vendor_code(data_from_selenium=data_from_selenium)
            }
    }
    return dict_info_good


def getting_text_data_good(url: str) -> dict:
    """
    Возвращает данные со страницы включает в себя проверку на наличие кнопки переключения объемов продукции
    если есть 2 и более кнопки вернет словарь с ключами по артикулу и значением словарь с данными
    :param url:
    :return:
    """
    driver = start_selenium_session()
    driver.get(url)
    page_info = {}
    #  Проверка на наличие кнопки выбора объема торава
    swatches = driver.find_element(By.XPATH, '//div[@class="pdp-form__swatches pdp-form-swatches"]')
    button = swatches.find_elements(By.XPATH, '//button[@tabindex="-1"]')
    if len(button) > 0:
        button = [element for element in button if element.is_displayed()]
        for i in button:
            i.click()
            page_info.update(getting_product_data_from_page(data_from_selenium=driver, link=url, volume=i.text))
    else:
        button = None
        page_info = getting_product_data_from_page(data_from_selenium=driver, link=url, volume=button)
    driver.close()
    return page_info


def getting_links_brands_with_products(url):
    """
    Получение ссылок на бренды
    :param url:
    :return:
    """
    driver = start_selenium_session()
    driver.get(url)
    time.sleep(1)
    list_element_links_brands = [element.get_attribute('href') for element in
                                 driver.find_elements(By.XPATH, '//a[@class="item"]')]
    driver.close()
    return list_element_links_brands


def getting_links_to_brand_products(url):
    """
    Получение ссылок на довары в брэнде
    :param url:
    :return:
    """
    driver = start_selenium_session()
    driver.get(url)
    time.sleep(1)
    list_links_to_brand_products = [element.get_attribute('href') for element in
                                    driver.find_elements(By.XPATH, '//a[@class="product-item-link"]')]
    driver.close()
    return list_links_to_brand_products


def site_parsing_goldapple():
    brands_links_list = getting_links_brands_with_products('https://goldapple.ru/brands/')
    for brand in brands_links_list:
        list_links_to_brand_products = getting_links_to_brand_products(brand)
        for product in list_links_to_brand_products:
            print(f'записываю продукт продукт--,{product},время -- {datetime.datetime.now()}')
            data = getting_text_data_good(product)
            with open(FILE_NAME, "a", encoding='utf-8', ) as file:
                for item in data.values():
                    writer = csv.DictWriter(file, item.keys(), delimiter='\t')
                    writer.writerow(item)
            print(f'записал!!! время -- {datetime.datetime.now()}')


site_parsing_goldapple()
