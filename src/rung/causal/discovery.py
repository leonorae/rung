import pandas as pd
import bnlearn as bn
from typing import Dict, Any, List, Optional

def run_causal_discovery(
    df: pd.DataFrame,
    method: str = "pc",
    alpha: float = 0.05,
    max_iter: int = 100
) -> Dict[str, Any]:
    if method == "pc":
        model = bn.structure_learning.fit(
            df,
            methodtype='cs',
        )
        model = bn.independence_test(
            model,
            df,
            alpha=alpha,
            prune=True
        )
    elif method == "hillclimb":
        model = bn.structure_learning.fit(
            df,
            methodtype='hc',
            scoretype='bic'
        )
    elif method == "chow-liu":
        model = bn.structure_learning.fit(
            df,
            methodtype='cl'  # Chow-Liu (tree structure)
        )
    else:
        raise ValueError(f"Unknown method: {method}")

    # if Prune:
        model = bn.independence_test(
            model,
            df,
            alpha=alpha,
            prune=True)

    edges = [(str(u), str(v)) for u, v in model['model'].edges()]
    nodes = [str(n) for n in model['model'].nodes()]

    model_params = bn.parameter_learning.fit(model, df)

    results = {
        "method": method,
        "nodes": nodes,
        "edges": edges,
        "n_edges": len(edges),
        "n_nodes": len(nodes),
        "parameters": {
            "alpha": alpha if method == "pc" else None,
            "max_iter": max_iter
        }
    }

    return results


def get_supported_methods() -> List[str]:
    """Return list of supported causal discovery methods"""
    return ["pc", "hillclimb", "chow-liu"]