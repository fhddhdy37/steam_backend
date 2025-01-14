import openai
import base64
import random
import os
from django.conf import settings

def get_image(keyword):
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


def get_keyword_from_diary():
    client = openai.Client(api_key=settings.GPT_API_KEY)
    
    diary_entry = """
    오늘은 오랜만에 가족과 함께 외출했다. 우리는 근처에 있는 박물관에 가기로 했고, 오전에 일찍 집을 나섰다. 박물관에 도착하자 다양한 전시물들이 눈에 들어왔다. 예술 작품, 고대 유물들, 그리고 현대 미술 전시까지 다양한 테마의 공간들이 있어 보는 내내 흥미로웠다. 가장 기억에 남는 전시물은 중세 시대의 유물들이었는데, 그 시기의 역사적 배경을 알 수 있어서 매우 유익했다.

박물관을 둘러본 후에는 근처의 공원으로 가서 간단한 피크닉을 즐겼다. 햇볕이 따뜻하고 바람도 시원해, 나무 그늘 아래에서 가족들과 함께 앉아 음식을 나누며 여유로운 시간을 보냈다. 아이들은 공원에서 뛰어놀며 즐거운 시간을 보냈고, 부모님과 나는 대화를 나누며 웃고 떠들었다.

저녁에는 맛있는 음식을 먹기 위해 근처의 맛집에 가기로 했다. 오랜만에 가족들과 함께 외식하니 기분이 정말 좋았다. 오늘 하루는 가족과 함께 소중한 추억을 쌓은 날이었고, 앞으로도 자주 이런 시간을 보내고 싶다는 생각이 들었다.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"다음 일기에서 제일 중요한 단어 1개를 구체적으로 요약해줘. 스티커를 생성할거니까 일기 속의 흐름과 맥락을 반영하여 형용사+명사 or 동사+명사 형식으로 나타내줘. /*예) 산책 나간 강아지*/ : {diary_entry}"}
            ]
        )

        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except openai.BadRequestError as e:
        print(e)


if __name__ == "__main__":
    get_image(get_keyword_from_diary())