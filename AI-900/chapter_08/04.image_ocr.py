import requests
import sys
import json
import time
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

def read_image_ocr(image_path):
    read_url = ENDPOINT.rstrip('/') + "/vision/v3.2/read/analyze"
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
    
    response = requests.post(read_url, headers=headers, data=image_data)
    if response.status_code != 202:
        print(f"OCR 요청 실패: {response.status_code} {response.text}")
        return None

    # Operation-Location 헤더에 폴링할 URL이 포함됩니다.
    operation_url = response.headers.get("Operation-Location")
    if not operation_url:
        print("Operation-Location 헤더가 없습니다.")
        return None

    # 결과가 준비될 때까지 폴링 (최대 10회, 1초 간격)
    for _ in range(10):
        result_response = requests.get(operation_url, headers={'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY})
        result_json = result_response.json()
        status = result_json.get("status")
        if status == "succeeded":
            return result_json
        elif status == "failed":
            print("OCR 작업 실패")
            return None
        time.sleep(1)
    
    print("OCR 작업 시간이 초과되었습니다.")
    return None

def extract_text(ocr_result):
    if not ocr_result:
        return ""
    text_lines = []
    analyze_result = ocr_result.get("analyzeResult", {})
    read_results = analyze_result.get("readResults", [])
    for page in read_results:
        for line in page.get("lines", []):
            text_lines.append(line.get("text", ""))
    return "\n".join(text_lines)

def main():
    image_path = input("이미지 경로를 입력하세요: ")

    print("1. 이미지 분석")
    print("2. 객체 감지")
    print("3. OCR (텍스트 추출)")
    choice = input("원하는 작업을 선택하세요 (1, 2 또는 3): ")

    if choice == '1':
        result = analyze_image(image_path)
        if result:
            print(json.dumps(result, indent=4))
    elif choice == '2':
        detection_result = detect_objects(image_path)
        if detection_result:
            annotate_and_display(image_path, detection_result)
    elif choice == '3':
        ocr_result = read_image_ocr(image_path)
        if ocr_result:
            extracted_text = extract_text(ocr_result)
            print("추출된 텍스트:")
            print(extracted_text)
    else:
        print("잘못된 선택입니다.")
        return

if __name__ == '__main__':
    main()