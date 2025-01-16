import openai
import base64
import random
import os
from django.conf import settings

def generate_image(keyword):
    client = openai.Client(api_key=settings.GPT_API_KEY)
    
    try:
        response = client.images.generate(
                    model="dall-e-3",
                    prompt=f"{keyword} 그림 그려줘. 플랫 디자인 스타일로, 배경은 흰색으로 그려줘.",
                    n=1,
                    size="1024x1024",
                    response_format="b64_json"
                    )

        print(response.data[0].url)

        # Base64 인코딩된 이미지 데이터를 가져옵니다.
        b64_json = response.data[0].b64_json

        # Base64 문자열을 디코딩합니다.
        image_data = base64.b64decode(b64_json)

        # 파일로 저장합니다.
        # current_directory = os.path.dirname(os.path.abspath(__file__))
        # image_path = os.path.join(current_directory, f"resources/images/image{random.randrange(10000, 99999)}.png")
        image_path = settings.IMAGE_DIR / f"image{random.randrange(10000, 99999)}.png"

        with open(image_path, "wb") as file:
            file.write(image_data)

        return str(image_path)
    except openai.BadRequestError as e:
        print(e)
        return None


def generate_keyword_from_diary(diary_content):
    client = openai.Client(api_key=settings.GPT_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"다음 일기에서 제일 중요한 단어 1개를 구체적으로 요약해줘. 스티커를 생성할거니까 일기 속의 흐름과 맥락을 반영하여 형용사+명사 or 동사+명사 형식으로 나타내줘. /*예) 산책 나간 강아지*/ : {diary_content}"}
            ]
        )

        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except openai.BadRequestError as e:
        print(e)


if __name__ == "__main__":
    generate_image(generate_keyword_from_diary("오늘은 날씨가 좋아서 산책을 나갔다."))