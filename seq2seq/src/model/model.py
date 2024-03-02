import os

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

CUDA_IS_AVAILABLE = torch.cuda.is_available()

if not os.path.exists(local_model_directory := "src/model/rut5_REBEL_base"):
    # Download the model
    tokenizer = AutoTokenizer.from_pretrained("memyprokotow/rut5-REBEL-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("memyprokotow/rut5-REBEL-base")
else:
    tokenizer = AutoTokenizer.from_pretrained(local_model_directory)
    model = AutoModelForSeq2SeqLM.from_pretrained(local_model_directory)

if CUDA_IS_AVAILABLE:
    model.to("cuda")
