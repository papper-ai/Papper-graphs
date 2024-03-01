import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from src.config import settings

CUDA_IS_AVAILABLE = torch.cuda.is_available()

tokenizer = AutoTokenizer.from_pretrained("src/model/rut5-REBEL-base") if settings.lm_mode == 'local' else AutoTokenizer.from_pretrained("memyprokotow/rut5-REBEL-base")
model = AutoModelForSeq2SeqLM.from_pretrained("src/model/rut5-REBEL-base") if settings.lm_mode == 'local' else AutoTokenizer.from_pretrained("memyprokotow/rut5-REBEL-base")

if CUDA_IS_AVAILABLE:
    model.to("cuda")
