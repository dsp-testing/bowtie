FROM python:3.15.0a2-alpine
RUN python -m pip install jsonschema
COPY lintsonschema /usr/local/bin
COPY schemas /schemas
CMD ["/usr/local/bin/lintsonschema"]
