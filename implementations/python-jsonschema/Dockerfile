FROM python:3.13.5-alpine
WORKDIR /usr/src/myapp
RUN python -m pip install jsonschema
COPY bowtie_jsonschema.py .
CMD ["python3", "bowtie_jsonschema.py"]
