FROM python:3.15.0b3-alpine
RUN python -m pip install jsonschema
COPY lintsonschema /usr/local/bin
COPY schemas /schemas
CMD ["/usr/local/bin/lintsonschema"]
