import requests
import sys
import json

# 상수로 subscription key와 endpoint를 정의합니다.
SUBSCRIPTION_KEY = "{SUBSCRIPTION_KEY}"
ENDPOINT = "{ENDPOINT}"

def analyze_image(image_path):
    analyze_url = ENDPOINT.rstrip('/') + "/vision/v3.2/analyze"
    # 분석 옵션 (카테고리, 설명, 색상 정보를 포함)
    params = {'visualFeatures': 'Categories,Description,Color'}
    headers = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Content-Type': 'application/octet-stream'
    }
    
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
    except Exception as e:
        print(f"이미지 파일 {image_path}을(를) 읽을 수 없습니다: {e}")
        sys.exit(1)
    
    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    if response.status_code != 200:
        print(f"오류 발생: {response.status_code} {response.text}")
        return None

    return response.json()

def main():
    image_path = input("이미지 경로를 입력하세요: ")

    result = analyze_image(image_path)
    if result:
        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()