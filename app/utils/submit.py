from typing import Callable

import pandas as pd
import torch
from transformers import BertModel, BertTokenizer

print("Loading models...", end="")
model_name = "DeepPavlov/rubert-base-cased-sentence"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)
print("OK")


def get_sentence_embedding(sentence: str) -> torch.Tensor:
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state[:, 0, :].squeeze()
    return embedding


def string2embedding(string: str) -> torch.Tensor:
    return torch.Tensor([float(i) for i in string.split()])


def embedding2string(embedding: torch.Tensor) -> str:
    return " ".join([str(i) for i in embedding.tolist()])


def generate_submit(data_path: str, predict_func: Callable, save_path: str, use_tqdm: bool = True) -> None:
    df_solutions = pd.read_excel(f'{data_path}/solutions.xlsx')
    df_tasks = pd.read_excel(f'{data_path}/tasks.xlsx')
    df_tests = pd.read_excel(f'{data_path}/tests.xlsx')

    bar = range(len(df_solutions))
    if use_tqdm:
        import tqdm
        bar = tqdm.tqdm(bar, desc="Predicting")

    submit_df = pd.DataFrame(columns=["solution_id", "author_comment", "author_comment_embedding"])

    for i in bar:
        idx = df_solutions.index[i]
        solution_row = df_solutions.iloc[i]

        student_code = solution_row['student_solution']
        task_id = solution_row['task_id']

        task_row = df_tasks.loc[df_tasks['id'] == task_id]
        if task_row.empty:
            print(f"Task with id {task_id} not found.")
            continue
        task = task_row['description'].values[0]
        author_code = task_row['author_solution'].values[0]

        tests = df_tests[df_tests['task_id'] == task_id]

        user_data = {
            'task': task,
            'student_code': student_code,
            'author_code': author_code,
            'tests': tests
        }

        try:
            text = predict_func(user_data)
            if not text:
                print(f"Empty comment generated for solution id {idx}")
                continue

            embedding = embedding2string(get_sentence_embedding(text))
            submit_df.loc[i] = [idx, text, embedding]

        except Exception as e:
            print(f"Error during prediction for solution id {idx}: {e}")
            continue

        submit_df.to_csv(save_path, index=False)
    submit_df.to_csv(save_path, index=False)
