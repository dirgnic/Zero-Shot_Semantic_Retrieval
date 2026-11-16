from itertools import permutations

IDIOMS = (
    "rm-sursilv",
    "rm-sutsilv",
    "rm-surmiran",
    "rm-puter",
    "rm-vallader",
)

SPLITS = ("train", "validation", "test", "no_surm")

HF_DATASET = "ZurichNLP/mediomatix"
HF_PARQUET_URL = (
    "https://huggingface.co/api/datasets/"
    f"{HF_DATASET}/parquet/default/{{split}}/0.parquet"
)

DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
XLM_R_MODEL = "FacebookAI/xlm-roberta-base"
DEFAULT_MODELS = (DEFAULT_MODEL, XLM_R_MODEL)
DEFAULT_MAX_SEQ_LENGTH = 128


def all_pairs():
    return tuple(permutations(IDIOMS, 2))
