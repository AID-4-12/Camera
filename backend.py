from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

# JSON 파일 경로 설정
json_file_path = "main.json"

# JSON 파일에서 데이터를 로드하는 함수
def load_json():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return {}

# JSON 파일에 데이터를 저장하는 함수
def save_json(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file)

# lat와 lon을 저장하는 API 엔드포인트
@app.put("/set/{lat}/{lon}")
def set(lat: float, lon: float):
    # JSON 파일에서 데이터를 로드
    data = load_json()
    
    # `lat`과 `lon` 쌍이 이미 데이터에 존재하는지 확인
    existing_entry = any(entry["lat"] == lat and entry["lon"] == lon for entry in data.values())
    
    if existing_entry:
        # `lat`과 `lon` 쌍이 이미 존재하면 추가하지 않고 메시지를 반환
        return {"message": "Lat and Lon already exist, skipping."}
    
    # 새로운 데이터의 인덱스는 기존 데이터의 길이
    index = len(data)

    # 전달된 `lat`와 `lon`을 딕셔너리로 저장
    data[index] = {"lat": lat, "lon": lon}

    # JSON 파일에 데이터를 저장
    save_json(data)

    # 성공적으로 저장되었음을 확인
    return {"message": "Data saved successfully"}


# 모든 데이터를 불러오는 API 엔드포인트
@app.get("/get")
def get_all_data():
    # JSON 파일에서 데이터를 로드
    data = load_json()

    # 데이터를 리스트로 변환하여 반환
    markers_list = list(data.values())
    return markers_list

# 특정 인덱스 또는 모든 데이터를 삭제하는 API 엔드포인트
@app.delete("/set/{index}")
def set_del(index: str):
    # JSON 파일에서 데이터를 로드
    data = load_json()

    # 요청된 인덱스가 "*"인 경우 모든 데이터를 삭제
    if index == "*":
        data = {}  # 모든 데이터를 삭제
        save_json(data)  # JSON 파일에 빈 데이터를 저장
        return {"message": "All data deleted successfully"}

    # 요청된 인덱스가 숫자일 경우 해당 인덱스의 데이터를 삭제
    try:
        index = int(index)
        if index in data:
            del data[index]  # 해당 인덱스의 데이터 삭제
            # 남아있는 데이터의 인덱스를 재정렬
            data = {idx: data[key] for idx, key in enumerate(data)}
            # JSON 파일에 업데이트된 데이터를 저장
            save_json(data)
            return {"message": f"Data at index {index} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Index not found")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid index format")
