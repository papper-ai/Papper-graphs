from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Download the model
tokenizer = AutoTokenizer.from_pretrained("memyprokotow/rut5-REBEL-base")
model = AutoModelForSeq2SeqLM.from_pretrained("memyprokotow/rut5-REBEL-base")
model.to("cuda")
