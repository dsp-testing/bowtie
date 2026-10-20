FROM python:3.16.0a1-alpine
RUN python -m pip install jsonschema
COPY lintsonschema /usr/local/bin
COPY schemas /schemas
CMD ["/usr/local/bin/lintsonschema"]
