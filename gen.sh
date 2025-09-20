#!/bin/bash
#BEFORE RUNNING IT, RUN ON TERMINAL ----> chmod +x run.sh

HF_TOKEN="YOUR-API-TOKEN-HERE"
TEMPS="0.3 0.5 0.7"

MODEL_ID="mistralai/Mistral-7B-Instruct-v0.3"
OUTPUT_PATH="MISTRAL-8X7b/"
python scripts/essayGeneration/gen.py --model_id $MODEL_ID --hf_token $HF_TOKEN --temps $TEMPS --output_path $OUTPUT_PATH

MODEL_ID="microsoft/Phi-3-small-8k-instruct"
OUTPUT_PATH="PHI-3-SMALL/"
python scripts/essayGeneration/gen.py --model_id $MODEL_ID --hf_token $HF_TOKEN --temps $TEMPS --output_path $OUTPUT_PATH

MODEL_ID="google/gemma-2-9b-it"
OUTPUT_PATH="GEMMA-9b/"
python scripts/essayGeneration/gen.py --model_id $MODEL_ID --hf_token $HF_TOKEN --temps $TEMPS --output_path $OUTPUT_PATH

MODEL_ID="Qwen/Qwen2.5-7B-Instruct"
OUTPUT_PATH="QWEN2-7b/"
python scripts/essayGeneration/gen.py --model_id $MODEL_ID --hf_token $HF_TOKEN --temps $TEMPS --output_path $OUTPUT_PATH

MODEL_ID="meta-llama/Llama-3.1-8B-Instruct"
OUTPUT_PATH="LLAMA-8b/"
python scripts/essayGeneration/gen.py --model_id $MODEL_ID --hf_token $HF_TOKEN --temps $TEMPS --output_path $OUTPUT_PATH