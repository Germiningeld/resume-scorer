import requests
from bs4 import BeautifulSoup
import urllib3
import re # Для более эффективной замены пробелов

# Отключаем предупреждения о небезопасном SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_html(url: str) -> str:
    """
    Получает HTML страницы с использованием requests
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Ошибка при получении страницы: {str(e)}")
        return ""

def remove_extra_spaces(text: str) -> str:
    """
    Заменяет табы и неразрывные пробелы на обычные пробелы,
    затем заменяет последовательности пробелов на одинарные,
    и удаляет пробелы по краям строки.
    """
    if not text:
        return ""
    text = text.replace('\t', ' ')     # Замена табов на пробелы
    text = text.replace('\xa0', ' ')   # Замена неразрывных пробелов
    # Заменяем одну или более последовательностей пробелов (которые теперь включают бывшие табы и неразрывные пробелы)
    # на один обычный пробел.
    text = re.sub(r' +', ' ', text)
    return text.strip()                # Финальная очистка пробелов по краям

def extract_vacancy_data(html: str) -> str:
    """
    Извлекает данные о вакансии с hh.ru
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Название вакансии
    title_tag = soup.find('h1', {'data-qa': 'vacancy-title'})
    title = remove_extra_spaces(title_tag.text) if title_tag else 'Название не найдено'
    
    # Название компании
    company_tag = soup.find('a', {'data-qa': 'vacancy-company-name'})
    if not company_tag:
        company_tag = soup.find('span', {'data-qa': 'vacancy-company-name'})
    company = remove_extra_spaces(company_tag.text) if company_tag else 'Компания не указана'

    # Детали работы
    experience_tag = soup.find('span', {'data-qa': 'vacancy-experience'})
    experience = remove_extra_spaces(experience_tag.text) if experience_tag else 'Опыт работы не указан'
    
    # Занятость - ищем по data-qa и классу text
    employment = ''
    employment_block = soup.find('div', {'data-qa': 'common-employment-text'})
    if employment_block:
        employment_span = employment_block.find('span', {'class': 'text--xmNTy6IsSzcA0FG8'})
        if employment_span:
            employment = remove_extra_spaces(employment_span.text)
    
    schedule_tag = soup.find('p', {'data-qa': 'work-schedule-by-days-text'})
    schedule = remove_extra_spaces(schedule_tag.text.replace('График:', '')) if schedule_tag else ''
    
    work_hours_tag = soup.find('div', {'data-qa': 'working-hours-text'})
    work_hours = remove_extra_spaces(work_hours_tag.text.replace('Рабочие часы:', '')) if work_hours_tag else ''
    
    work_format_tag = soup.find('p', {'data-qa': 'work-formats-text'})
    work_format = remove_extra_spaces(work_format_tag.text.replace('Формат работы:', '')) if work_format_tag else ''

    # Описание вакансии
    description_tag = soup.find('div', {'data-qa': 'vacancy-description'})
    description = remove_extra_spaces(description_tag.text) if description_tag else 'Описание не найдено'
    
    # Ключевые навыки - ищем по data-qa="skills-element"
    skills = []
    skills_elements = soup.find_all('li', {'data-qa': 'skills-element'})
    for element in skills_elements:
        skill_div = element.find('div', {'class': 'magritte-tag__label___YHV-o_3-1-20'})
        if skill_div:
            skills.append(remove_extra_spaces(skill_div.text))
    skills_str = '\n'.join(f"- {skill}" for skill in skills) if skills else 'Не указаны'

    return f"""# {title}

**Компания:** {company}

**Условия работы:**
- Опыт работы: {experience}
- Занятость: {employment}
- График работы: {schedule}
- Рабочие часы: {work_hours}
- Формат работы: {work_format}

**Описание вакансии:**
{description}

**Ключевые навыки:**
{skills_str}
"""

def extract_candidate_data(html: str) -> str:
    """
    Извлекает данные резюме с hh.ru
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Личная информация
    personal_info = []
    gender = soup.find('span', {'data-qa': 'resume-personal-gender'})
    if gender:
        personal_info.append(remove_extra_spaces(gender.text))
    
    age = soup.find('span', {'data-qa': 'resume-personal-age'})
    if age:
        personal_info.append(remove_extra_spaces(age.text))
    
    birthday = soup.find('span', {'data-qa': 'resume-personal-birthday'})
    if birthday:
        personal_info.append(f"родился {remove_extra_spaces(birthday.text)}")
    
    address_block = soup.find('span', {'data-qa': 'resume-personal-address'})
    if address_block:
        parent_p = address_block.find_parent('p')
        if parent_p:
            full_address_info = remove_extra_spaces(parent_p.text)
            personal_info.append(full_address_info)
        else: 
            personal_info.append(remove_extra_spaces(address_block.text))

    position = soup.find('span', {'data-qa': 'resume-block-title-position'})
    position = remove_extra_spaces(position.text) if position else 'Должность не указана'
    
    salary = soup.find('span', {'data-qa': 'resume-block-salary'})
    salary = remove_extra_spaces(salary.text) if salary else 'Зарплата не указана'
    
    total_experience_header = soup.find('h2', {'data-qa': 'bloko-header-2'}, class_='bloko-header-2_lite')
    total_experience_text = ''
    if total_experience_header:
        title_span = total_experience_header.find('span', class_='resume-block__title-text')
        if title_span:
            total_experience_text = remove_extra_spaces(title_span.text)

    experience_entries = []
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
      
    if experience_section:
        job_elements = experience_section.select('div.resume-block-item-gap > div.bloko-columns-row > div.resume-block-item-gap')
        
        if not job_elements:
            direct_gaps = experience_section.find_all('div', class_='resume-block-item-gap', recursive=False)
            if direct_gaps:
                job_elements = direct_gaps
            else:
                wrapper = experience_section.find('div', recursive=False)
                if wrapper:
                    job_elements = wrapper.find_all('div', class_='resume-block-item-gap', recursive=False)
        
        job_elements = list(dict.fromkeys(job_elements))
 
        for job_item_container in job_elements: 
            date_text = 'Дата не указана'
            date_div = job_item_container.select_one('div.bloko-column.bloko-column_xs-4.bloko-column_s-2.bloko-column_m-2.bloko-column_l-2')
 
            if date_div:
                date_parts = []
                for content_node in date_div.contents:
                    if isinstance(content_node, str):
                        part = remove_extra_spaces(content_node)
                        if part:
                            date_parts.append(part)
                    elif content_node.name == 'div' and 'bloko-text_tertiary' in content_node.get('class', []):
                        tertiary_text = remove_extra_spaces(content_node.text)
                        if tertiary_text:
                            date_parts.append(f" {tertiary_text}")
                current_date_text = ''.join(date_parts)
                if current_date_text:
                    date_text = remove_extra_spaces(current_date_text)
  
            company_name = ''
            job_title = ''
            description_details_text = ''
 
            details_container_column = job_item_container.find('div', class_=lambda x: x and 'bloko-column_l-10' in x and 'bloko-column_m-7' in x)
            
            if details_container_column:
                content_root = details_container_column.find('div', class_='resume-block-container', recursive=False)
                if not content_root:
                    content_root = details_container_column

                position_div = content_root.find('div', {'data-qa': 'resume-block-experience-position'})
                if position_div:
                    job_title = remove_extra_spaces(position_div.get_text(strip=True))

                all_strong_elements = content_root.find_all('div', class_='bloko-text bloko-text_strong', recursive=False)
                
                for strong_element in all_strong_elements:
                    if strong_element == position_div:
                        continue
                    
                    link_tag = strong_element.find('a', class_='bloko-link', recursive=False)
                    if link_tag:
                        company_name = remove_extra_spaces(link_tag.get_text(strip=True))
                    else:
                        company_name = remove_extra_spaces(strong_element.get_text(strip=True))
                    break 

                description_div = content_root.find('div', {'data-qa': 'resume-block-experience-description'})
                if description_div:
                    # Используем strip=True в get_text для предварительной очистки строк
                    raw_lines = description_div.get_text(separator='\n', strip=True).split('\n')

                    cleaned_lines = [remove_extra_spaces(line) for line in raw_lines]
                    description_details_text = '\n'.join(filter(None, cleaned_lines)) # Удаляем пустые строки, возникшие после очистки
            
            current_experience_parts = []
            if date_text != 'Дата не указана':
                current_experience_parts.append(date_text)
            if company_name:
                current_experience_parts.append(company_name)
            if job_title:
                current_experience_parts.append(job_title)
            
            if description_details_text:
                if current_experience_parts: 
                    current_experience_parts.append("\n" + description_details_text)
                else: 
                    current_experience_parts.append(description_details_text)
            
            if current_experience_parts: 
                experience_entries.append("\n".join(current_experience_parts))
              
    experience_output = '\n\n'.join(experience_entries)

    about_div = soup.find('div', {'data-qa': 'resume-block-skills-content'})
    about_text = ''
    if about_div:
        # Используем strip=True в get_text для предварительной очистки строк
        raw_about_lines = about_div.get_text(separator='\n', strip=True).split('\n')
        
        cleaned_about_lines = [remove_extra_spaces(line) for line in raw_about_lines]
        about_text = '\n'.join(filter(None, cleaned_about_lines))
    
    education = []
    education_main_section = soup.find('div', {'data-qa': 'resume-block-education'})
    if education_main_section:
        education_data_items = education_main_section.find_all('div', {'data-qa': 'resume-block-education-item'})
        
        for edu_data_item_container in education_data_items: 
            name_div = edu_data_item_container.find('div', {'data-qa': 'resume-block-education-name'})
            organization_div = edu_data_item_container.find('div', {'data-qa': 'resume-block-education-organization'})
            
            name_text = remove_extra_spaces(name_div.get_text(strip=True)) if name_div else ''
            organization_text = remove_extra_spaces(organization_div.get_text(strip=True)) if organization_div else ''
            
            year_text = ''
            details_column = edu_data_item_container.parent 
            if details_column and details_column.name == 'div' and \
               'bloko-column_l-10' in details_column.get('class', []): 
                
                row_that_holds_year_and_details = details_column.parent
                if row_that_holds_year_and_details and row_that_holds_year_and_details.name == 'div' and \
                   'bloko-columns-row' in row_that_holds_year_and_details.get('class', []):
                    
                    year_column = row_that_holds_year_and_details.find('div', 
                        class_=lambda x: x and all(c in x for c in ['bloko-column', 'bloko-column_xs-4', 'bloko-column_s-2', 'bloko-column_m-2', 'bloko-column_l-2']), 
                        recursive=False)
                    if year_column:
                        year_text = remove_extra_spaces(year_column.get_text(strip=True))
            
            entry_parts = []
            if year_text: entry_parts.append(f"**{year_text}**")
            if name_text: entry_parts.append(name_text)
            if organization_text: entry_parts.append(organization_text)

            if entry_parts:
                if len(entry_parts) > 1 and year_text: # Year and name/org
                    education.append(f"{entry_parts[0]} - {' '.join(entry_parts[1:])}")
                elif len(entry_parts) > 1 and name_text and organization_text : # name and org, no year
                     education.append(f"**{name_text}**\n{organization_text}")
                else: # only one part or specific combo
                     education.append(' '.join(entry_parts))

    languages = []
    languages_section = soup.find('div', {'data-qa': 'resume-block-languages'})
    if languages_section:
        lang_items = languages_section.find_all('div', {'class': 'label--rww2ZivO9BoGXcua'})
        for lang in lang_items:
            if lang:
                languages.append(remove_extra_spaces(lang.text))
    
    citizenship_section = soup.find('div', {'data-qa': 'resume-block-additional'})
    citizenship_info = []
    if citizenship_section:
        item_gap_block = citizenship_section.find('div', class_='resume-block-item-gap')
        if item_gap_block:
            container_with_p_tags = item_gap_block.find('div', class_='resume-block-container')
            if container_with_p_tags:
                for p_tag in container_with_p_tags.find_all('p', recursive=False): 
                    text = remove_extra_spaces(p_tag.text)
                    if text: 
                        citizenship_info.append(text)

    # Собираем финальные строки, применяя очистку к каждой
    final_personal_info_str = remove_extra_spaces(', '.join(filter(None, personal_info)))
    final_education_str = '\n'.join(filter(None, [remove_extra_spaces(e) for e in education]))
    final_languages_str = '\n'.join(filter(None, [f"- {remove_extra_spaces(lang)}" for lang in languages]))
    final_citizenship_str = '\n'.join(filter(None, [f"- {remove_extra_spaces(info)}" for info in citizenship_info]))

    # Итоговая сборка резюме.
    # total_experience_text, experience_output, about_text уже должны быть очищены на этапе формирования.
    # position и salary также очищаются при извлечении.
    return f"""# Резюме

**Личная информация:**
{final_personal_info_str}

**Желаемая должность:** {position}
**Ожидания по зарплате:** {salary}

## {total_experience_text}
{experience_output}

**Обо мне:**
{about_text}

**Образование:**
{final_education_str}

**Знание языков:**
{final_languages_str}

**Гражданство и разрешение на работу:**
{final_citizenship_str}
"""

def get_candidate_info(url: str) -> str:
    html = get_html(url)
    return extract_candidate_data(html)

def get_job_description(url: str) -> str:
    html = get_html(url)
    return extract_vacancy_data(html)

if __name__ == "__main__":
    test_candidate_url = "https://hh.ru/resume/f694325c00072745540039ed1f6b6d35787556?query=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+laravel&searchRid=1748937992763309c61ac19a31478b0d&hhtmFrom=resume_search_result"
    # test_vacancy_url = "https://hh.ru/vacancy/121183802?hhtmFromLabel=similar_vacancies_sidebar&hhtmFrom=vacancy"
    try:
        print(f"Fetching candidate info from: {test_candidate_url}")
        candidate_info = get_candidate_info(test_candidate_url)
        if candidate_info:
            print("--- Candidate Info Start ---")
            print(candidate_info)
            print("--- Candidate Info End ---")
        else:
            print("!!! ERROR: No candidate information was extracted or the result was empty. !!!")
        
        # print(f"Fetching job description from: {test_vacancy_url}")
        # job_description = get_job_description(test_vacancy_url)
        # if job_description:
        # print("--- Job Description Start ---")
        # print(job_description)
        # print("--- Job Description End ---")
        # else:
        # print("!!! ERROR: No job description was extracted or the result was empty. !!!")

    except Exception as e:
        print(f"!!! TOP LEVEL ERROR DURING SCRIPT EXECUTION: {str(e)} !!!")
        import traceback
        traceback.print_exc()