from typing import Optional

from transformers import AutoModelForCausalLM, AutoTokenizer

from app.models.base import BaseModel


class Qwen(BaseModel):
    MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

    def __init__(
        self,
        system_prompt: Optional[str] = None,
        torch_dtype: str = "auto",
        device_map: str = "auto",
        max_new_tokens: int = 512,
    ) -> None:
        super().__init__(system_prompt)
        self.model = AutoModelForCausalLM.from_pretrained(
            Qwen.MODEL_NAME, torch_dtype=torch_dtype, device_map=device_map
        )
        self.tokenizer = AutoTokenizer.from_pretrained(Qwen.MODEL_NAME)
        self.messages = []
        self.max_new_tokens = max_new_tokens

    def ask(self, user_message: str, clear_history: bool = True) -> Optional[str]:
        if clear_history:
            self.messages = []
            if self.system_prompt:
                self.messages.append({"role": "system", "content": self.system_prompt})

        self.messages.append({"role": "user", "content": user_message})

        text = self.tokenizer.apply_chat_template(self.messages, tokenize=False, add_generation_prompt=True)
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(**model_inputs, max_new_tokens=self.max_new_tokens)
        generated_ids = [
            output_ids[len(input_ids) :] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response
