# Translate API

A lightweight, production-ready FastAPI service for multilingual translation
using Meta's NLLB-200 model with CTranslate2 optimization. Supports 200+
languages with an airgapped deployment model.

## Features

- **200+ Languages**: Supports all 200 languages from Meta's NLLB model
- **Performance Optimized**: Uses CTranslate2 for efficient CPU/GPU-based
  inference
- **Production Ready**: FastAPI with Uvicorn, Docker containerization
- **Beam Search**: Returns multiple translation hypotheses (up to 5) with
  confidence ranking
- **Airgapped**: Fully offline deployment capability after model initialization

## Local Development

1. **Clone and setup**:

```bash
git clone <repository-url>
cd translate-api
uv sync
source .venv/bin/activate
```

2. **Initialize the model** (first run only):

```bash
uv run ct2-transformers-converter \
  --model facebook/nllb-200-distilled-600M \
  --output_dir models/nllb-200-distilled-600M
```

3. **Run the API**:

```bash
uv run fastapi dev main.py
```

The API will be available at `http://localhost:8000` with interactive docs at
`http://localhost:8000/docs`.

## Development

## Docker Deployment

### Build

```bash
docker build -t translate-api:0.1.0 .
```

### Run

```bash
docker run -d \
  -p 8000:8000 \
  --name translation-service \
  translate-api:0.1.0
```

### Environment Variables

- `DEVICE`: Inference device (`cpu` or `cuda`). Default: `cpu`
  - Edit `main.py` to configure GPU support

### Performance Notes

- **CPU**: ~1-2s per request (600M model, single beam)
- **GPU (CUDA)**: ~200-400ms per request
- Models are cached in memory after first request

## Model Information

This project uses Meta's **NLLB-200-Distilled-600M** model:

- **Parameters**: 600M (smallest in the NLLB family)
- **Languages**: 200+ supported
- **Training Data**: FLORES-200 multilingual corpus
- **Optimization**: Compiled with CTranslate2 for production inference

**References**:

- [CTranslate2 NLLB Guide](https://opennmt.net/CTranslate2/guides/transformers.html#nllb)
- [NLLB Paper](https://arxiv.org/abs/2207.04672)
- [FLORES-200 Languages](https://github.com/facebookresearch/flores/blob/main/flores200/README.md)
