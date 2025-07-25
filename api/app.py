import os
import cv2
import matplotlib.pyplot as plt

from ultralytics import YOLO
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})

model_path = "../yolo_model/e50_b64_m50_ship_detection_categorized_25_balance_40.pt"
model = YOLO(model_path)

# POST image_name
@app.route('/predict', methods=['POST'])
def predict():
    request_data = request.get_json()

    if not request_data or 'image_name' not in request_data:
        return jsonify({"error": "Missing 'image_name' in request"}), 400

    image_name = request_data['image_name']

    image_path = os.path.join("../images/uploads", image_name)

    results = model.predict(
        source=image_path,
        imgsz=768,
        conf=0.25,
        save=False # Bounding boxes drawn manually
    )

    image = cv2.imread(image_path)

    result = results[0]
    boxes = result.boxes

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = float(box.conf[0])
        label = f"({i+1}) ship {conf:.2f}"

        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)

    result_image_path = os.path.join("../images/predict_result", image_name)
    cv2.imwrite(result_image_path, image)

    centerCoords = []
    for result in results:
        for box in result.boxes.xyxy:
            x1, y1, x2, y2, = box.numpy()
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            centerCoords.append([round(center_x, 3), round(center_y, 3)])

    response =  jsonify({"result": "OK", "result_path": result_image_path, "center_coords": centerCoords})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Access-Control-Allow-Methods", "POST")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

if __name__ == '__main__':
    app.run(debug=True)