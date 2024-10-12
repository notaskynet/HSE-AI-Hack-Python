from typing import Optional

from transformers import pipeline

from app.models.base import BaseModel


class Gemma(BaseModel):

    def __init__(self, model_name: str, token: str, device: str = "cuda", system_prompt: Optional[str] = None) -> None:
        super().__init__(system_prompt)
        self.pipe = pipeline("text-generation", model=model_name, device=device, token=token)

    def ask(self, user_message: str, clear_history: bool = True) -> Optional[str]:
        outputs = self.pipe(user_message, max_new_tokens=256)
        response = outputs[0]["generated_text"]
        return response
