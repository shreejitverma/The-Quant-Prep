# Archive

Material kept for reference but outside the curriculum.
Nothing here is indexed by `qp`, checked by `qp check`, or linked from the syllabus except where a note says so explicitly.

## `legacy/`

The repo's content before the 2026 restructure into the numbered syllabus, moved here unchanged (history is preserved by `git mv`).
It is mostly Jupyter notebooks and scripts collected from many sources: book companion repositories (for example the Yves Hilpisch / The Python Quants book code in `08_research_and_resources/external_resources`), open-source projects (FinRL, pysystemtrade and others), course exercises, and YouTube-series notebooks.
Several collections carry their own licences and attributions; check a folder's README and licence before reusing or redistributing anything from it.
Large binaries (Windows DLLs, a browser installer, IDE folders) were deleted during the move.

Useful starting points:

| Folder | Contents |
| :--- | :--- |
| `legacy/02_quantitative_data_analysis/misc_notebooks/` | Numbered notebooks on stochastic calculus, options, volatility, Markov models and Monte Carlo, each with a video link. |
| `legacy/02_quantitative_data_analysis/notebooks_collection/` | Dated notebooks on option pricing, Monte Carlo variance reduction, Heston calibration and weather derivatives. |
| `legacy/05_algorithmic_trading/` | Strategy notebooks, backtesting frameworks and RL trading environments. |
| `legacy/08_research_and_resources/external_resources/` | Companion code for several Python-for-finance books. |
| `legacy/08_research_and_resources/seminal_papers/` | Paper collection. |

## `superseded/`

Short early guides by the repo author that the new syllabus notes replace (probability, linear algebra, data structures, study roadmap, Jane Street notes, modern C++, HFT architecture, distributed compute, Java low latency), plus the original toy strategy test.
Their content is covered, and extended, by the notes linked from [Start Here](../00-Start-Here/README.md).
