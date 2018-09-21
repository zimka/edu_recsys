import json

from django.test import TestCase

from apps.networking.recommender.compute.compute_prereq import build_df, _get_news, \
    _get_hobby, get_interests_similarity, _get_project_directions, _get_education, \
    _get_language, get_experience_similarity, _get_base, _get_main_competence, get_competence_similarity, \
    _get_environment

stub1 = json.loads(
    '{"WEFsurvey": [{"question": {"title": "Последний год вы:", "uuid": "d101147a-6e79-4336-aeb5-5fed41231b2d"}, "answers": ["работали по найму в бизнесе"]}, {"question": {"title": "В какую среду работы и общения вы были больше погружены последние 3 года (на месте работы или учебы)", "uuid": "4a74ea86-3944-4738-86e8-0388d8d03c84"}, "answers": ["академическая среда"]}, {"question": {"title": "Укажите три профессиональных компетенции, которые стали за последний год самыми значимыми в вашей деятельности. Как вы считаете, насколько меньше вы бы зарабатывали, если бы у вас их не было?", "uuid": "c7dfe386-67eb-4a52-9ee0-779ed0fa2004"}, "answers": [["Компетенция 1", "Программирование"], ["Компетенция 1 принесла приблизительно % годового дохода", "223"], ["Компетенция 2", "фыв"], ["Компетенция 2 принесла приблизительно % годового дохода", "123"], ["Компетенция 3", "фыва"], ["Компетенция 3 принесла приблизительно % годового дохода", "123"]]}, {"question": {"title": "Укажите количество ваших подписчиков в соцсети Facebook", "uuid": "a5075e74-9bec-40c2-9723-14b1160ffa3e"}, "answers": ["30000"]}, {"question": {"title": "Укажите количество ваших друзей в соцсети Facebook", "uuid": "afcab22d-171f-4aa6-8bae-2e80439ad634"}, "answers": ["123123"]}, {"question": {"title": "Укажите ссылку на ваш профиль в социальной сети, которой вы пользуетесь наиболее часто", "uuid": "d8c338c3-1c04-4928-9982-39034a5b8b87"}, "answers": [""]}, {"question": {"title": "В следующем году вы бы хотели", "uuid": "c258f973-eee1-4a7e-af83-84d6682b7105"}, "answers": ["продолжить работу на прежнем месте"]}, {"question": {"title": "В каком из этих направлений вы видите больше перспектив для своего развития (при равном уровне оплаты и прочих базовых условий)", "uuid": "44b7baab-50f3-49d4-8065-db8154e746a5"}, "answers": ["научная деятельность в области естественных или точных наук"]}, {"question": {"title": "Есть ли у вас высшее образование и работаете ли вы по этому профилю?", "uuid": "516a4a78-145f-4190-94d6-0613260ce64a"}, "answers": ["высшее гуманитарное или экономическое – работаю не по профилю"]}, {"question": {"title": "Новостями из каких сфер вы интересуетесь регулярно? (Cпособ передачи/потребления информации в данном случае не важен).", "uuid": "f9289823-a6ba-4437-85fa-a5f6731dbbd8"}, "answers": ["построение сообществ", "технологии будущего, новости науки"]}, {"question": {"title": "Выберите из списка все направления, к которым принадлежали ваши проекты за последние 5 лет", "uuid": "b24e881b-ff15-4e06-8a2e-981b46de877d"}, "answers": ["организация сред общения или обучения", "мышление, методология, разработка систем", "работа с современными технологическими решениями"]}, {"question": {"title": "Модули по каким технологиям вам интересны наиболее всего?", "uuid": "534d2173-5312-4360-8bc4-f39c8dd882ad"}, "answers": ["базы данных", "энергетика", "VR/AR(технологии виртуальной реальности) "]}, {"question": {"title": "Какими иностранными языками вы владеете?", "uuid": "3557786b-1b0a-4ab9-a15f-6817e6be55f5"}, "answers": ["английский"]}, {"question": {"title": "Есть ли у вас хобби? Если да, то какое?", "uuid": "4432f582-dfe8-4255-af11-cccfc4aca762"}, "answers": ["Игра программирование"]}, {"question": {"title": "Есть ли у вас личный проект или идея проекта, над которым вы сейчас работаете?", "uuid": "e066f1a5-b252-4cf1-9d34-a67935c9864e"}, "answers": ["цукацуацвацуа"]}, {"question": {"title": "Релевантные теги (ключевые слова) проекта - введите от трех до пяти ключевых слов.", "uuid": "e186c8bf-5c24-4327-a89f-ab36d7d270cb"}, "answers": ["цваыцацукпауцкпцукп"]}, {"question": {"title": "Укажите ссылки на профили ключевых участников вашей команды (ядро команды) в социальных сетях.", "uuid": "25131b6c-f58b-46d7-9fc3-1adceee0ed7d"}, "answers": ["ццыпаывапафывпцфукп"]}, {"question": {"title": "Актуальна ли для вас задача сбора/доукомлпектации команды под ваш проект? Если да, опишите требования к кандидатам.", "uuid": "0a1c55a0-9d57-4c93-b924-e91d467bb836"}, "answers": ["ыуывпыфукпыфукпукпукцп"]}], "WEFtech": [{"question": {"title": "Наноаккумуляторы", "uuid": "484b183c-611d-40d4-a1a0-4f91d401ff1b"}, "answers": ["Анализ и статистика"]}, {"question": {"title": "Электрокар Tesla", "uuid": "7f2404f3-db16-4cd7-aa42-4660e97cf700"}, "answers": ["Автодорожный (сухопутный) транспорт"]}, {"question": {"title": "Замкнутый цикл", "uuid": "577b279e-70b4-4b46-8d19-5d1ba51f072a"}, "answers": ["Солнечная энергетика"]}, {"question": {"title": "Протонообменная мембрана", "uuid": "7b8267e9-cf26-4749-ba80-e4a5c706d6d7"}, "answers": ["Фотоэлементы"]}, {"question": {"title": "Экзоскелеты", "uuid": "f7378f13-4227-4add-8405-c0184591d2ee"}, "answers": ["Микробиологическая промышленность"]}, {"question": {"title": "Ultraprivate смартфоны", "uuid": "9552b4cc-d0c7-4d3b-9f56-6c53de60754d"}, "answers": ["Печать, СМИ (соц. Сети) "]}, {"question": {"title": "Прямоточный двигатель", "uuid": "db3ec471-f37d-410c-9d3f-3125f3b20b72"}, "answers": ["Автомобильная промышленность"]}, {"question": {"title": "Глубокое обучение", "uuid": "945829a6-7c43-44c9-9983-6918e1402e7e"}, "answers": ["Педагогика"]}, {"question": {"title": "MYCIN", "uuid": "fd2615f4-ad80-41ad-a69e-4b80c85431b7"}, "answers": ["IoT (Интернет вещей)"]}, {"question": {"title": "Сильный ИИ", "uuid": "68e79e39-198c-4019-b35a-64bcab1857a9"}, "answers": ["Типология ИИ"]}, {"question": {"title": "Бустинг", "uuid": "de04faa5-aaaf-4f92-a4f3-a7e7cf186259"}, "answers": ["Известные ИИ-системы"]}, {"question": {"title": "Нечеткая логика", "uuid": "bdfdcf0a-da34-48d6-8294-b5216daee080"}, "answers": ["Машинное творчество"]}, {"question": {"title": "Нейроморфные когнитивные системы", "uuid": "a9d08319-5aa5-4034-b3c3-4481333b9725"}, "answers": ["Нейроразвлечения"]}, {"question": {"title": "Брейнфитнес", "uuid": "4d29bff0-d040-4075-975d-705b3f86240c"}, "answers": ["Нейромедтех"]}, {"question": {"title": "Tracking в VR", "uuid": "ef75481b-aed3-4630-9ed7-10d2b6dcacb0"}, "answers": ["Виды систем деятельности"]}, {"question": {"title": "Где часто применяется распознавание маркера?", "uuid": "34b11d95-3f8a-4c7a-b007-47263cb3cbc7"}, "answers": ["Альтернативные источники питания"]}, {"question": {"title": "Биномиальное распределение", "uuid": "e68350a2-7110-4fd0-baa3-29e618eb47d1"}, "answers": ["Интеграция данных"]}, {"question": {"title": "Мода", "uuid": "457e3822-54ef-4682-94a7-f3cf6ca4d210"}, "answers": ["Интеллектуальный анализ данных "]}, {"question": {"title": "Нейронные сети", "uuid": "b7d298b8-dd25-4e73-8235-ee02270c89e9"}, "answers": ["Многомерный статистический анализ"]}, {"question": {"title": "Кластерный анализ", "uuid": "4f931773-06bd-4fe2-9429-bbcd56d521f6"}, "answers": ["Параметрическая статистика"]}, {"question": {"title": "БПЛА", "uuid": "bf91d6bc-0fd3-4f4e-b504-0680b7443b37"}, "answers": ["Взаимодействие человека и робота, этика роботостроения"]}, {"question": {"title": "Реконструкция модели окружающего мира", "uuid": "bb479e41-8be1-45d7-8916-bc497aeba520"}, "answers": ["Случайные леса"]}, {"question": {"title": "FPV", "uuid": "061dde09-7509-4b5b-be3e-c2913e44bdd2"}, "answers": ["Машинное зрение"]}, {"question": {"title": "Лидар", "uuid": "b2f4a4fe-c483-435b-9790-b38b4b3faa28"}, "answers": ["Понимание естественного языка"]}, {"question": {"title": "Токен", "uuid": "d82c440c-c00a-4de5-b452-9176ee0ddb5e"}, "answers": ["Акция"]}, {"question": {"title": "Криптовалюта", "uuid": "c9ed9b9c-fc14-4fea-a644-6e97985edc31"}, "answers": ["Автоматизированная система управления средствами"]}, {"question": {"title": "Майнинг", "uuid": "6f0d1731-f367-47c0-8335-a04c14b60b29"}, "answers": ["Контроль над сетью"]}, {"question": {"title": "Консенсус", "uuid": "605de4e4-f629-4644-b435-aee1ab5b5e0e"}, "answers": ["Автоматизированная система управления средствами"]}], "WEFknowledge": [{"question": {"title": "Заполнение ssd-диска", "uuid": "d52aed0d-dbf2-46fa-b687-193d04621e39"}, "answers": ["31"]}, {"question": {"title": "Кто выйдет на планету первым?", "uuid": "301d1ca5-c806-4f2b-be21-009dbeb9bd35"}, "answers": ["около 60% "]}, {"question": {"title": "Биогель в питательном растворе", "uuid": "ec0975e1-7dac-4391-a54a-ce2b8f7fbd9c"}, "answers": ["200"]}, {"question": {"title": "Параллельные вычисления", "uuid": "05f58b23-b9f7-41c6-8947-f87d67d08e05"}, "answers": ["3"]}, {"question": {"title": "Отчеты и папки", "uuid": "eb9847dd-2a07-4e24-bb5f-959a0fca151d"}, "answers": ["4 отчета, 5 папок"]}, {"question": {"title": "Бензоколонки в Москве", "uuid": "123bc689-e5df-4cb8-9116-ddb25247e286"}, "answers": ["фывафцвацуа"]}, {"question": {"title": "Перегон техники", "uuid": "a5bcce06-f900-4393-8414-8ddbe3cd9238"}, "answers": ["31"]}, {"question": {"title": "Массивно-параллельные вычисления", "uuid": "40c716b1-5f67-458e-a68e-4caee309d415"}, "answers": ["Когда вычисляются уравнения Фурье, Навье Стокса и задачи Particle in Cell "]}, {"question": {"title": "Если руководствоваться данной картой, на каком языке говорят антиподы Веллингтона и Формозы?", "uuid": "08d83e23-39dd-411e-a9f2-cb0b9fa98604"}, "answers": ["Испанском"]}, {"question": {"title": "Экспертиза письма", "uuid": "8c34212f-d449-4da6-8751-61e303af6110"}, "answers": [["Какое заключение сделал эксперт?", "Хуйня"], ["Почему?", "Ну вот так"]]}, {"question": {"title": "Инфузолии в питательном растворе", "uuid": "43467784-a0cd-4b28-85f1-6589904522d2"}, "answers": ["никогда"]}, {"question": {"title": "Выборы председателя компании", "uuid": "29c82049-445d-48a0-b5e6-f1b1a6ad62d4"}, "answers": ["такого в принципе не может произойти"]}, {"question": {"title": "Проблемы менторских сообществ", "uuid": "3243347b-e477-4db0-90ae-c0b5b6904ca5"}, "answers": ["ну как"]}, {"question": {"title": "Ухудшение вкуса рыбы", "uuid": "19e2077f-0a0e-46cc-ad75-cdab7d60edd8"}, "answers": ["В садки запускали хищников "]}, {"question": {"title": "Рекламная площадь", "uuid": "62c7b581-7c7a-488f-9426-5184582146bb"}, "answers": ["фывфывйцв"]}, {"question": {"title": "Отметьте варианты со структурированными данными:", "uuid": "679890f0-40e7-43fa-b5cd-7693bd1978de"}, "answers": ["Данные о скорости и направлении ветра, полученные на гидрометеостанции"]}, {"question": {"title": "Расходы фирмы", "uuid": "270ef887-7967-4b02-a1fd-5c28cede79a5"}, "answers": ["классификации"]}]}',
)

stub = json.loads(
    '{"WEFsurvey": [{"question": {"title": "Последний год вы:", "uuid": "d101147a-6e79-4336-aeb5-5fed41231b2d"}, "answers": ["работали по найму в бизнесе"]}, {"question": {"title": "В какую среду работы и общения вы были больше погружены последние 3 года (на месте работы или учебы)", "uuid": "4a74ea86-3944-4738-86e8-0388d8d03c84"}, "answers": ["академическая среда"]}, {"question": {"title": "Укажите три профессиональных компетенции, которые стали за последний год самыми значимыми в вашей деятельности. Как вы считаете, насколько меньше вы бы зарабатывали, если бы у вас их не было?", "uuid": "c7dfe386-67eb-4a52-9ee0-779ed0fa2004"}, "answers": [["Компетенция 1", "фыва"], ["Компетенция 1 принесла приблизительно % годового дохода", "223"], ["Компетенция 2", "фыв"], ["Компетенция 2 принесла приблизительно % годового дохода", "123"], ["Компетенция 3", "фыва"], ["Компетенция 3 принесла приблизительно % годового дохода", "123"]]}, {"question": {"title": "Укажите количество ваших подписчиков в соцсети Facebook", "uuid": "a5075e74-9bec-40c2-9723-14b1160ffa3e"}, "answers": ["30000"]}, {"question": {"title": "Укажите количество ваших друзей в соцсети Facebook", "uuid": "afcab22d-171f-4aa6-8bae-2e80439ad634"}, "answers": ["123123"]}, {"question": {"title": "Укажите ссылку на ваш профиль в социальной сети, которой вы пользуетесь наиболее часто", "uuid": "d8c338c3-1c04-4928-9982-39034a5b8b87"}, "answers": [""]}, {"question": {"title": "В следующем году вы бы хотели", "uuid": "c258f973-eee1-4a7e-af83-84d6682b7105"}, "answers": ["продолжить работу на прежнем месте"]}, {"question": {"title": "В каком из этих направлений вы видите больше перспектив для своего развития (при равном уровне оплаты и прочих базовых условий)", "uuid": "44b7baab-50f3-49d4-8065-db8154e746a5"}, "answers": ["научная деятельность в области естественных или точных наук"]}, {"question": {"title": "Есть ли у вас высшее образование и работаете ли вы по этому профилю?", "uuid": "516a4a78-145f-4190-94d6-0613260ce64a"}, "answers": ["высшее гуманитарное или экономическое – работаю не по профилю"]}, {"question": {"title": "Новостями из каких сфер вы интересуетесь регулярно? (Cпособ передачи/потребления информации в данном случае не важен).", "uuid": "f9289823-a6ba-4437-85fa-a5f6731dbbd8"}, "answers": ["построение сообществ", "технологии будущего, новости науки"]}, {"question": {"title": "Выберите из списка все направления, к которым принадлежали ваши проекты за последние 5 лет", "uuid": "b24e881b-ff15-4e06-8a2e-981b46de877d"}, "answers": ["организация сред общения или обучения", "мышление, методология, разработка систем", "работа с современными технологическими решениями"]}, {"question": {"title": "Модули по каким технологиям вам интересны наиболее всего?", "uuid": "534d2173-5312-4360-8bc4-f39c8dd882ad"}, "answers": ["базы данных", "энергетика", "VR/AR(технологии виртуальной реальности) "]}, {"question": {"title": "Какими иностранными языками вы владеете?", "uuid": "3557786b-1b0a-4ab9-a15f-6817e6be55f5"}, "answers": ["английский"]}, {"question": {"title": "Есть ли у вас хобби? Если да, то какое?", "uuid": "4432f582-dfe8-4255-af11-cccfc4aca762"}, "answers": ["ЫВАываывпывап"]}, {"question": {"title": "Есть ли у вас личный проект или идея проекта, над которым вы сейчас работаете?", "uuid": "e066f1a5-b252-4cf1-9d34-a67935c9864e"}, "answers": ["цукацуацвацуа"]}, {"question": {"title": "Релевантные теги (ключевые слова) проекта - введите от трех до пяти ключевых слов.", "uuid": "e186c8bf-5c24-4327-a89f-ab36d7d270cb"}, "answers": ["цваыцацукпауцкпцукп"]}, {"question": {"title": "Укажите ссылки на профили ключевых участников вашей команды (ядро команды) в социальных сетях.", "uuid": "25131b6c-f58b-46d7-9fc3-1adceee0ed7d"}, "answers": ["ццыпаывапафывпцфукп"]}, {"question": {"title": "Актуальна ли для вас задача сбора/доукомлпектации команды под ваш проект? Если да, опишите требования к кандидатам.", "uuid": "0a1c55a0-9d57-4c93-b924-e91d467bb836"}, "answers": ["ыуывпыфукпыфукпукпукцп"]}], "WEFtech": [{"question": {"title": "Наноаккумуляторы", "uuid": "484b183c-611d-40d4-a1a0-4f91d401ff1b"}, "answers": ["Анализ и статистика"]}, {"question": {"title": "Электрокар Tesla", "uuid": "7f2404f3-db16-4cd7-aa42-4660e97cf700"}, "answers": ["Автодорожный (сухопутный) транспорт"]}, {"question": {"title": "Замкнутый цикл", "uuid": "577b279e-70b4-4b46-8d19-5d1ba51f072a"}, "answers": ["Солнечная энергетика"]}, {"question": {"title": "Протонообменная мембрана", "uuid": "7b8267e9-cf26-4749-ba80-e4a5c706d6d7"}, "answers": ["Фотоэлементы"]}, {"question": {"title": "Экзоскелеты", "uuid": "f7378f13-4227-4add-8405-c0184591d2ee"}, "answers": ["Микробиологическая промышленность"]}, {"question": {"title": "Ultraprivate смартфоны", "uuid": "9552b4cc-d0c7-4d3b-9f56-6c53de60754d"}, "answers": ["Печать, СМИ (соц. Сети) "]}, {"question": {"title": "Прямоточный двигатель", "uuid": "db3ec471-f37d-410c-9d3f-3125f3b20b72"}, "answers": ["Автомобильная промышленность"]}, {"question": {"title": "Глубокое обучение", "uuid": "945829a6-7c43-44c9-9983-6918e1402e7e"}, "answers": ["Педагогика"]}, {"question": {"title": "MYCIN", "uuid": "fd2615f4-ad80-41ad-a69e-4b80c85431b7"}, "answers": ["IoT (Интернет вещей)"]}, {"question": {"title": "Сильный ИИ", "uuid": "68e79e39-198c-4019-b35a-64bcab1857a9"}, "answers": ["Типология ИИ"]}, {"question": {"title": "Бустинг", "uuid": "de04faa5-aaaf-4f92-a4f3-a7e7cf186259"}, "answers": ["Известные ИИ-системы"]}, {"question": {"title": "Нечеткая логика", "uuid": "bdfdcf0a-da34-48d6-8294-b5216daee080"}, "answers": ["Машинное творчество"]}, {"question": {"title": "Нейроморфные когнитивные системы", "uuid": "a9d08319-5aa5-4034-b3c3-4481333b9725"}, "answers": ["Нейроразвлечения"]}, {"question": {"title": "Брейнфитнес", "uuid": "4d29bff0-d040-4075-975d-705b3f86240c"}, "answers": ["Нейромедтех"]}, {"question": {"title": "Tracking в VR", "uuid": "ef75481b-aed3-4630-9ed7-10d2b6dcacb0"}, "answers": ["Виды систем деятельности"]}, {"question": {"title": "Где часто применяется распознавание маркера?", "uuid": "34b11d95-3f8a-4c7a-b007-47263cb3cbc7"}, "answers": ["Альтернативные источники питания"]}, {"question": {"title": "Биномиальное распределение", "uuid": "e68350a2-7110-4fd0-baa3-29e618eb47d1"}, "answers": ["Интеграция данных"]}, {"question": {"title": "Мода", "uuid": "457e3822-54ef-4682-94a7-f3cf6ca4d210"}, "answers": ["Интеллектуальный анализ данных "]}, {"question": {"title": "Нейронные сети", "uuid": "b7d298b8-dd25-4e73-8235-ee02270c89e9"}, "answers": ["Многомерный статистический анализ"]}, {"question": {"title": "Кластерный анализ", "uuid": "4f931773-06bd-4fe2-9429-bbcd56d521f6"}, "answers": ["Параметрическая статистика"]}, {"question": {"title": "БПЛА", "uuid": "bf91d6bc-0fd3-4f4e-b504-0680b7443b37"}, "answers": ["Взаимодействие человека и робота, этика роботостроения"]}, {"question": {"title": "Реконструкция модели окружающего мира", "uuid": "bb479e41-8be1-45d7-8916-bc497aeba520"}, "answers": ["Случайные леса"]}, {"question": {"title": "FPV", "uuid": "061dde09-7509-4b5b-be3e-c2913e44bdd2"}, "answers": ["Машинное зрение"]}, {"question": {"title": "Лидар", "uuid": "b2f4a4fe-c483-435b-9790-b38b4b3faa28"}, "answers": ["Понимание естественного языка"]}, {"question": {"title": "Токен", "uuid": "d82c440c-c00a-4de5-b452-9176ee0ddb5e"}, "answers": ["Акция"]}, {"question": {"title": "Криптовалюта", "uuid": "c9ed9b9c-fc14-4fea-a644-6e97985edc31"}, "answers": ["Автоматизированная система управления средствами"]}, {"question": {"title": "Майнинг", "uuid": "6f0d1731-f367-47c0-8335-a04c14b60b29"}, "answers": ["Контроль над сетью"]}, {"question": {"title": "Консенсус", "uuid": "605de4e4-f629-4644-b435-aee1ab5b5e0e"}, "answers": ["Автоматизированная система управления средствами"]}], "WEFknowledge": [{"question": {"title": "Заполнение ssd-диска", "uuid": "d52aed0d-dbf2-46fa-b687-193d04621e39"}, "answers": ["31"]}, {"question": {"title": "Кто выйдет на планету первым?", "uuid": "301d1ca5-c806-4f2b-be21-009dbeb9bd35"}, "answers": ["около 60% "]}, {"question": {"title": "Биогель в питательном растворе", "uuid": "ec0975e1-7dac-4391-a54a-ce2b8f7fbd9c"}, "answers": ["200"]}, {"question": {"title": "Параллельные вычисления", "uuid": "05f58b23-b9f7-41c6-8947-f87d67d08e05"}, "answers": ["3"]}, {"question": {"title": "Отчеты и папки", "uuid": "eb9847dd-2a07-4e24-bb5f-959a0fca151d"}, "answers": ["4 отчета, 5 папок"]}, {"question": {"title": "Бензоколонки в Москве", "uuid": "123bc689-e5df-4cb8-9116-ddb25247e286"}, "answers": ["фывафцвацуа"]}, {"question": {"title": "Перегон техники", "uuid": "a5bcce06-f900-4393-8414-8ddbe3cd9238"}, "answers": ["31"]}, {"question": {"title": "Массивно-параллельные вычисления", "uuid": "40c716b1-5f67-458e-a68e-4caee309d415"}, "answers": ["Когда вычисляются уравнения Фурье, Навье Стокса и задачи Particle in Cell "]}, {"question": {"title": "Если руководствоваться данной картой, на каком языке говорят антиподы Веллингтона и Формозы?", "uuid": "08d83e23-39dd-411e-a9f2-cb0b9fa98604"}, "answers": ["Испанском"]}, {"question": {"title": "Экспертиза письма", "uuid": "8c34212f-d449-4da6-8751-61e303af6110"}, "answers": [["Какое заключение сделал эксперт?", "Хуйня"], ["Почему?", "Ну вот так"]]}, {"question": {"title": "Инфузолии в питательном растворе", "uuid": "43467784-a0cd-4b28-85f1-6589904522d2"}, "answers": ["никогда"]}, {"question": {"title": "Выборы председателя компании", "uuid": "29c82049-445d-48a0-b5e6-f1b1a6ad62d4"}, "answers": ["такого в принципе не может произойти"]}, {"question": {"title": "Проблемы менторских сообществ", "uuid": "3243347b-e477-4db0-90ae-c0b5b6904ca5"}, "answers": ["ну как"]}, {"question": {"title": "Ухудшение вкуса рыбы", "uuid": "19e2077f-0a0e-46cc-ad75-cdab7d60edd8"}, "answers": ["В садки запускали хищников "]}, {"question": {"title": "Рекламная площадь", "uuid": "62c7b581-7c7a-488f-9426-5184582146bb"}, "answers": ["фывфывйцв"]}, {"question": {"title": "Отметьте варианты со структурированными данными:", "uuid": "679890f0-40e7-43fa-b5cd-7693bd1978de"}, "answers": ["Данные о скорости и направлении ветра, полученные на гидрометеостанции"]}, {"question": {"title": "Расходы фирмы", "uuid": "270ef887-7967-4b02-a1fd-5c28cede79a5"}, "answers": ["классификации"]}]}',
)


class BaseComputeTest(TestCase):
    def setUp(self):
        self.data = {
            1: stub,
            2: stub,
            3: stub
        }

        self.question_map = {
            "news": "f9289823-a6ba-4437-85fa-a5f6731dbbd8",
            "hobby": '4432f582-dfe8-4255-af11-cccfc4aca762',
            "project": "b24e881b-ff15-4e06-8a2e-981b46de877d",
            "education": "516a4a78-145f-4190-94d6-0613260ce64a",
            "language": "3557786b-1b0a-4ab9-a15f-6817e6be55f5",
            "environment": '4a74ea86-3944-4738-86e8-0388d8d03c84',
            "main_competence": 'c7dfe386-67eb-4a52-9ee0-779ed0fa2004'
        }
        self.df = build_df(self.data, self.question_map)


class CoreTestCase(BaseComputeTest):

    def test_matrix_compute(self):
        df = self.df
        self.assertTrue(set(df.index) == set(self.data.keys()))
        self.assertTrue(set(df.columns) == set(self.question_map.values()))

    def test_base_matrix(self):
        df = self.df
        r = _get_base(df, self.question_map)

    def test_environmetn(self):
        df = self.df
        r = _get_environment(df, self.question_map)

class ExperienceSimilarityTest(BaseComputeTest):

    def test_get_project_matrix(self):
        r = _get_project_directions(self.df, self.question_map)
        print("proj")
        print(r)

    def test_get_education_matrix(self):
        r = _get_education(self.df, self.question_map)
        print("educ")
        print(r)

    def test_get_experience_similarity(self):
        r = get_experience_similarity(self.df, self.question_map)
        print("exp_sim")
        print(r)


class InterestsSimilarityTest(BaseComputeTest):

    def test_get_news_matrix(self):
        r = _get_news(self.df, self.question_map)
        print("news")
        print(r)

    def test_get_hobby_matrix(self):
        r = _get_hobby(self.df, self.question_map)
        print('hobby')
        print(r)

    def test_interests_similarity(self):
        r = get_interests_similarity(self.df, self.question_map)
        print('int_sim')
        print(r)


class CompetenceSimilarityTest(BaseComputeTest):

    def test_get_language_matrix(self):
        r = _get_language(self.df, self.question_map)
        print('lang')
        print(r)

    def test_get_main_competence_matrix(self):
        r = _get_main_competence(self.df, self.question_map)
        print('comp')
        print(r)

    def test_competence_similarity(self):
        r = get_competence_similarity(self.df, self.question_map)
        print('comp sim')
        print(r)
