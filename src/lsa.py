from __future__ import annotations

from typing import Tuple
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline


def lsa_transform(X, n_components: int = 120, random_state: int = 42) -> Tuple[np.ndarray, object]:
    """
    TF-IDF (sparse) -> LSA dense representation.
    Normalization is important for cosine-like behavior.
    """
    svd = TruncatedSVD(n_components=n_components, random_state=random_state)
    normalizer = Normalizer(copy=False)
    pipe = make_pipeline(svd, normalizer)
    X_lsa = pipe.fit_transform(X)  # dense
    return X_lsa, pipe
