import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from src.config import settings

use_cuda = torch.cuda.is_available() and settings.use_cuda

# Download the model
tokenizer = AutoTokenizer.from_pretrained("memyprokotow/rut5-REBEL-base")
model = AutoModelForSeq2SeqLM.from_pretrained("memyprokotow/rut5-REBEL-base")

if use_cuda:
    model.to("cuda")
