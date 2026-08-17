# Neue metrische Grafiken (2026-08-12)

- STS summary rows: 22; complete Original-GS rows used for boxplots: 16
- SuGaR-Coarse summary rows: 12; complete rows used for boxplots: 12
- STS overview includes grey intermediate `sts_masked.json` values from incomplete SuGaR-route experiments; they are not ranked as complete runs.
- SuGaR-Coarse overview uses only `sugar_coarse_masked.json` and never substitutes `sts_masked.json`.
- Boxplots use the `per_frame` values from the corresponding JSON files.
- Boxplot points are placed on their category and receive only a small horizontal spread; y-ranges include all per-frame values.
- Runtime scatter uses archived STS-to-postprocess durations and is exploratory because SAM3/COLMAP wall time was not archived per experiment.
- Runtime x-axis is fixed to 15-40 minutes; light colors encode FPS and point/square/triangle encode 720p/QHD/Low.
- Camera names are explicit x-axis labels; camera legends are intentionally omitted.
- `middle` is used upstream for coverage and fixed-split eligibility; metric JSONs document `mask_level=default` for PSNR/SSIM/LPIPS aggregation.
- Cross-resolution values are sensitivity results, not one global quality ranking; paired same-resolution comparisons are stronger.

## Files

- `sts_masked_overview.pdf` / `sugar_coarse_masked_overview.pdf`: aggregate per-run metric comparisons
- `sts_masked_per_frame_boxplots.pdf` / `sugar_coarse_masked_per_frame_boxplots.pdf`: per-view distributions
- `sugar_coarse_vs_sts_delta.pdf`: paired stage difference on identical follow-up runs
- `metric_vs_runtime.pdf`: exploratory metric/runtime relation
- `*_summary.csv`, `*_per_frame.csv`: provenance sources
