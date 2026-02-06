## NLLB

NLLB is a collection of multilingual models trained by Meta and supporting 200
languages. See here for the list of accepted language codes.

The example below uses the smallest version with 600M parameters.

> Important Converting NLLB models requires `transformers>=4.21.0`.

```bash
uv run ct2-transformers-converter --model facebook/nllb-200-distilled-600M --output_dir nllb-200-distilled-600M
```

```python
import ctranslate2
import transformers

src_lang = "eng_Latn"
tgt_lang = "fra_Latn"

translator = ctranslate2.Translator("nllb-200-distilled-600M")
tokenizer = transformers.AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", src_lang=src_lang)

source = tokenizer.convert_ids_to_tokens(tokenizer.encode("Hello world!"))
target_prefix = [tgt_lang]
results = translator.translate_batch([source], target_prefix=[target_prefix])
target = results[0].hypotheses[0][1:]

print(tokenizer.decode(tokenizer.convert_tokens_to_ids(target)))
```

Bron : https://opennmt.net/CTranslate2/guides/transformers.html#nllb
