# Motion Detector

Motion Detector - мини проект для детекции движения с веб-камеры или видеофайла с возможностью сохранения клипов, в которых зафиксировано движение.

Проект использует **OpenCV** для обработки видеопотока, сохраняет фрагменты с движением в папку `output/`, логирует события в `logs/events.log` и предоставляет минимальный **Flask API** для мониторинга статуса.

---

## Структура проекта
motion_detector/
├─ api/
│ └─ app.py 
├─ detector/
│ ├─ motion_detector.py
│ └─ utils.py
├─ logs/ 
├─ output/ 
├─ main.py # Основной скрипт запуска
├─ requirements.txt 
└─ Dockerfile 

---

## Локальный запуск

git clone <https://github.com/Davidmasle/motion_detector.git>
cd motion_detector

docker build -t motion_detector:latest .

docker run --rm -it \
  --device /dev/video0:/dev/video0 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/output:/app/output \
  -p 5000:5000 \
  motion_detector:latest


Flask API
Доступен на http://localhost:5000

/ - возвращает статус проекта

/status - последняя запись о движении из логов
