import os

import pandas as pd
from dotenv import load_dotenv

from app.models.gigachat import GigaChatBased, get_credentials
from app.utils.submit import generate_submit

if __name__ == "__main__":
    load_dotenv()

    system_prompt = """
    Ты — профессиональный программист и ментор. Твоя задача — помогать студентам находить ошибки в их коде, направляя их к правильному решению, указывая на конкретные ошибки, допущенные студентом. Ты не раскрываешь прямое решение или закрытые тесты. Учитывай как открытые, так и закрытые тесты.
    """
    
    giga_client_id = os.environ['GIGACHAT_CLIENT_ID']
    giga_key = os.environ['GIGACHAT_CLIENT_SECRET']
    giga_creds = get_credentials(giga_client_id, giga_key)

    gigachat = GigaChatBased(
        credentials=giga_creds,
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False,
        system_prompt=system_prompt,
    )

    def predict(user_data: dict) -> str:
        return gigachat.ask(user_data)


    generate_submit(
        data_path="data/raw/test",
        predict_func=predict,
        save_path="data/processed/submission.csv",
        use_tqdm=True,
    )
