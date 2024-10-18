from app.models.base import BaseModel

from typing import Optional
import base64
import requests
import os

from langchain_community.chat_models import GigaChat
from langchain.schema import HumanMessage, SystemMessage

from app.utils.anonimize import delete_comments

def get_promts(task: str, student_code: str, author_code: str, tests: str):
  student_code_without_comments = delete_comments(student_code)
  #anonymized_student_code = anonymize_code(code_without_comments)

  author_code_without_comments = delete_comments(author_code)
  #anonymized_author_code = anonymize_code(code_without_comments)

  promts = []
  promt = f"""Дана задача, код студента, и тесты (открытые и закрытые). Объясни, какие тесты не проходят и в чём может быть ошибка в коде. Не раскрывай детали закрытых тестов и не предлагай конкретное решение. Опиши логику ошибки в 2-3 предложениях.  Отвечай коротко.

Задача:
{task}
Решение студента:
```python
{student_code_without_comments}
```
Предполагаемое правильное решение:
```python
{author_code_without_comments}
```
Входные данные:
{tests}"""
  promts.append(promt)

  promt = """
Дай краткую подсказку, которая поможет студенту самостоятельно найти и исправить ошибку. Сосредоточься на логике задачи, избегая упоминания конкретных кодовых строк или закрытых тестов. Ответь одним предложением, выделив аспект, на который нужно обратить внимание, учитывая тип логической ошибки. Отвечай коротко.
"""
  promts.append(promt)
  promt = """
Дай краткую подсказку, которая поможет студенту самостоятельно найти и исправить ошибку. Сосредоточься на логике задачи, избегая упоминания конкретных строк кода или закрытых тестов. В ответе нельзя использовать код или данные с тестов. Ответь одним предложением, выделяя аспект, на который нужно обратить внимание. Пиши простым, понятным языком. Дай указания мне, как студенту.
Если была допущена логическая ошибка, нужно добавить в начала сообщения либо '', либо '', в зависимости от того, на каких тестах была допущена ошибка.
Вот примеры формулировок:
Обратите внимание …
Вы забыли… (в случае синтаксической ошибки)
Проверьте…
В данном случае…
"""
  promts.append(promt)
  return promts

def get_credentials(giga_client_id: str, giga_key: str):
    credentials = f"{giga_client_id}:{giga_key}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return encoded_credentials


class GigaChatBased(BaseModel):
    def __init__(
        self,
        credentials: str,
        scope: str,
        verify_ssl_certs: bool,
        system_prompt: Optional[str] = None,
    ) -> None:
        super().__init__(system_prompt)
        
        self.model = GigaChat(
            credentials=credentials,
            scope="GIGACHAT_API_PERS",
            model="GigaChat",
            verify_ssl_certs=verify_ssl_certs,
        )
        self.system_prompt = system_prompt
        self.messages = []


    def ask(self, user_data: dict) -> Optional[str]:
        promts = [HumanMessage(content=promt_text) for promt_text in get_promts(**user_data)]

        history = [
            SystemMessage(
                content=self.system_prompt
            )
        ]

        for promt in promts:
            history.append(promt)
            res = self.model.invoke(history)
            history.append(res)
        
        return history[-1].content


