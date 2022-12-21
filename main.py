from collections import Counter
from googletrans import Translator

from vacancy_link import get_all_links_to_vacancies
from skills_parse import creating_a_list_of_required_skills


def main() -> None:
    skill_list = []

    translator = Translator()

    links_to_vacancy_id = get_all_links_to_vacancies("data scientist")

    for link in links_to_vacancy_id:
        skill_list.extend(creating_a_list_of_required_skills(link))
    skill_list_ru = [trans.text.lower() for trans in translator.translate(
        skill_list, src='ru', dest='en')]
    skill_list_count = Counter(skill_list_ru)
    skill_list_count_sort = {skill: count for skill,
                             count in skill_list_count.items() if count > 5}
    skill_list_sort = dict(
        sorted(skill_list_count_sort.items(), key=lambda item: item[1], reverse=True))

    print(skill_list_sort)


if __name__ == "__main__":
    main()
