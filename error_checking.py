from selenium.webdriver.common.by import By


def decorator_exception(func):
    """
    Декоратор для отловки ошибок при поиске на странице товара
    :param func:
    :return:
    """
    def wrapper(data_from_selenium):
        try:
            text = func(data_from_selenium)
            return text
        except Exception:
            return f'None'

    return wrapper


@decorator_exception
def search_and_check_path_bread_crumbs(data_from_selenium):
    """
    Поиска пути товара
    :param data_from_selenium:
    :return:
    """
    path_bread_crumbs = data_from_selenium.find_element(By.XPATH, '//ul[@class="pdp-breadcrumbs__list"]').text.replace(
        '\n', '/')
    return path_bread_crumbs


@decorator_exception
def search_and_check_vendor_code(data_from_selenium) -> str:
    """
    Поиска  артикула
    :param data_from_selenium:
    :return:
    """
    vendor_code = data_from_selenium.find_element(By.XPATH, '//span[@itemprop="sku"]').text
    return vendor_code


@decorator_exception
def search_and_check_price(data_from_selenium) -> str:
    """
    Поиска цены
    :param data_from_selenium:
    :return:
    """
    price = data_from_selenium.find_element(By.XPATH, './/span[@class="special-price"]').get_attribute()
    return price


@decorator_exception
def search_and_check_discount(data_from_selenium) -> str:
    """Поиска скидок"""
    discount = data_from_selenium.find_element(By.XPATH,
                                               './/span[@class="price-container price-final_price tax weee"]'). \
        get_attribute('data-price-description')
    return discount


@decorator_exception
def search_and_check_description(data_from_selenium) -> str:
    """Поиска описания товара"""
    button = data_from_selenium.find_element(By.XPATH, './/button[@class="product-description__read-more"]')
    if button.is_displayed():
        button.click()
    description = data_from_selenium.find_element(By.XPATH,
                                                  './/section[@itemprop="description"]').text
    return description.replace('\n', ' ')


@decorator_exception
def search_and_check_link_image(data_from_selenium) -> str:
    """
    Поиска ссылки на картинку
    :param data_from_selenium:
    :return:
    """
    link_image = data_from_selenium.find_element(By.XPATH,
                                                 '//img[@data-role="fullscreen-gallery-opener"]').get_attribute('src')
    return link_image


@decorator_exception
def search_and_check_type_of_product(data_from_selenium) -> str:
    """
    Поиска на тип единицу измерения
    :param data_from_selenium:
    :return:
    """
    for data_unit in data_from_selenium.find_elements(By.XPATH, '//p[@class="subheading-1 pdp-subheading"]'):
        if data_unit.is_displayed():
            unit_good = data_unit.text.lower()
            return unit_good


@decorator_exception
def search_and_check_title__of_product(data_from_selenium) -> str:
    """
    Поиска на название продукта(заголвок товара)
    :param data_from_selenium:
    :return:
    """
    for data_title in data_from_selenium.find_elements(By.XPATH, '//h1[@itemprop="name"]'):
        if data_title.is_displayed():
            title_good = data_title.text.lower()
            return title_good
