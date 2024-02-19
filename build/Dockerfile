ARG   PYTHON_IMAGE="python:3-alpine"
FROM  ${PYTHON_IMAGE}
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
#COPY main.json   ./main.json
COPY main.py     ./main.py
ENTRYPOINT ["python", "-u", "main.py"]
