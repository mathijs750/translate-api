from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ctranslate2
from transformers import AutoTokenizer
import logging


# Initialize App
app = FastAPI()

logger = logging.getLogger("uvicorn.error")

translator = ctranslate2.Translator(
    "models/nllb-200-distilled-600M", device="cpu"
)  # Use "cuda" if you have GPU nodes

tokenizer = AutoTokenizer.from_pretrained(
    "facebook/nllb-200-distilled-600M", clean_up_tokenization_spaces=True
)


class TranslateRequest(BaseModel):
    text: str


class TranslateResponse(BaseModel):
    original: str
    guesses: list[str]


@app.post("/translate", response_model=TranslateResponse)
async def translate_text(req: TranslateRequest):
    try:
        source = tokenizer.convert_ids_to_tokens(tokenizer.encode(req.text))

        # language codes https://github.com/facebookresearch/flores/blob/main/flores200/README.md#languages-in-flores-200
        target_prefix = ["nld_Latn"]

        results = translator.translate_batch(
            [source], target_prefix=[target_prefix], beam_size=5
        )
        hypotheses = results[0].hypotheses[:5]  # Get up to 5 hypotheses
        logger.info(f"Generated {len(hypotheses)} hypotheses")
        guesses = [
            tokenizer.decode(
                tokenizer.convert_tokens_to_ids(hypothesis[1:]),
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True,
            )
            for hypothesis in hypotheses
        ]

        return TranslateResponse(original=req.text, guesses=guesses)
    except Exception as e:
        logger.exception("Failed to translate text")
        raise HTTPException(status_code=500, detail=str(e))
