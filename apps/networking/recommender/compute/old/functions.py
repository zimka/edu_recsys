import numpy as np
import scipy as sp

from pandas import DataFrame

from typing import List

from functools import partial
import re
from typing import List

import numpy as np
from scipy import spatial
from pandas import DataFrame, Series
import pymorphy2
from .text_processing import parse_competences


def words_to_vec(words, word_vecs, word_weights=None, min_n_words=1):
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
    morph = pymorphy2.MorphAnalyzer()
    words = np.array(re.findall(r"[\w']+", text.strip().lower()))
    return [morph.parse(w)[0].normal_form for w in words]


def request_distances(vecs, request_vec):
    if np.isnan(vecs).all():
        return None

    return min([spatial.distance.cosine(request_vec, vec) for vec in vecs])


def mean_distances(vec_series, description_vec):
    map_func = partial(request_distances, request_vec=description_vec)
    return DataFrame([v.map(map_func) for v in vec_series]).T.mean(axis=1, skipna=True)


class TeamRecommender:
    def __init__(self, word_vecs: Series, word_weights: Series, vecs_per_field, user_similarity: DataFrame,
                 user_diversity: DataFrame, language_info: Series, worked_together: DataFrame):
        """
        :param word_vecs: Series with word2vec embeddings for russian words
        :param word_weights: Series with weights of words. Currently weights are estimated based on word frequencies
        :param vecs_per_field: word2vec embeddings for data from user surveys. Used to match it with activity description
        :param user_similarity: DataFrame indexed with unti ids by rows and columns. Contains similarity of island users
        :param user_diversity: DataFrame indexed with unti ids by rows and columns. Contains aggregated diversity metrics of island users
        :param language_info: Series with info about programming languages for each user
        :param worked_together: DataFrame indexed with unti ids by rows and columns. Contains 1 if two users worked in the same team and 0 otherwise
        """
        assert all([user_diversity.shape[i] == worked_together.shape[i] for i in range(2)])
        assert (user_diversity.index == worked_together.index).all()
        assert (user_diversity.columns == worked_together.columns).all()

        self.word_vecs = word_vecs
        self.word_weights = word_weights
        self.vecs_per_field = vecs_per_field
        self.user_similarity = user_similarity
        self.user_diversity = user_diversity
        self.language_info = language_info
        self.worked_together = worked_together

    def recommend_users(self, description: str, user_id: int, n_recommendations: int, target_user_ids: list = None,
                        text_match_threshold: float = 0.3):
        """
        :param description: description of the activity or the competence, for each recommendations are requested
        :param user_id: id of the user, who requests recommendations
        :param n_recommendations: maximal number of output recommendations
        :param target_user_ids: user ids of the users, who should be ranked for recommendations
        :param text_match_threshold: threshold for initial user filtration by the description matching
        :return: tuple (list of recommended user ids, list of recommendation scores)
        """
        desc_words = text_to_words(description)
        description_vec = words_to_vec(desc_words, word_vecs=self.word_vecs, word_weights=self.word_weights)
        if target_user_ids is not None:
            vecs_per_field_subset = self.vecs_per_field.map(lambda x: [v.reindex(target_user_ids).dropna() for v in x])
        else:
            vecs_per_field_subset = self.vecs_per_field

        if description_vec is None:
            if target_user_ids is None:
                text_match_distance = Series(0.75, index=self.user_similarity.index)
            else:
                text_match_distance = Series(0.75, index=target_user_ids)
        else:
            distance_matrix = DataFrame({k: mean_distances(v, description_vec) for k, v in vecs_per_field_subset.items()})
            text_match_distance = distance_matrix.min(axis=1).sort_values()
            text_match_distance[text_match_distance > 1] = 1

        desc_words = set(desc_words)
        language_match_ids = self.language_info.index[self.language_info.map(lambda x: len(x & desc_words) > 0)]\
            .intersection(text_match_distance.index)

        text_match_distance[language_match_ids] /= 10

        if target_user_ids is not None:
            unexpected_user_ids = set(target_user_ids) - set(text_match_distance.index)
            if len(unexpected_user_ids) > 0:
                print("Warning: unexpected user ids: {}".format(unexpected_user_ids))

        min_filtered_size = 2 * n_recommendations

        text_match_distance = text_match_distance.sort_values()
        if text_match_distance.size <= min_filtered_size:
            filtered_target_inds = text_match_distance.index
        elif text_match_distance.iloc[min_filtered_size] > text_match_threshold:
            filtered_target_inds = text_match_distance.index[:min_filtered_size]
        else:
            filtered_target_inds = text_match_distance.index[text_match_distance < text_match_threshold]

        similarity_score = 0.7 * (1 - text_match_distance[filtered_target_inds]) + \
                           0.3 * self.user_similarity.loc[user_id, :].reindex(filtered_target_inds).fillna(0)

        diversified_ids = self.diversify_recommendation(user_id, similarity_score, n_recommendations)
        return diversified_ids, similarity_score[diversified_ids].values

    def recommend_me_team(self, user_id: int, user_ids_per_group: list, n_recommendations: int):
        """
        Recommend team for specific activity
        :param user_id: user id for the recommendation
        :param user_ids_per_group: ids of users for each of available groups
        :param n_recommendations: number of output recommendation
        :return: tuple (ids of recommended groups, recommendation scores)
        """
        res_arr = np.array([self.user_similarity.loc[user_id, group_ids].mean() for group_ids in user_ids_per_group])
        res_inds = np.argsort(res_arr)[::-1][:n_recommendations]
        return res_inds, res_arr[res_inds]

    @staticmethod
    def _command_acquaintance_modifiers(d_frac, command_frac, min_frac=0.33, max_frac=0.5):
        d_weights = np.zeros_like(d_frac)

        small_frac_mask = d_frac + command_frac < min_frac
        large_frac_mask = d_frac + command_frac > max_frac
        d_weights[large_frac_mask] = max_frac - command_frac - d_frac[large_frac_mask]
        d_weights[small_frac_mask] = d_frac[small_frac_mask] - (min_frac - command_frac)

        return d_weights

    def diversify_recommendation(self, user_id: int, target_scores: Series, n_recommendations: int, max_iters=1000,
                                 max_acquainted_frac=0.33, recommended_acquainted_frac=0.1):
        stop_iter_num = max(int(n_recommendations * 0.2), max_iters // 10)

        target_scores[user_id] = 0
        target_ids = target_scores.index.values
        target_scores = target_scores.values

        diversity_matrix = self.user_diversity.reindex(index=target_ids, columns=target_ids).fillna(0).values
        worked_together = self.worked_together.reindex(index=target_ids, columns=target_ids).fillna(0).values

        user_id = np.where(target_ids == user_id)[0][0]

        command_ids = list(diversity_matrix[user_id].argsort()[::-1][:n_recommendations])

        max_score, max_score_delay = 0, 0
        best_command_ids = command_ids
        scores = []
        acquainted_ids = np.where(worked_together[user_id])[0]

        for i in range(max_iters):
            if len(command_ids) > n_recommendations:
                command_ids.pop(0)
                command_ids[0] = user_id

            user_weights = diversity_matrix[command_ids].mean(axis=0)
            user_weights[command_ids[1:]] += target_scores[command_ids[1:]]
            user_weights[command_ids[1:]] /= 2

            acquainted_frac = worked_together[user_id, command_ids[1:]].mean()
            if acquainted_frac > max_acquainted_frac:
                user_weights[acquainted_ids] = 0
            elif acquainted_frac < 1e-10:
                user_weights[acquainted_ids] += 10  # Select only acquainted users
            elif acquainted_frac < recommended_acquainted_frac:
                user_weights[acquainted_ids] += (1 - user_weights[acquainted_ids]) / 2

            have_acquainted = worked_together[command_ids, :][:, command_ids].any(axis=1)
            d_frac = worked_together[np.array(command_ids)[~have_acquainted]].mean(axis=0)
            user_weights += TeamRecommender._command_acquaintance_modifiers(d_frac, have_acquainted.mean())
            user_weights[command_ids] = -1

            command_ids.append(user_weights.argmax())

            score = diversity_matrix[command_ids, :][:, command_ids].mean()
            scores.append(score)
            if max_score < score:
                max_score = score
                best_command_ids = command_ids

            if len(scores) > stop_iter_num:
                max_score_delay = max(max_score_delay, scores[-stop_iter_num])
                if abs(max_score_delay - max_score) < 1e-5:
                    break

        return target_ids[best_command_ids[1:]]


class SimilarityBasedNetworkingRecommender:
    def __init__(self, teammates_by_id: dict, interest_similarity: DataFrame, experience_similarity: DataFrame,
                 competence_similarity : DataFrame):
        self.interest_similarity = interest_similarity
        self.experience_similarity = experience_similarity
        self.competence_similarity = competence_similarity
        self.teammates_by_id = teammates_by_id

        self.target_ids = self.interest_similarity.index.values

    def recommend_man(self, unti_id: int, existed_contact_ids: list, recommendation_type: str):
        """
        :param unti_id: id of the user for recommendation
        :param existed_contact_ids: list of previously recommended users for all users
        :param recommendation_type: one of 3 recommendation types: ['interests', 'experience', 'competences']
        :return: single id of the recommendation
        """

        target_ids_filt = set(self.target_ids) - {unti_id} - set(existed_contact_ids)

        if unti_id in self.teammates_by_id:
            target_ids_filt -= self.teammates_by_id[unti_id]

        if len(target_ids_filt) == 0:
            return np.random.choice(self.target_ids[self.target_ids != unti_id]), 0.5

        if recommendation_type == 'interests':
            similarity_arr = self.interest_similarity
        elif recommendation_type == 'experience':
            similarity_arr = self.experience_similarity
        elif recommendation_type == 'competences':
            similarity_arr = self.competence_similarity
        else:
            raise Exception("Unexpected recommendation type: " + recommendation_type)

        similarity_arr = similarity_arr[unti_id][list(target_ids_filt)]
        res_id = similarity_arr.idxmax()
        return res_id, similarity_arr[res_id]




def parse_languages(languages: str):
    languages = languages.split('|')
    if languages[-1][0] == 'д':
        languages = languages[:-1] + languages[-1][17:].split(',')

    return languages


def extract_technology_info(name):
    if "(" in name:
        name = name[:name.find("(")]

    if ":" in name:
        name = name[:name.find(":")]

    return name


def minimum_cosine_distance(vecs1, vecs2):
    return min([sp.spatial.distance.cosine(v1, v2) for v1 in vecs1 for v2 in vecs2])


def text_series_to_word_vecs(series, word_vecs, word_weights):
    series = series.dropna().map(np.unique)
    words = series.map(lambda x: [words_to_vec(text_to_words(v), word_vecs, word_weights=word_weights) for v in x])

    vecs = words.map(lambda x: [v for v in x if v is not None])
    return vecs[vecs.map(len) > 0]


def text_series_to_word_vec(series, word_vecs, word_weights):
    series = series.dropna().map(np.unique)
    return series.map(" ".join).map(text_to_words).map(
        partial(words_to_vec, word_vecs=word_vecs, word_weights=word_weights)).dropna()


def text_series_to_vecs(series, word_vecs, word_weights):
    return series.dropna().map(text_to_words).map(
        partial(words_to_vec, word_vecs=word_vecs, word_weights=word_weights)).dropna()


def pairwise(series, func, full_index=None):
    res = np.array([[func(s1, s2) for s1 in series] for s2 in series])
    try:
        res = DataFrame(res, index=series.index, columns=series.index)
    except ValueError:
        res = DataFrame(np.nan, index=series.index, columns=series.index)
    if full_index is None:
        return res

    return res.reindex(index=full_index, columns=full_index)


def aggregate_similarity_matrices(matrices: List[DataFrame], weights: np.array):
    assert len(matrices) == len(weights)
    similarities = np.concatenate([np.atleast_3d(m.values) for m in matrices], axis=2)
    user_similarity = np.nan_to_num(similarities * weights).sum(axis=2)
    divider = (~np.isnan(similarities) * weights).sum(axis=2)
    divider[divider < 1e-10] = 1
    user_similarity /= divider

    nan_ids = np.where(np.isnan(user_similarity))
    user_similarity = np.nan_to_num(user_similarity)

    user_similarity[nan_ids] = (user_similarity.mean(axis=0)[nan_ids[0]] + user_similarity.mean(axis=1)[nan_ids[1]]) / 2
    return DataFrame(user_similarity, index=matrices[0].index, columns=matrices[0].columns)


def prepare_environment_data(environment_data):
    return environment_data.dropna().map(lambda x: {v for v in x if isinstance(v, str)} if isinstance(x, list) else {x})


def prepare_competence_with_income_data(data):
    return data.dropna().map(parse_competences).dropna()