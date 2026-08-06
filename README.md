# Scan-to-BIM 3D Reconstruction Pipeline

This repository implements a 5-container Docker-based pipeline for the reconstruction of linear infrastructure (specifically underground cables in construction trenches) for TenneT. The pipeline integrates Meta's SAM 3 for 2D object segmentation, COLMAP for camera poses, Segment-then-Splat (STS) for object-specific 3D Gaussian Splatting, SuGaR for geometric mesh extraction, and DGtal/GDAL for centerline extraction and georeferencing.

---

## Getting Started

### 1. Repository & Data Split
To allow development on local machines and high-performance execution on a GPU-enabled server:
- All source code and Docker configuration files are tracked by Git.
- The `data/` folder is listed in `.gitignore` and is local to the machine running the calculations. You must create this folder locally:
  ```bash
  mkdir -p data/01_raw data/02_frames data/03_masks data/04_sfm data/05_3dgs data/06_mesh data/07_centerline data/08_gis data/09_evaluation
  ```

### 2. Preparing Raw Data

```bash
mkdir -p data/01_raw data/02_frames data/03_masks data/04_sfm data/05_3dgs data/06_mesh data/07_centerline data/08_gis data/09_evaluation
```


Place your starting files in the local `data/` directory:
1. Put the raw 4K drone video in `data/01_raw/video.mp4`.
2. Put the measured GNSS GCP coordinates in `data/01_raw/gcp_coordinates.csv`.

### SuGaR Fork Initialization

The mask-aware SuGaR route uses the project fork pinned by the Git submodule.
After cloning the repository, initialize the submodule before building or
running the SuGaR stage:

```bash
git submodule update --init --recursive
git -C third_party/SuGaR rev-parse HEAD
```

The expected commit is
`48bbfddbb557725f14d0d8e32c30b94b5d95f0e2`. The SuGaR image is built from the
same fork and commit. During development, `run_masked_sugar.sh` mounts the
initialized local checkout through `docker-compose.sugar-dev.yml`; an empty
submodule directory must not be used with that overlay. The current project
worktree additionally contains the uncommitted `train.py` change that allows
the segmented-object `c9000` route. Before a release or fresh clone, commit
that change into the fork and update the parent submodule reference.

The master scripts automatically export the invoking user's numeric
`HOST_UID`/`HOST_GID` for Docker bind mounts. This is required when raw files
use restrictive permissions such as mode `600`; explicit overrides can still
be supplied in the shell.

### 3. Execution
Run the master orchestration script on your GPU-enabled machine:
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

### Per-Run Logging

Every master-pipeline run creates a dedicated directory below
`data/10_runs/<video>_<YYYYMMDD_HHMMSS>/` containing:

- `run.log`: complete terminal and Docker output from the run.
- `run.md`: readable run report with input, timestamps, configuration values,
  step status, step durations and exit status.

The master scripts derive `HOST_UID` and `HOST_GID` automatically so the log
and generated data remain owned by the invoking user. The run directory is
ignored as local generated data and should be archived together with the
corresponding experiment if reproducibility documentation is required. The
Hugging-Face token is validated before SAM3; invalid saved tokens trigger a
hidden replacement prompt and are never written to either report.

If you have already processed the video, extracted SAM 3.1 masks, and computed the COLMAP camera poses, you can bypass the early stages and run the pipeline specifically starting from Segment-then-Splat (STS) onwards:
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh --from sts
```

### COLMAP Frame Profile

The validated default profile for the COLMAP SfM stage is:

```text
1280x720, 5 FPS, SIMPLE_RADIAL, Plain-SIFT with 4096 features,
Sequential Matching overlap 15, Guided Matching disabled
```

By default, `FRAME_PROFILE_SCOPE=all` applies the generated frame set to
SAM3, COLMAP, STS and SuGaR. This is the safe setting for a complete run,
because STS requires masks that correspond exactly to the images used by
COLMAP. Setting `FRAME_PROFILE_SCOPE=colmap` creates a benchmark-only stop
mode: SAM3 still creates the frames and masks, but the pipeline stops after
COLMAP. It must not be continued into STS unless a matching SAM3 mask set for
that frame profile has been generated. An FHD experiment
(1920x1080) for SAM3/STS is therefore a separate, explicitly documented
experiment rather than an implicit change to the COLMAP baseline.

COLMAP retains the original reconstruction for GCP picking and SfM evaluation.
For raw images with lens distortion, the default `SIMPLE_RADIAL` model estimates
the distortion during SfM. After model export, `run_sfm.sh` then runs
`colmap image_undistorter` and writes a separate ideal STS scene below
`data/04_sfm/undistorted/`. The original COLMAP model remains unchanged for the
GCP/UI workflow.

`SIMPLE_PINHOLE` and `PINHOLE` have a different meaning: they are ideal camera
models and assume that the input images were already undistorted before
COLMAP. For these two selections, `run_sfm.sh` deliberately skips
`image_undistorter` and creates an unchanged pass-through STS scene at the same
downstream path. This avoids double undistortion. Choosing `PINHOLE` does not
automatically correct distorted raw images; it is only correct when that input
assumption is true.

In other words, the normal raw-video route is not “undistort before COLMAP and
then use SIMPLE_PINHOLE”. It is “estimate a suitable distortion model in
COLMAP, keep that model for GCP/SfM, and undistort once for STS”. A genuinely
pre-undistorted dataset should instead use `SIMPLE_PINHOLE` or `PINHOLE` and
skip the second step.

### Object-Only Gaussian Mesh (Recommended default: Variant A)

For a segmented cable or pipe, an object-only Gaussian cloud must not be
optimized against unmasked full-frame RGB images. The standard pipeline now
keeps `point_cloud.ply` as the full-scene baseline, exports the genuinely
filtered object cloud as `point_cloud_filtered.ply`, and creates
`point_cloud_filtered_opacity999999.ply` as the geometry-oriented SuGaR input.
The latter deliberately overwrites the retained Gaussian opacities with
`alpha=0.999999`; it is an initialization policy for geometry optimization,
not a claim that the object is physically opaque. Use the guided master runner
for the complete workflow:

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

After STS, the runner confirms or edits the filter thresholds and the
high-opacity alpha, then uses `SUGAR_MESH_MODE=original_gs` by default. This is
variant A from the controlled ablation: the prepared high-opacity STS Gaussian
cloud is used directly, surface depth comes from the projected Diamond-Mesh
z-buffer, and surface sampling, Poisson reconstruction, density cleanup,
decimation, and vertex projection remain active. SuGaR Coarse optimization,
Gaussian-bound Refinement, and UV baking are skipped because the Gaussian cloud
itself is the target representation.

The default extraction uses `min_opacity=0.01`, `black_threshold=0.08`,
`alpha=0.999999`, 200,000 mesh vertices, 5,000,000 surface samples,
`SURFACE_LEVEL=0.3`, Poisson depth 10, density quantile 0.1,
`SURFACE_SAMPLE_SEED=42`, zero RGB/UV dilation, and no consensus crop. The
coarse PLY is preserved under `data/06_mesh/<export-name>/coarse.ply`; an
untextured compatibility OBJ is written as `refined.obj` because Container E
and existing downstream tooling use that filename. The file name does not
mean that SuGaR Refinement was run; `mesh_mode.txt` records the actual route.

The former mask-aware SuGaR Coarse -> Refinement -> UV route remains available
as an explicit comparison with `SUGAR_MESH_MODE=sugar_coarse`. Its c9000 default
is therefore no longer the production default. `EXPLAIN` is accepted at each
configuration prompt.

The STS default uses 7,000 total iterations: 5,000 iterations for the
small/middle object-mask curriculum followed by 2,000 iterations rendering all
configured objects. `stage2_iters` is a curriculum window inside the total,
not an additional 5,000 iterations after the total run. Container C runs with
unbuffered Python output, so the stage-2/stage-3 markers appear in the log at
their actual transition instead of being delayed behind the tqdm progress bar.

For a standalone object-only run after STS, prepare the standard input first
and then launch the default A route:

```bash
./prepare_sugar_input.sh
./run_masked_sugar.sh
```

If the default A extraction was interrupted after its PLY was written, recover
the existing coarse PLY and recreate the compatibility OBJ without retraining:

```bash
SUGAR_MESH_MODE=original_gs EXPORT_ONLY=1 REPLACE=1 ./run_pipeline.sh --from sugar
```

For the legacy route, use `SUGAR_MESH_MODE=sugar_coarse`; only that route
produces the refined Gaussian PLY and textured OBJ. The Centerline path needs
only the local triangle OBJ, not a textured model.

The runner keeps separate tagged checkpoints below `data/sugar_output/` and
refuses to overwrite an existing tag unless `REPLACE=1` is set deliberately.
SuGaR writes its runtime outputs through the shared `/data` mount; this avoids
permission problems caused by mounting a local development fork over
`/opt/sugar`.

### Cleanup und automatisierte Versuche

Das wiederhergestellte [clean_data_interactive.sh](clean_data_interactive.sh)
setzt abgeleitete Pipeline-Daten interaktiv zurück. Es lässt `data/01_raw` und
den Hugging-Face-Cache standardmäßig bestehen; `--new-video` wählt die Defaults
für einen vollständigen Neuaufbau und behandelt `data/01_raw/output.mp4` als
löschbares Arbeitsvideo. Für automatisierte Experimentmatrizen muss zuerst das
Experiment archiviert und mit Prüfsummen gesichert werden; erst danach darf ein
Cleanup ausgeführt werden.

Bei der geplanten Splat-Evaluation werden ausschließlich maskierte
PSNR-/SSIM-/LPIPS-Werte berechnet. Die aktuellen STS- und SuGaR-Modelle sind
object-only Splats; es gibt keinen vollständigen Full-Scene-Splat. Ein
Full-frame-Vergleich mit dem gesamten Originalbild würde deshalb außerhalb der
Objektmaske vor allem den nicht rekonstruierten Hintergrund bewerten und ist für
diese Matrix deaktiviert. Pixel außerhalb der Objektmaske werden bei PSNR/SSIM
nicht in die Kennzahl aufgenommen. LPIPS wird auf einem gemeinsamen
Objekt-Crop mit vereinheitlichtem Außenbereich berechnet. Die implementierte
Auswertung liegt in
[src/python/evaluate_masked_splat_metrics.py](src/python/evaluate_masked_splat_metrics.py)
und wird für jeden Matrixlauf auf dem festen Eval-Split ausgeführt. Details
stehen in
[EXPERIMENT_MATRIX_PLAN.md](docs/EXPERIMENT_MATRIX_PLAN.md).

Die automatisierte Testmatrix liegt unter
[tools/run_experiment_matrix.sh](tools/run_experiment_matrix.sh) und führt jede
konfigurierte Variante bei allen drei Auflösungen aus:

- `720p`: 1280×720
- `qhd`: 960×540
- `low`: 640×360

Vor jedem Matrixlauf wird das Rohvideo unverändert gelassen und ein eigenes
Arbeitsvideo erzeugt. Standardmäßig werden beide zeitlichen Profile getestet:
5 FPS und 2 FPS (`MATRIX_FPS_LIST=5,2`). Innerhalb jedes Profils verwenden die
Auflösungsvergleiche denselben Frame-Rhythmus; die native FPS-Zahl des
Rohvideos wird nicht unbeabsichtigt in die Testreihe übernommen.
Der Matrix-Standardprompt ist `pipe`; ein anderer Begriff kann explizit über
`MATRIX_PROMPT` gesetzt werden.

Nach SAM3 wird die Maskenabdeckung über alle Frames geprüft. Standardmäßig
bricht die Matrix bei mindestens 30 % leeren oder fehlenden `middle`-Masken ab
(`MATRIX_MAX_EMPTY_MASK_FRACTION=0.30`). Der Coverage-Report wird im jeweiligen
Experimentarchiv gespeichert.

#### Smoke-Test und Replay eines archivierten Laufs

`matrix_smoke_low_pipe_full` war ein einzelner Low-Resolution-Integrationstest
(`pipe`, 5 FPS, 640×360, `SIMPLE_RADIAL`, Variante A), nicht die vollständige
24er-Matrix. „Smoke“ bedeutet hier: die Übergaben zwischen SAM3, COLMAP, STS
und SuGaR mit einem kleinen, reproduzierbaren Lauf prüfen, bevor alle Varianten
gerechnet werden. `full` bedeutet nur, dass dieser einzelne Versuch nicht im
`--mask-only`-Modus beendet wurde.

Der archivierte Lauf kann ohne erneute Berechnung von SAM3, COLMAP oder STS für
SuGaR wiederhergestellt werden:

```bash
./tools/restore_matrix_replay.sh \
  data/10_runs/matrix_smoke_low_pipe_full/5fps/low/simple_radial_a
```

Das Skript kopiert nur ideale Masken, ideale COLMAP-Bilder, Sparse-Metadaten,
STS-Kameradaten, den vollständigen STS-Ply, den hochopaken STS-Ply und
`eval_frames.txt`; Rohdaten, HF-Cache und das Archiv bleiben unverändert.
Damit sind anschließend auch Rendern und objektmaskierte Metriken möglich.
Danach kann der A-Mesh-Replay mit
`AUTOPILOT=true`, `SUGAR_MESH_MODE=original_gs` und
`STOP_AFTER_COARSE_MESH=1` ausgeführt werden. Der Replay ist ein Neustart an
der SuGaR-Schrittgrenze, kein Fortsetzen innerhalb eines abgebrochenen
Trainingsprozesses.

Der frühere Fehler `CamerasWrapper([])` entstand, weil SuGaRs `cameras.json`
Bildnamen wie `00000` und der feste Split Namen wie `00000.jpg` enthielt. Die
aktuelle Implementierung normalisiert Basename/Stems, verwendet bei Bedarf die
numerische Frame-ID und protokolliert die Split-Kardinalitäten. Der erfolgreiche
Replay bestätigte 30 Test- und 210 Trainingskameras.

Die Varianten stehen in [tools/experiment_matrix.tsv](tools/experiment_matrix.tsv).
Eine Vorschau ohne Pipelineausführung ist mit
`./tools/run_experiment_matrix.sh --dry-run` möglich. Die Matrix arbeitet
sequenziell, archiviert jeden Lauf unter `data/10_runs/<batch>/` und verwendet
vor dem nächsten Versuch den nichtinteraktiven Modus von
[clean_data_interactive.sh](clean_data_interactive.sh). Rohdaten,
`data/01_raw/output.mp4` und `data/hf_cache` werden dabei nicht gelöscht.

### Centerline and GIS export

Container E reads the refined OBJ and performs a real DGtal voxelization,
interior fill, and topology-preserving thinning. On noisy thin meshes the
voxel skeleton is bushy (2D medial sheets and spur twigs), so the default
`CENTERLINE_MODE=single` deliberately reduces the largest skeleton component
to its diameter path, which robustly follows the structure. The postprocessing
then fits a clamped degree-10 B-spline to the unsplit path. Corner detection is
kept only as an optional experiment; it is disabled for the current smooth
linear-object route. The postprocessing step writes:

- `data/07_centerline/centerline_local_raw.csv` for the raw diameter path.
- `data/07_centerline/centerline_local.csv` for the degree-10 B-spline-smoothed
  centerline path.
- `data/08_gis/local_output.geojson` for the local (pre-georeferencing) 3D GeoJSON.
- `data/07_centerline/centerline_utm.csv` and `data/08_gis/final_output.geojson`
  after the CloudCompare transform and anchor are applied (EPSG:25832).
  If `matrix.txt`/`anchor.txt` are missing, a translation-only fallback
  (default UTM 567028.563, 5516784.082, 177) produces
  `centerline_fallback_georeferenced.csv` and
  `final_output_fallback_georeferenced.geojson` instead.

Georeferencing runs at the END of the step (after the local GeoJSON). If
`matrix.txt` is missing but `data/01_raw/matrix_screenshot.png` exists,
tesseract OCR runs automatically to produce `matrix.txt`. The fallback
anchor is configurable via `FALLBACK_ANCHOR`.

All CSV rows carry `branch_id` and `component_id`. Tunables:
`BSPLINE_DEGREE=10` sets the degree of the clamped uniform B-spline for the
current smooth linear-object route. `BSPLINE_SAMPLES_PER_SEGMENT=4` controls
the point density. `SEGMENT_CORNERS=0` keeps the extracted path as one smooth
curve; corner detection remains available for experiments. `MIN_PATH_LENGTH`,
`MIN_PATH_POINTS`, `MIN_CYCLE_LENGTH` and `PERSISTENCE` are extractor-side
filters.

`CENTERLINE_MODE=network` instead decomposes the full skeleton graph into
junction-to-junction branches. On noisy meshes most of those micro-branches
fall below `MIN_PATH_LENGTH=0.75`, which can leave an empty result. The
extractor flag `--one-isthmus` (1D-only thinning) and
`src/python/centerline_graph_simplify.py` (spur pruning, junction clustering,
chain merging) exist for experiments in that direction.

The matrix must be saved as `data/04_sfm/matrix.txt`, and
`src/python/prepare_gcp.py` creates `data/01_raw/anchor.txt` from the GCP CSV.
Postprocessing fails explicitly when either input or the mesh is missing; it no
longer creates empty placeholder files.
After changing the C++ extractor or Container E image, rebuild it with
`docker compose build post-processing` before running the pipeline.

The project keeps a pinned SuGaR checkout in `third_party/SuGaR`. The runner
automatically applies `docker-compose.sugar-dev.yml`, which mounts that local
checkout over `/opt/sugar` in the existing SuGaR container. Thus changing the
local fork needs neither a fresh clone nor an image rebuild during development.
After validation, the same tracked source can be baked into the Docker image
for a release build.

For a focused Coarse-mesh extraction from an existing completed run, use:

```bash
SOURCE_RUN_TAG=masked_7000_dn_consistency_medium \
COARSE_MESH_ABLATION_TAG=depth8_v50000 \
MESH_VERTICES=50000 \
POISSON_DEPTH=8 \
./tools/run_coarse_mesh_ablation.sh
```

This does not retrain SuGaR and does not run refinement, UV baking, or crop.
The default source checkpoint is preserved and every ablation requires a new
output tag. To run a new full Coarse optimization but stop immediately after
the resulting Coarse mesh, set `STOP_AFTER_COARSE_MESH=1` on
`run_masked_sugar.sh`.

To test the hypothesis that the object-specific STS Gaussians are already good
enough and that SuGaR's Coarse optimization changes them unfavorably, use the
same extractor directly on the private staged STS PLY:

```bash
SOURCE_RUN_TAG=library_i7000_c9000_v200000 \
COARSE_MESH_ABLATION_TAG=original_gs_projected_depth10 \
USE_ORIGINAL_GS=True \
USE_GAUSSIAN_DEPTH=False \
SURFACE_SAMPLE_SEED=42 \
MESH_VERTICES=200000 \
SURFACE_SAMPLE_COUNT=5000000 \
POISSON_DEPTH=10 \
PROJECT_MESH_ON_SURFACE_POINTS=True \
./tools/run_coarse_mesh_ablation.sh
```

This is the same coarse-mesh route used by the production default. It skips
SuGaR Coarse training and still performs the surface sampling, Poisson
reconstruction, density cleanup, decimation, and optional vertex projection. Set
`USE_GAUSSIAN_DEPTH=True` for the comparison that obtains the surface depth
directly from the Gaussian rasterizer instead of SuGaR's projected diamond-mesh
z-buffer. If the direct-original-GS mesh is clean while the c9000 mesh is not,
the coarse optimization is the likely cause. If both are similarly noisy, the
problem is downstream in surface sampling, rasterization, Poisson, density
cleanup, decimation, or vertex projection.

The former full SuGaR route remains available with
`SUGAR_MESH_MODE=sugar_coarse` in `run_masked_sugar.sh` or the master pipeline.

`SURFACE_SAMPLE_SEED` is optional. Use the same non-negative integer for all
variants of a controlled ablation; leaving it empty preserves the historical
stochastic sampling behavior. The seed controls the random camera-sample
selection during extraction, not the SuGaR training checkpoint.
`INCLUDE_BACKGROUND_MESH=False` is a separate object-only diagnostic for
testing whether sparse samples outside the foreground camera bounding box are
responsible for artifacts; the historical/default behavior remains `True`.

`run_pipeline.sh --from sugar` now asks for the SuGaR parameters unless
Autopilot is explicitly selected. Choosing `STOP_AFTER_COARSE_MESH=1` also
ends that replay after the Coarse mesh instead of attempting post-processing
without a refined OBJ.

To crop an already exported textured SuGaR OBJ without retraining, run:

```bash
./run_multiview_crop.sh
```

This uses the existing `sugar-meshing` service and needs no additional
container. The default pass preserves faces with insufficient observations;
review its JSON report before using more aggressive crop options. For an already
dense full-scene mesh, use `CROP_PROFILE=semantic-core` to retain only faces
with semantic support and remove unobserved faces. It writes a separate
`*_semantic_core.obj` result and never replaces the conservative output.

---

## Directory Reference
For a complete breakdown of directories and build caching, refer to the [recommended_structure.md](file:///C:/Users/4567r/.gemini/antigravity-ide/brain/0d83ae5b-3ce6-4d35-b202-67437f7ecc10/recommended_structure.md) design artifact.
