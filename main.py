from fastapi import FastAPI
import uvicorn
from g4f.client import Client
import g4f
import time
app = FastAPI()
client = Client()
Models_Image = [
    'flux-anime', # 18+ 10/10 ЕСТЬ ВОДЯНОЙ ЗНАК
    'flux-realism', # 18+ 10/10 ЕСТЬ ВОДЯНОЙ ЗНАК
    'flux-4o', # Нет знака. 8/10
]


@app.get("/GPT/{prompt}", tags=['Запрос чату гпт'], summary='chatGPT')
def generate_answer_gpt(prompt):
    response = g4f.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    ) 
    print(response)
    return(response)
    

@app.get("/GPT/Image/{Content}", tags=['Генерация изображений'])
def generate_image_gpt(Content):
    response = client.images.generate(model="flux", prompt=Content)
    image_url = response.data[0].url
    return image_url


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

