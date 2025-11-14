# Rung

Causal discovery and inference lab

## Project Structure


## Setup
Uses pyproject.toml and `uv` for dependencies.

### Graphviz
Requires graphviz. Follow https://pygraphviz.github.io/documentation/stable/install.html

For Linux, be sure to install the `libgraphviz-dev` version of the package.

For Windows, use the following command to install `pygraphviz` so it can locate the `graphviz` library files.

```
uv pip install --config-settings="--global-option=build_ext" --config-settings="--global-option=-IC:\Program Files\Graphviz\include" --config-settings="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz
```

then, use `uv sync` to create a venv, then activate it to enter the environment
