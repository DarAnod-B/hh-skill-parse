from enum import Enum
from fake_useragent import UserAgent
import requests
from selectolax.lexbor import LexborHTMLParser


LINK_TEMPLATE = r"https://hh.ru/vacancies/{vacancies_name}?page={page_num}&items_on_page=100"
PAGE_NOT_FOUND = 404

ua = UserAgent()


class CSSpath(Enum):
    ListOfVacancies = "#a11y-main-content"
    LinkToVacancies = "a.serp-item__title"


def get_html(url: str) -> str:
    with requests.Session() as session:
        headers = {'User-Agent': ua.chrome}

        result = session.get(url, headers=headers)

        html = result.text
        status_code = result.status_code
        return html, status_code


def parse_links_to_vacancies(html: str) -> list:
    tree = LexborHTMLParser(html)
    tree_url = tree.css(CSSpath.ListOfVacancies.value)
    links_from_page = []
    if tree_url is not None:
        for a in tree_url[0].css(CSSpath.LinkToVacancies.value):
            link = a.attrs['href']
            link_vacancy_id = link[22:].split("?")[0]
            links_from_page.append(link_vacancy_id)
        return links_from_page


def get_all_links_to_vacancies(vacancies_name: str) -> list:
    links_from_all_page = []
    page_num = 0
    vacancies_name = vacancies_name.replace(' ', '-')

    while True:
        page_num += 1

        LINK = LINK_TEMPLATE.format(
            vacancies_name=vacancies_name,
            page_num=page_num)
        html, status_code = get_html(LINK) 

        if status_code == PAGE_NOT_FOUND: break

        links_from_page = parse_links_to_vacancies(html)
        links_from_all_page.extend(links_from_page)

        

    return links_from_all_page
