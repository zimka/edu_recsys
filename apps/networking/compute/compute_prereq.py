import numpy as np
import scipy as sp
import pandas as pd
from .old import pairwise, jaccard_similarity, text_series_to_vecs, get_word_vecs, get_word_weights, \
    aggregate_similarity_matrices, prepare_environment_data, prepare_competence_with_income_data, text_to_vec, minimum_cosine_distance


from django.conf import settings
default_question_map = getattr(settings, "NETWORKING_QUESTION_MAP")

word_vecs = get_word_vecs()
word_weights = get_word_weights()


def get_question_answer(answers, quid):
    for guid in answers.keys():
        for a in answers.get(guid, {}):
            if not isinstance(a, dict):
                continue
            if a['question']['uuid'] == quid:
                return a['answers']
    return []


def build_df(users_diagnostics, quids_guids):
    data = []
    for user, diagnostics in users_diagnostics.items():
        current = {}
        for common, quid in quids_guids.items():
            current[quid] = get_question_answer(diagnostics, quid)
        current['uid'] = user
        data.append(current)
    return pd.DataFrame(data).set_index('uid')

# BASE

def _get_environment(user_diagnostics_df, question_map):
    quid = question_map["environment"]
    environment = prepare_environment_data(user_diagnostics_df[quid])
    return 1 - pairwise(environment, jaccard_similarity)


def _get_base(user_diagnostics_df, question_map=default_question_map):
    return _get_environment(user_diagnostics_df, question_map)

# INTERESTS

def _get_news(user_diagnostics_df, question_map):
    quid = question_map["news"]
    news_info = user_diagnostics_df[quid]
    news_info = news_info.dropna().map(np.unique).map(lambda x: set(x) - {'ничего из перечисленного.'})
    news_info = news_info[news_info.map(len) > 0]
    return pairwise(news_info, jaccard_similarity, user_diagnostics_df.index)


def _get_hobby(user_diagnostics_df, question_map):
    quid = question_map["hobby"]
    hobbies = user_diagnostics_df[quid]
    hobbies = hobbies.apply(lambda x: " ".join(x) if x is not None else "")
    assert (hobbies.map(type) == str).all()
    hobby_vecs = text_series_to_vecs(hobbies, word_vecs, word_weights=word_weights)
    try:
        res = pairwise(hobby_vecs, sp.spatial.distance.cosine, user_diagnostics_df.index)
    except Exception:
        res = np.zeros((len(user_diagnostics_df), len(user_diagnostics_df))) + 1
        res = pd.DataFrame(res,index=user_diagnostics_df.index, columns=user_diagnostics_df.index)
    res = np.maximum(1 - res, 0)
    return res


def get_interests_similarity(user_diagnostics_df, question_map=default_question_map):
    base_similarity = _get_base(user_diagnostics_df, question_map)
    news_similarity = _get_news(user_diagnostics_df, question_map)
    hobby_similarity = _get_hobby(user_diagnostics_df, question_map)
    return aggregate_similarity_matrices(
        [base_similarity, news_similarity, hobby_similarity],[1.0, 1.0, 0.7]
    )

# EXPERIENCE

def _get_project_directions(user_diagnostics_df, question_map):
    quid = question_map["project"]
    project_area_info = user_diagnostics_df[quid]
    project_area_info = project_area_info.dropna().map(np.unique).map(set)
    return pairwise(project_area_info, jaccard_similarity, user_diagnostics_df.index)


def _get_education(user_diagnostics_df, question_map):
    quid = question_map["education"]
    education_info = user_diagnostics_df[quid]
    return pairwise(education_info, lambda x, y: int(x == y), user_diagnostics_df.index)


def get_experience_similarity(user_diagnostics_df, question_map=default_question_map):
    base_similariry = _get_base(user_diagnostics_df, question_map)
    project_area_similarity = _get_project_directions(user_diagnostics_df, question_map)
    education_similarity = _get_project_directions(user_diagnostics_df, question_map)

    return aggregate_similarity_matrices(
        [base_similariry, project_area_similarity, education_similarity],
        [1., 1.0, 0.5]
    )

# COMPETENCE

def _get_language(user_diagnostics_df, question_map):
    quid = question_map["language"]
    data = user_diagnostics_df[quid]
    language_info = data.dropna().map(
        lambda x: {v for v in x if v[:3] != "дру"})
    return pairwise(language_info, jaccard_similarity,user_diagnostics_df.index)


def _get_main_competence(user_diagnostics_df, question_map):
    quid = question_map["main_competence"]
    data = user_diagnostics_df[quid]
    competence_words = prepare_competence_with_income_data(data).map(lambda x: [v[0] for v in x])
    competence_vecs = competence_words.map(
        lambda x: [text_to_vec(words, word_vecs, word_weights=word_weights) for words in x])
    competence_vecs = competence_vecs.map(lambda x: [v for v in x if v is not None])
    competence_vecs = competence_vecs[competence_vecs.map(len) > 0]
    return np.maximum(1 - pairwise(competence_vecs, minimum_cosine_distance, user_diagnostics_df.index), 0)


def get_competence_similarity(user_diagnostics_df, question_map=default_question_map):
    base_similarity = _get_base(user_diagnostics_df, question_map)
    language_similarity = _get_language(user_diagnostics_df, question_map)
    main_competence_similarity = _get_main_competence(user_diagnostics_df, question_map)
    return aggregate_similarity_matrices(
        [base_similarity, language_similarity, main_competence_similarity],
        [1.0, 0.8, 0.8]
    )


def compute_similarities(students_desired, question_map=default_question_map):
    from apps.interpreter.models import SingleScoreComputeTask

    uids = [u.uid for u in students_desired]
    students_profiles = SingleScoreComputeTask.objects.filter(complete=True, user__uid__in=uids)
    user_diagnostics = {}
    for u in uids:
        current_student_profile = list(filter(lambda x: x.user.uid==u, students_profiles))
        if len(list(current_student_profile)):
            current_student_profile = sorted(current_student_profile, key=lambda x:x.created)
            user_diagnostics[u] = current_student_profile[0].input
    df = build_df(user_diagnostics, question_map)
    validated_students = list(u for u in students_desired if u.uid in user_diagnostics.keys())
    return validated_students, \
           get_competence_similarity(df, question_map), \
           get_interests_similarity(df, question_map), \
           get_experience_similarity(df, question_map)
