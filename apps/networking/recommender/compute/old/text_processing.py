import re

import numpy as np
import pymorphy2
import scipy as sp
from Levenshtein import distance
from pandas import Series


def parse_word2vec(path):
    with open(path) as f:
        lines = list(f)

    text = "".join([l.replace('\n', '\t') for l in lines])
    text_parts = [t.split("\t[") for t in text.split("]\t")]

    return Series({p[0].split("\t")[1]: np.array(list(map(float, p[1].split()))) for p in text_parts[:-1]})


def find_merge_target(word, target_words, merge_threshold):
    distances = [distance(word, w2) for w2 in target_words]
    merge_ind = np.argmin(distances)
    if distances[merge_ind] / max(len(word), len(target_words[merge_ind])) > merge_threshold:
        return None

    return target_words[merge_ind]


def extend_word_vec(all_words, word_vecs):
    word_vecs = word_vecs.copy()
    new_words = set(all_words) - set(word_vecs.index)
    known_words = list(word_vecs.index)
    for word in (new_words):
        target = find_merge_target(word, known_words, merge_threshold=0.3)
        if target is None:
            continue

        word_vecs[word] = word_vecs[target]

    return word_vecs


def text_to_vec(words, word_vecs, word_weights=None, min_n_words=1):
    vecs = []
    known_words = set(word_vecs.index)
    sum_weight = 0
    for word in words:
        if word in known_words:
            weight = word_weights[word] if word_weights is not None and word in word_weights else 1
            sum_weight += weight
            vecs.append(word_vecs[word] * weight)

    if len(vecs) < min_n_words:
        return None

    return np.atleast_2d(vecs).sum(axis=0) / sum_weight


def text_to_words(text):
    # return np.array(re.findall(r"[\w']+", text.strip().lower()))
    morph = pymorphy2.MorphAnalyzer()
    words = np.array(re.findall(r"[\w']+", text.strip().lower()))
    return [morph.parse(w)[0].normal_form for w in words]

def list_to_str(lst):
    return " ".join(map(str, lst))


def str_to_list(string):
    return np.array(list(map(float, string.split())))


def cosine_similarity(src_vec, target_vecs):
    return 1 - np.array([sp.spatial.distance.cosine(src_vec, v) for v in target_vecs])


def jaccard_similarity(s1, s2, min_len=1):
    union_len = len(s1 | s2)
    if union_len < min_len:
        return 0

    return len(s1 & s2) / union_len


# Competences
def parse_competence(competences, c_id):
    salary_question = 'принесла приблизительно % годового дохода'

    c_parts = competences[c_id:c_id + 2]
    if c_parts[0][0] == salary_question or len(c_parts[0][1].strip()) == 0:
        return []

    salary = 0

    if len(c_parts) != 1 and c_parts[1][0] == salary_question:
        try:
            salary = float(c_parts[1][1].strip())
        except:
            pass

    return text_to_words(c_parts[0][1]), salary, c_parts[0][1]


def parse_competences(competences):
    try:
        if not len(competences):
            return None
    except:
        return None
    if len(competences[0]) < 2:
        return None

    if not isinstance(competences[0], list):
        competences = [competences]

    comps = [parse_competence(competences, i) for i in range(len(competences))]
    return [c for c in comps if len(c) > 0]
