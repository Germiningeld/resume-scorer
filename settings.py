# OpenAI settings
MODEL_NAME = "gpt-4o-mini"
MAX_TOKENS = 1500
TEMPERATURE = 0

# Prompts
SYSTEM_PROMPT = """
Ты — опытный HR-специалист, задача которого — провести первичный скоринг резюме кандидата относительно предложенной вакансии. Твоя цель — помочь нанимающему менеджеру быстро принять решение.

Проанализируй предоставленные текст вакансии и текст резюме.

**Структура твоего ответа должна быть следующей:**

1.  **Общая оценка соответствия (от 1 до 10):** Краткое числовое выражение, насколько кандидат подходит.
2.  **Резюме анализа (2-3 предложения):** Ключевые выводы по соответствию кандидата вакансии. Укажи, стоит ли обратить внимание на этого кандидата.
3.  **Качество резюме:** Оцени, насколько полно и понятно кандидат описывает свой опыт и достижения. Это важный фактор.
4.  **Подходящие пункты:** Перечисли конкретные навыки, опыт или качества из резюме, которые хорошо соответствуют требованиям вакансии. Приводи примеры.
5.  **Неподходящие пункты / Области для уточнения:** Укажи, каких навыков или опыта не хватает, или какие моменты в резюме вызывают вопросы и требуют уточнения на собеседовании.

Будь объективен и основывай свои выводы только на предоставленной информации.
""".strip()

# Environment variables
ENV_VARS = {
    "OPENAI_API_KEY": "OPENAI_API_KEY"
}

# UI Messages
MESSAGES = {
    "TITLE": "Прескоринг резюме",
    "API_KEY_INPUT": "Введите ваш OpenAI API ключ",
    "API_KEY_MISSING": "API ключ не найден в .env файле. Пожалуйста, добавьте его в .env файл или введите здесь.",
    "ENV_SETUP_HELP": "Создайте файл .env в корне проекта и добавьте строку: OPENAI_API_KEY=your-api-key-here",
    "INIT_ERROR": "Ошибка при инициализации OpenAI клиента: {error}",
    "URL_MISSING": "Пожалуйста, введите URL вакансии и резюме.",
    "PROCESSING": "Оцениваем резюме...",
    "JOB_DESCRIPTION_TITLE": "### Описание вакансии:",
    "CV_TITLE": "### Резюме кандидата:",
    "ANALYSIS_TITLE": "### Результат анализа:",
    "PROCESSING_ERROR": "Произошла ошибка при обработке данных: {error}"
}

# Input fields
INPUTS = {
    "JOB_URL": "Введите URL вакансии",
    "CV_URL": "Введите URL резюме"
}

# Selectors for hh.ru parsing
VACANCY_SELECTORS = {
    "title": {'tag': 'h1', 'attrs': {'data-qa': 'vacancy-title'}},
    "company": {'tag': 'a', 'attrs': {'data-qa': 'vacancy-company-name'}},
    "company_fallback": {'tag': 'span', 'attrs': {'data-qa': 'vacancy-company-name'}},
    "experience": {'tag': 'span', 'attrs': {'data-qa': 'vacancy-experience'}},
    "employment_block": {'tag': 'div', 'attrs': {'data-qa': 'common-employment-text'}},
    "employment_span": {'tag': 'span', 'attrs': {'class': 'text--xmNTy6IsSzcA0FG8'}},
    "schedule": {'tag': 'p', 'attrs': {'data-qa': 'work-schedule-by-days-text'}},
    "work_hours": {'tag': 'div', 'attrs': {'data-qa': 'working-hours-text'}},
    "work_format": {'tag': 'p', 'attrs': {'data-qa': 'work-formats-text'}},
    "description": {'tag': 'div', 'attrs': {'data-qa': 'vacancy-description'}},
    "skills": {'tag': 'li', 'attrs': {'data-qa': 'skills-element'}},
    "skill_div": {'tag': 'div', 'attrs': {'class': 'magritte-tag__label___YHV-o_3-1-20'}},
}

RESUME_SELECTORS = {
    "gender": {'tag': 'span', 'attrs': {'data-qa': 'resume-personal-gender'}},
    "age": {'tag': 'span', 'attrs': {'data-qa': 'resume-personal-age'}},
    "birthday": {'tag': 'span', 'attrs': {'data-qa': 'resume-personal-birthday'}},
    "address_block": {'tag': 'span', 'attrs': {'data-qa': 'resume-personal-address'}},
    "position": {'tag': 'span', 'attrs': {'data-qa': 'resume-block-title-position'}},
    "salary": {'tag': 'span', 'attrs': {'data-qa': 'resume-block-salary'}},
    "total_experience_header": {'tag': 'h2', 'attrs': {'data-qa': 'bloko-header-2'}},
    "experience_section": {'tag': 'div', 'attrs': {'data-qa': 'resume-block-experience'}},
    "job_elements_selector": 'div.resume-block-item-gap > div.bloko-columns-row > div.resume-block-item-gap',
    "date_div_selector": 'div.bloko-column.bloko-column_xs-4.bloko-column_s-2.bloko-column_m-2.bloko-column_l-2',
    "details_container_selector": "div[class*='bloko-column_l-10'][class*='bloko-column_m-7']",
    "position_div": {'tag': 'div', 'attrs': {'data-qa': 'resume-block-experience-position'}},
    "description_div": {'tag': 'div', 'attrs': {'data-qa': 'resume-block-experience-description'}},
    "about_div": {'tag': 'div', 'attrs': {'data-qa': 'resume-block-skills-content'}},
    "key_skills_div": {'tag': 'div', 'attrs': {'data-qa': 'resume-block-skills'}},
    "key_skill_item": {'tag': 'div', 'attrs': {'data-qa': 'bloko-tag__text'}},
    "languages_header": {'tag': 'h2', 'attrs': {'data-qa': 'resume-block-languages-title'}},
    "language_item": {'tag': 'p', 'attrs': {'data-qa': 'resume-block-language-item'}},
    "education_section": {'tag': 'div', 'attrs': {'data-qa': 'resume-block-education'}},
    "education_item": {'tag': 'div', 'attrs': {'class': 'resume-block-item-gap'}},
    "edu_name": {'tag': 'div', 'attrs': {'data-qa': 'resume-block-education-name'}},
    "edu_organization": {'tag': 'div', 'attrs': {'data-qa': 'resume-block-education-organization'}},
    "citizenship_section": {'tag': 'div', 'attrs': {'data-qa': 'resume-block-additional'}},
} 