import asyncio
import json
import time
import torch
from pydantic import ValidationError
from transformers import AutoTokenizer, AutoModelForCausalLM

from backend.config import settings
from backend.models.schemas import ModulationSchedule
from backend.llm_engine.prompts import build_schedule_prompt
from backend.llm_engine.fallbacks import get_fallback_schedule
from backend.llm_engine.validator import parse_llm_response

MAX_RETRIES = 2


class LLMEngine:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    async def load(self):
        #Called once during app lifespan startup — runs blocking load in executor
        print(f"Loading {settings.hf_model_id} on {self.device}...")
        start = time.time()

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._load_model)

        elapsed = time.time() - start
        print(f"Model loaded in {elapsed:.1f}s on {self.device}")

    def _load_model(self):
        #Synchronous model loading — called via run_in_executor
        self.tokenizer = AutoTokenizer.from_pretrained(settings.hf_model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            settings.hf_model_id,
            torch_dtype=torch.float16,
            device_map="auto",
        )

    def generate_schedule(self, intent: str, duration_minutes: int = 25) -> ModulationSchedule:
        #Synchronous inference — called from async endpoint via run_in_executor
        prompt = build_schedule_prompt(intent, duration_minutes)

        messages = [{"role": "user", "content": prompt}]
        input_text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.device)

        last_error = None
        for attempt in range(MAX_RETRIES + 1):
            start = time.time()
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=settings.llm_max_new_tokens,
                    temperature=settings.llm_temperature,
                    top_p=0.95,
                    do_sample=True,
                )
            inference_time = time.time() - start
            print(f"LLM inference took {inference_time:.2f}s (attempt {attempt + 1})")

            # Decode only new tokens (skip input)
            new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
            raw_output = self.tokenizer.decode(new_tokens, skip_special_tokens=True)

            try:
                return parse_llm_response(raw_output)
            except json.JSONDecodeError as e:
                last_error = e
                print(f"LLM JSON parse failed (attempt {attempt + 1}): {e}")
            except ValidationError as e:
                last_error = e
                print(f"LLM validation failed (attempt {attempt + 1}): {e}")

        print(f"All retries exhausted, using fallback. Last error: {last_error}")
        print(f"Raw output (first 500 chars): {raw_output[:500]}")
        return get_fallback_schedule(intent, duration_minutes)


# Singleton
llm_engine = LLMEngine()
