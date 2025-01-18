from yandex_cloud_ml_sdk import YCloudML
import os

YA_FOLDER = os.getenv('YA_FOLDER')
YA_TOKEN = os.getenv('YA_TOKEN')
TEMPERATURE = 0.3

sdk = YCloudML(
    folder_id=YA_FOLDER,
    auth=YA_TOKEN
)

model = sdk.models.completions("yandexgpt")
model = model.configure(temperature=TEMPERATURE)

def generate_text(prompt, context):
    request = [{"role": "system", "text":context},{"role": "user", "text": prompt}]
    response = model.run(request)
    text = response.alternatives[0].text
    return text

if __name__ == "__main__":
    txt = generate_text("Назови два обычных для России имени и их этимологию", " ")
    print(txt)