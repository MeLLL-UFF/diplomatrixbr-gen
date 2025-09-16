#!/bin/bash
#BEFORE RUNNING IT, RUN ON TERMINAL ----> chmod +x run.sh

HF_TOKEN="YOUR HUGGING FACE API KEY HERE"
TEMPS="0.3 0.5 0.7"

MODEL_ID="mistralai/Mistral-7B-Instruct-v0.3"
OUTPUT_PATH="mistral/"
python3 gen.py --model_id $MODEL_ID --hf_token $HF_TOKEN --temps $TEMPS --output_path $OUTPUT_PATH

MODEL_ID="microsoft/Phi-3-small-8k-instruct"
OUTPUT_PATH="phi/"
python3 gen.py --model_id $MODEL_ID --hf_token $HF_TOKEN --temps $TEMPS --output_path $OUTPUT_PATH

MODEL_ID="google/gemma-2-9b-it"
OUTPUT_PATH="gemma/"
python3 gen.py --model_id $MODEL_ID --hf_token $HF_TOKEN --temps $TEMPS --output_path $OUTPUT_PATH

MODEL_ID="Qwen/Qwen2.5-7B-Instruct"
OUTPUT_PATH="qwen/"
python3 gen.py --model_id $MODEL_ID --hf_token $HF_TOKEN --temps $TEMPS --output_path $OUTPUT_PATH

MODEL_ID="meta-llama/Llama-3.1-8B-Instruct"
OUTPUT_PATH="llama/"
python3 gen.py --model_id $MODEL_ID --hf_token $HF_TOKEN --temps $TEMPS --output_path $OUTPUT_PATH