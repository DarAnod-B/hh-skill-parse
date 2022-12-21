from parse_hh_data import download


def creating_a_list_of_required_skills(vacancy_id: int) -> list:
    vacancy = download.vacancy(vacancy_id)
    return [skill["name"] for skill in vacancy["key_skills"]]
