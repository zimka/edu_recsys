import bz2
import io
import pandas as pd
import os

def get_word_vecs():
    try:
        return get_word_vecs_fast()
    except IOError:
        return get_word_vecs_long()


def get_word_vecs_fast():
    path = os.path.dirname(os.path.abspath(__file__))
    return pd.read_pickle(path + "/w2v_extended.pickle")


def get_word_vecs_long():
    path = os.path.dirname(os.path.abspath(__file__)) + "/w2v_extended.csv.bz2"
    zipfile = bz2.BZ2File(path)  # open the file
    data = zipfile.read()  # get the decompressed data
    return pd.read_csv(io.BytesIO(data))


def get_word_freqs():
    path = os.path.dirname(os.path.abspath(__file__))
    return pd.read_table(path + "/russian_word_frequencies.csv", index_col=0)["Freq(ipm)"]


def get_word_weights():
    word_freqs = get_word_freqs()
    return 1 / word_freqs
