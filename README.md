# Svetofor
# Traffic Control Hackathon MVP

Программа для анализа видеопотока робота:
- детектирует светофор;
- распознает сигнал (RED / GREEN);
- детектирует желтую стоп-линию;
- выводит `STOP` или `GO!` только при приближении к стоп-линии.

## Стек
- Python 3.11+
- OpenCV
- NumPy

## Структура проекта
- `main.py` — точка входа
- `src/config.py` — HSV-пороги и параметры
- `src/services/detectors.py` — детекция светофора и стоп-линии
- `src/services/analyzer.py` — сглаживание сигнала и логика решения
- `src/application/processor.py` — обработка кадров и видео
- `src/domain/` — модели и enum'ы

## Установка
```bash
pip install -r requirements.txt
