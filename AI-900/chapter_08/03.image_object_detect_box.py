import requests
import sys
import json
from PIL import Image, ImageDraw

# 상수로 subscription key와 endpoint를 정의합니다.
SUBSCRIPTION_KEY = "AtXfS5OQhfotXiriCGovxGE9CihH43cewGpjujg9FVtr6Z0UApYRJQQJ99BDACYeBjFXJ3w3AAAEACOGTe7o"
ENDPOINT = "https://ai-900-ai-service-001.cognitiveservices.azure.com/"

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

def detect_objects(image_path):
    detect_url = ENDPOINT.rstrip('/') + "/vision/v3.2/detect"
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
    
    response = requests.post(detect_url, headers=headers, data=image_data)
    if response.status_code != 200:
        print(f"오류 발생: {response.status_code} {response.text}")
        return None

    return response.json()

def annotate_and_display(image_path, detection_data):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"이미지 열기 실패: {e}")
        return

    draw = ImageDraw.Draw(image)
    for obj in detection_data.get("objects", []):
        rect = obj.get("rectangle")
        if rect:
            x = rect.get("x")
            y = rect.get("y")
            w = rect.get("w")
            h = rect.get("h")
            # 바운딩 박스를 빨간색으로 그립니다.
            draw.rectangle((x, y, x + w, y + h), outline="red", width=2)
            # 객체 라벨 표시 (객체 타입)
            label = obj.get("object", "object")
            draw.text((x, y - 10), label, fill="red")
    
    # 파일명을 변경하여 저장
    parts = image_path.rsplit(".", 1)
    if len(parts) == 2:
        annotated_path = f"{parts[0]}_annotated.{parts[1]}"
    else:
        annotated_path = image_path + "_annotated"
    
    image.save(annotated_path)
    print(f"Annotated image saved: {annotated_path}")
    image.show()

def main():
    image_path = input("이미지 경로를 입력하세요: ")

    print("1. 이미지 분석")
    print("2. 객체 감지")
    choice = input("원하는 작업을 선택하세요 (1 또는 2): ")

    if choice == '1':
        result = analyze_image(image_path)
        if result:
            print(json.dumps(result, indent=4))
    elif choice == '2':
        detection_result = detect_objects(image_path)
        if detection_result:
            annotate_and_display(image_path, detection_result)
    else:
        print("잘못된 선택입니다.")
        return

if __name__ == '__main__':
    main()