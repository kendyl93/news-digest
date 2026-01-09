from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix


PL_STOPWORDS = [
    "i","w","na","do","od","z","za","że","to","się","jest","są","nie","ale","też","oraz",
    "czy","jak","a","o","po","pod","nad","przez","dla","we","ze","już","tym","tej","ten",
    "by","być","będzie","będą","może","można","tam", "gdzie", "mówi", "powiedział", "podaje", 
    "także", "kolejne", "sprawie", "wspólna", "żeby", "czekaj", "tylko", "jeszcze", "więcej", 
    "będą", "będzie", "przed", "ponieważ", "dlatego", "który", "która", "które", "ich", "jego", 
    "jej", "nas", "was", "sobie", "mnie", "mną", "tobie", "tobą", "jednak", "wczoraj", "dziś",
    "tvn24", "rmf24", "polsatnews", "bankier", "money", "wyborcza", "medonet", "google", "news", "pl"
]

def vectorize_tfidf(
    texts: List[str],
    min_df: int = 2,
    ngram_range: Tuple[int, int] = (1, 2),
    max_features: int = 20000,
) -> Tuple[TfidfVectorizer, csr_matrix]:
    """
    Convert a list of texts into TF-IDF vectors.

    Defaults are tuned for "daily news":
    - min_df=2 removes extremely rare tokens (noise)
    - ngram_range=(1,2) captures phrases
    - max_features prevents feature explosion
    """
    vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        lowercase=True,
        min_df=min_df,
        max_df=0.85,
        stop_words=PL_STOPWORDS,
        ngram_range=ngram_range,
        max_features=max_features,
    )
    X = vectorizer.fit_transform(texts)
    return vectorizer, X
