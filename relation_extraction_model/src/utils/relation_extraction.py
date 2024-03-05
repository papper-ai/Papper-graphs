import logging
import math

import torch

from src.model.model import CUDA_IS_AVAILABLE, model, tokenizer


# from https://huggingface.co/Babelscape/rebel-large
def extract_relations_from_model_output(text: str) -> list:
    relations = []
    relation, subject, relation, object_ = "", "", "", ""
    text = text.strip()
    current = "x"
    text_replaced = text.replace("<s>", "").replace("<pad>", "").replace("</s>", "")
    for token in text_replaced.split():
        if token == "<triplet>":
            current = "t"
            if relation != "":
                relations.append(
                    {
                        "head": subject.strip(),
                        "type": relation.strip(),
                        "tail": object_.strip(),
                    }
                )
                relation = ""
            subject = ""
        elif token == "<subj>":
            current = "s"
            if relation != "":
                relations.append(
                    {
                        "head": subject.strip(),
                        "type": relation.strip(),
                        "tail": object_.strip(),
                    }
                )
            object_ = ""
        elif token == "<obj>":
            current = "o"
            relation = ""
        else:
            if current == "t":
                subject += " " + token
            elif current == "s":
                object_ += " " + token
            elif current == "o":
                relation += " " + token
    if subject != "" and relation != "" and object_ != "":
        relations.append(
            {"head": subject.strip(), "type": relation.strip(), "tail": object_.strip()}
        )
    return relations


def run_relation_extraction(text: str) -> list:
    span_length = 256

    inputs = tokenizer([text], return_tensors="pt")

    # Compute span boundaries
    num_tokens = len(inputs["input_ids"][0])
    num_spans = math.ceil(num_tokens / span_length)
    overlap = math.ceil((num_spans * span_length - num_tokens) / max(num_spans - 1, 1))
    spans_boundaries = []
    start = 0

    logging.info(f"Started running relation extraction on {num_tokens} token text")

    for i in range(num_spans):
        spans_boundaries.append(
            [start + span_length * i, start + span_length * (i + 1)]
        )
        start -= overlap

    # Transform input with spans
    tensor_ids = [
        inputs["input_ids"][0][boundary[0] : boundary[1]]
        for boundary in spans_boundaries
    ]
    tensor_masks = [
        inputs["attention_mask"][0][boundary[0] : boundary[1]]
        for boundary in spans_boundaries
    ]

    if CUDA_IS_AVAILABLE:
        inputs = {
            "input_ids": torch.stack(tensor_ids).to("cuda"),
            "attention_mask": torch.stack(tensor_masks).to("cuda"),
        }
    else:
        inputs = {
            "input_ids": torch.stack(tensor_ids),
            "attention_mask": torch.stack(tensor_masks),
        }

    # Generate relations
    num_return_sequences = 5
    gen_kwargs = {
        "max_length": span_length,
        "length_penalty": 0,
        "num_beams": 5,
        "num_return_sequences": num_return_sequences,
    }

    # Generate relations in batches
    batch_size = 8  # Choose an appropriate batch size that fits in the GPU memory
    for batch_start in range(0, len(tensor_ids), batch_size):
        batch_end = min(batch_start + batch_size, len(tensor_ids))

        if CUDA_IS_AVAILABLE:
            batch_inputs = {
                "input_ids": torch.stack(tensor_ids[batch_start:batch_end]).to("cuda"),
                "attention_mask": torch.stack(tensor_masks[batch_start:batch_end]).to(
                    "cuda"
                ),
            }
        else:
            batch_inputs = {
                "input_ids": torch.stack(tensor_ids[batch_start:batch_end]),
                "attention_mask": torch.stack(tensor_masks[batch_start:batch_end]),
            }

        with torch.no_grad():
            batch_generated_tokens = model.generate(
                **batch_inputs,
                **gen_kwargs,
            ).cpu()

        # Decode relations
        batch_decoded_preds = tokenizer.batch_decode(
            batch_generated_tokens, skip_special_tokens=False
        )

        # Process decoded relations
        for i, sentence_pred in enumerate(batch_decoded_preds):
            current_span_index = (batch_start + i) // num_return_sequences
            current_span_input_ids = tensor_ids[current_span_index]
            current_span_text = tokenizer.decode(
                current_span_input_ids, skip_special_tokens=True
            )
            relations = extract_relations_from_model_output(sentence_pred)
            for relation in relations:
                relation["meta"] = {
                    "information": current_span_text  # Here we use the actual text of the span
                }

    logging.info(f"Finished running relation extraction on {num_tokens} token text")

    return relations
