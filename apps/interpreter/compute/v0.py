"""
В v0 находится интерпретатор, использовавшийся на ВЭФ(09.2018), рассчитывающий балл
пользователя по направлениям на основе диагностических тестов.
https://wiki.2035.university/pages/viewpage.action?pageId=1179912
"""

from functools import partial

import numpy as np
import pandas as pd
from django.conf import settings

from edu_coresys.models import Directions
from apps.interpreter.models import PleQuestionIdUuidMap


def equals_approx(value, prec, eps=0.05):
    try:
        value = float(value)
    except ValueError:
        return False
    return abs(float(value) - float(prec)) < float(prec)*eps


def any_equals_approx(answers, prec, eps=0.05):
    f = partial(equals_approx, prec=prec, eps=eps)
    return any(map(f, answers))


def has_string(answer_map, a):
    def f(answers):
        total = 0
        for key, score in answer_map.items():
            if key in answers:
                total += score
        return total
    return f(a)


class TestChecker:
    def __init__(self, correct_rules, direction_lists):
        self.rules = correct_rules
        self.direction_lists = direction_lists

    def get_score(self, test_answer):
        default = lambda x:0
        rule = self.rules.get(test_answer.id, default)
        if not len(test_answer.answers):
            score = 0
        else:
            score = rule(test_answer.answers)
        data = {}
        for k in Directions.KEYS:
            if test_answer.id in self.direction_lists[k]:
                data[k] = score
            else:
                data[k] = 0
        return data


class TestAnswer:
    def __init__(self, uuid, answers):
        self.uuid = uuid
        self.answers = answers

    @classmethod
    def from_results(cls, result):
        try:
            return cls(result['question']['uuid'], result['answers'])
        except:
            return cls(None, [], None)

    @property
    def id(self):
        if hasattr(self, "_id"):
            return self._id
        self._id = PleQuestionIdUuidMap.get_id_by_uuid(self.uuid)
        return self._id


def compute_knowledge(results):
    COMPUTE_KNOWLEDGE_RULES = {
        824: lambda a: has_string({"31":1}, a),
        825: lambda a: has_string({"около 50%": 1, "около 60% ":3 }, a),
        826: lambda a: has_string({
            "200":-2,
        }, a),
        827: lambda a: 2 if any_equals_approx(a, 3.3) else 0,
        828: lambda a: has_string({"4 отчета, 5 папок":2}, a),
        829: lambda a: 1,
        830: lambda a: has_string({"11.5":1}, a),
        831: lambda a: has_string({
            "Когда Процесс можно представить как совокупность мелких однотипных процессов": 1,
            "При необходимости распределенных вычислений": 1,
            "Когда вычисляются уравнения Фурье, Навье Стокса и задачи Particle in Cell": 2
        }, a),
        839: lambda a: has_string({
            "Школьный журнал учета посещаемости" :2,
            "Данные о скорости и направлении ветра, полученные на гидрометеостанции" :1
            }, a),
        840: lambda a: has_string({
            "классификации": 2
            }, a),
        832: lambda a: 0,
        833: lambda a: 0,
        834: lambda a: has_string({
            "в конце 28 часа": 1,
            "никогда": 2
            }, a),
        835: lambda a: has_string({
            "выберут дочь председателем" :1,
            "такого в принципе не может произойти" :3
            }, a),
        836: lambda a:0,
        837: lambda a:has_string({
            "В садки запускали хищников": 2
            }, a),
        838: lambda a: 0
    }
    COMPUTE_DIRECTION_LIST = {
        Directions.DATA_ANALYST:[824,825,826, 828, 829,830, 831, 839, 840, 832, 833, 835],
        Directions.TECHNOLOGIST: [824, 825, 826,827, 828, 830,831,832, 834, 836, 837, 838],
        Directions.BUSINESS_ARCHITECT: [829, 839, 840, 832, 833,834, 835,836,837],
        Directions.ENTREPRENEUR: [824, 828, 829,832, 833, 835, 837, 838],
        Directions.COMMUNITY_LEADER: [829, 840, 832, 833, 834, 835, 836],
        Directions.ORGANIZER: [824, 828,829,830,832,833,834,836,837,838]
    }

    checker = TestChecker(COMPUTE_KNOWLEDGE_RULES, COMPUTE_DIRECTION_LIST)
    scores = []
    for q in results:
        t = TestAnswer.from_results(q)
        scores.append(checker.get_score(t))
    df = pd.DataFrame(scores)
    return df.sum().to_dict()


def compute_tech(results):
    def sqhas_string(string, a):
        return has_string({string: 0.5}, a)
    COMPUTE_RULES = {
        778: lambda a: sqhas_string("Электрификация (электроэнергетика)", a),
        779: lambda a: sqhas_string("Автодорожный (сухопутный) транспорт", a),
        780: lambda a: sqhas_string("Ядерная энергетика", a),
        781: lambda a: sqhas_string("Низкотемпературные топливные элементы", a),
        782: lambda a: sqhas_string("Физкультура и спорт", a),
        783: lambda a: sqhas_string("Связь (почта, телеграф, телефон)", a),
        784: lambda a: sqhas_string("Гиперзвуковая авиация и космонавтика", a),
        785: lambda a: sqhas_string("Искусственный интеллект", a),
        786: lambda a: sqhas_string("Известные ИИ-системы", a),
        787: lambda a: sqhas_string("Типология ИИ", a),
        788: lambda a: sqhas_string("Алгоритмы", a),
        789: lambda a: sqhas_string("Подходы", a),
        790: lambda a: sqhas_string("Нейрообразование", a),
        791: lambda a: sqhas_string("Нейроразвлечения", a),
        792: lambda a: sqhas_string("Системы трекинга", a),
        793: lambda a: sqhas_string("AR", a),
        794: lambda a: sqhas_string("Вероятностно-статистическое моделирование", a),
        795: lambda a: sqhas_string("Описательная статистика", a),
        796: lambda a: sqhas_string("Интеллектуальный анализ данных", a),
        797: lambda a: sqhas_string("Многомерный статистический анализ", a),
        798: lambda a: sqhas_string("Покорение атмосферы", a),
        799: lambda a: sqhas_string("Машинное зрение", a),
        800: lambda a: sqhas_string("Взаимодействие человека и робота", a),
        801: lambda a: sqhas_string("Сети датчиков", a),
        802: lambda a: sqhas_string("Средства расчета", a),
        803: lambda a: sqhas_string("Средства расчета", a),
        804: lambda a: sqhas_string("Добыча криптовалюты", a),
        805: lambda a: sqhas_string("Условия исполнения контракта или создания блока", a)
    }
    COMPUTE_DIRECTIONS = {
        Directions.DATA_ANALYST: [785, 786, 787, 788, 789, 794, 795, 796, 797, 799, 804],
        Directions.TECHNOLOGIST: [778, 779, 780, 781, 782, 784, 787, 789, 790, 791, 792, 793, 796, 798, 799, 800, 801, 802, 803, 805],
        Directions.BUSINESS_ARCHITECT: [783, 785, 787, 789, 796, 797, 802, 803, 804],
        Directions.ENTREPRENEUR: [778, 779, 782, 783, 787,791, 792, 793, 798, 799, 801, 802, 803],
        Directions.COMMUNITY_LEADER: [778, 779, 782,783, 787,791,792,793,796,798,799,801,802,803],
        Directions.ORGANIZER:[783, 789, 802, 803, 804]
    }

    checker = TestChecker(COMPUTE_RULES, COMPUTE_DIRECTIONS)
    scores = []
    for q in results:
        t = TestAnswer.from_results(q)
        scores.append(checker.get_score(t))
    df = pd.DataFrame(scores)
    return df.sum().to_dict()


def compute_archetypes(results):
    TOP_1 = {
        Directions.DATA_ANALYST: [
            "аналитик", "исполнитель", "эксперт"
        ],
        Directions.TECHNOLOGIST: [
            "связной", "визионер"
        ],
        Directions.BUSINESS_ARCHITECT: [
            "организатор", "визионер", "конструктор", "хозяин"
        ],
        Directions.ENTREPRENEUR: [
            "аналитик", "связной", "визионер"
        ],
        Directions.COMMUNITY_LEADER: [
            "организатор", "связной", "визионер"
        ],
        Directions.ORGANIZER: [
            "визионер", "связной"
        ]
    }
    TOP_2 = {
        Directions.DATA_ANALYST:[
            "контролер", "преследователь"
        ],
        Directions.TECHNOLOGIST: [
            "аналитик", "хозяин", "контролер", "преследователь", "хакер"
        ],
        Directions.BUSINESS_ARCHITECT: [
            "связной", "аналитик", "контролер", "экспериментатор", "творец"
        ],
        Directions.ENTREPRENEUR : [
            "эксперт", "преследователь", "организатор", "эмпат", "экспериментатор","хакер"
        ],
        Directions.COMMUNITY_LEADER: [
            "вождь"
        ],
        Directions.ORGANIZER: [
            "конструктор", "контролер", "аналитик"
        ]
    }

    keys = []
    for v in TOP_1.values():
        keys.extend(v)
    for v in TOP_2.values():
        keys.extend(v)
    KEYS = sorted(list(set(keys)))
    user_vector = np.zeros(len(KEYS))
    for num, k in enumerate(KEYS):
        if k in results:
            user_vector[num] = int(results[k])
    scores = {}
    for d in Directions.KEYS:
        top1_vec = np.zeros(len(KEYS))
        for num, k in enumerate(KEYS):
            if k in TOP_1[d]:
                top1_vec[num] = 1

        top2_vec = np.zeros(len(KEYS))
        for num, k in enumerate(KEYS):
            if k in TOP_2[d]:
                top2_vec[num] = 0.5
        scores[d] = np.dot(top1_vec, user_vector) + np.dot(top2_vec, user_vector)
    return scores


def compute_survey(results):
    def has_thr(number_map, a):
        if not len(a):
            return 0
        try:
            num = int(a[0])
        except:
            return 0
        for thr, score in number_map.items():
            if num >= thr:
                return score
        return 0

    COMPUTE_DEFAULT_DIRECTIONS = {
        Directions.DATA_ANALYST: [],
        Directions.BUSINESS_ARCHITECT: [],
        Directions.TECHNOLOGIST: [],
        Directions.ORGANIZER: [],
        Directions.COMMUNITY_LEADER: [],
        Directions.ENTREPRENEUR: []
    }

    COMPUTE_ANALYST = {
        806: lambda a: has_string({"работали на фрилансе": 1, "занимались самообразованием":1}, a),
        807: lambda a: has_string({"академическая среда": 1, "научно-исследовательская среда":1}, a),
        812: lambda a: has_string({"продолжить обучение": 1}, a),
        813: lambda a: has_string({"научная деятельность в области естественных или точных наук":1, "работа с большими данными":2}, a),
        815: lambda a: has_string({"Big Data и аналитика": 1}, a),
        816: lambda a: has_string({"работа с большими дата-сетами, поиск закономерностей": 1}, a),
        817: lambda a: has_string({"базы данных": 1}, a)
    }
    COMPUTE_TECHIE = {
        806: lambda a: has_string({"занимались самообразованием": 1}, a),
        807: lambda a: has_string({"академическая среда":1, "научно-исследовательская среда": 1}, a),
        813: lambda a: has_string({"работа с программным кодом": 1}, a),
        814: lambda a: has_string({
            "незаконченное высшее в сфере точных наук или в технической/IT-сфере – работаю по профилю": 2,
            "одно или несколько высших образований в сфере точных наук или в технической/IT-сфере – работаю по профилю": 2,
            "высшее образование в технической/IT-сфере – работаю не по профилю": 1
        }, a),
        815: lambda a: has_string({"проблематика инженерной или IT-сферы": 2}, a),
        816: lambda a: has_string({"работа с современными технологическими решениями": 2}, a),
        817: lambda a: has_string({
            "биотехнологии":1,
            "сенсорика":1,
            "роботехника":1,
            "нейротехнологии":1,
            "энергетика":1,
            "VR / AR(технологии виртуальной реальности)":1,
            "IoT(интернет вещей)":1,
            "блокчейн":1,
            "3Д - моделирование / прототипирование":1
        }, a)

    }
    COMPUTE_BUSINESS = {
        806: lambda a: has_string({"были со/основателем бизнеса": 1}, a),
        807: lambda a: has_string({"бизнес, ориентированный на достижение результата": 1}, a),
        809: lambda a: has_thr({1000:2, 500:1}, a),
        810: lambda a: has_thr({3000:2, 2000:1}, a),
        812: lambda a: has_string({"сформировать команду и запустить вместе новый проект": 1}, a),
        813: lambda a: has_string({"работа, связанная с построением бизнес-процессов": 1}, a),
        816: lambda a: has_string({
            "мышление, методология, разработка систем":2,
            "разработка и поддержание в работе экосистем и организационных процессов, в том числе в бизнес-среде":1}, a),
        818: lambda a: has_string({"английский": 1}, a),
    }

    COMPUTE_ENTERPRENER = {
        806: lambda a: has_string({"были со/основателем бизнеса": 2}, a),
        807: lambda a: has_string({"среда стартапа": 2}, a),
        812: lambda a: has_string({"создать свой бизнес": 1, "сформировать команду и запустить вместе новый проект":2}, a),
        814: lambda a: has_string({"высшее гуманитарное или экономическое – работаю по профилю": 1}, a),
        816: lambda a: has_string({"выведение на рынок новых продуктов с нуля": 2}, a),
        818: lambda a: has_string({"английский": 1, "китайский": 2}, a),
    }

    COMPUTE_COMMUNITY = {
        806: lambda a: has_string({"работали на фрилансе": 1}, a),
        807: lambda a: has_string({"сообщество единомышленников": 2}, a),
        809: lambda a: has_thr({1000: 2, 500: 1}, a),
        810: lambda a: has_thr({3000: 2, 2000: 1}, a),
        815: lambda a: has_string({"построение сообществ": 2}, a),
        817: lambda a: has_string({
            "сенсорика": 1,
            "роботехника": 1,
            "нейротехнологии": 1,
            "энергетика": 1,
            "VR / AR(технологии виртуальной реальности)": 1,
            "IoT(интернет вещей)": 1,
            "блокчейн": 1,
        }, a)
    }

    COMPUTE_ORGANIZER = {
        806: lambda a: has_string({
            "работали по найму в бизнесе":1,
            "работали по найму в государственных организациях":1,
            "занимались самообразованием":1
        }, a),
        807: lambda a: has_string({
            "бизнес, ориентированный на достижение результата": 2,
        }, a),
        813: lambda a: has_string({
            "работа, связанная с построением бизнес-процессов": 1,
        }, a),
        814: lambda a: has_string({
            "высшее гуманитарное или экономическое – работаю по профилю": 1
        }, a),
        815: lambda a: has_string({
            "управление бизнес-проектами": 1
        }, a),
        816: lambda a: has_string({
            "разработка и поддержание в работе экосистем и организационных процессов, в том числе в бизнес-среде": 1
        }, a),
    }
    rules = {
        Directions.DATA_ANALYST: COMPUTE_ANALYST,
        Directions.BUSINESS_ARCHITECT: COMPUTE_BUSINESS,
        Directions.TECHNOLOGIST: COMPUTE_TECHIE,
        Directions.ENTREPRENEUR: COMPUTE_ENTERPRENER,
        Directions.ORGANIZER: COMPUTE_ORGANIZER,
        Directions.COMMUNITY_LEADER: COMPUTE_COMMUNITY
    }
    scores = []
    mult = getattr(settings, "DIAGNOSTICS_V0_TECHIE_MULTIPLIER", 1.5)
    for d in Directions.KEYS:
        current_rules = rules[d]
        current_directions = COMPUTE_DEFAULT_DIRECTIONS.copy()
        current_directions[d] = list(current_rules.keys())
        checker = TestChecker(current_rules, current_directions)
        for q in results:
            t = TestAnswer.from_results(q)
            scores.append(checker.get_score(t))
    df = pd.DataFrame(scores)

    return (mult*df.sum()).to_dict()


def compute_v0(data):
    import logging
    log = logging.getLogger(__name__)
    mapping = settings.DIAGNOSTICS_V0_GUID_TO_COMMON
    common_names = {
        "behavior_archetypes": compute_archetypes,
        "knowledge": compute_knowledge,
        "survey": compute_survey,
        "tech": compute_tech
    }
    scores = []
    for key, value in data.items():
        common = mapping.get(key, None)
        log.info("{} {} {}".format(key, common, data.keys()))
        if common in common_names:
            scores.append(common_names[common](value))
    log.info(scores)
    res = pd.DataFrame(scores).sum().to_dict()
    norm = settings.DIAGNOSTICS_V0_NORM
    shift = settings.DIAGNOSTICS_V0_MU
    results = {}
    for key, value in res.items():
        score = value/norm[key] + shift[key]
        results[key] = min(int(score), 100)
    return results


def add_archetype_motivalis_uuids(data):
    results = {}
    inverse_mapping = dict((v,k) for (k, v) in settings.DIAGNOSTICS_V0_GUID_TO_COMMON.items())
    archetypes_map_uuids = settings.DIAGNOSTICS_V0_ARCHETYPES_UUIDS
    archetypes = data.get(inverse_mapping ['behaviour_archetypes'], {})
    for a,value in archetypes.items():
        key = archetypes_map_uuids.get(a)
        if key:
            results[key] = value

    motivalis_map_uuids = settings.DIAGNOSTICS_V0_MOTIVALIS_UUIDS
    motivalis = data.get(inverse_mapping ['behaviour_motivalis'], {})
    for a,value in motivalis.items():
        key = motivalis_map_uuids.get(a)
        if key:
            results[key] = value
    return results

