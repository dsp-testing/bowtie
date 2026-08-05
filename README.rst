======
Bowtie
======

.. image:: ./docs/_static/dreamed.png
  :alt: Bowtie
  :target: https://pypi.org/project/bowtie-json-schema/
  :align: center
  :width: 250px

|

.. image:: https://zenodo.org/badge/531839193.svg
  :alt: DOI
  :target: https://zenodo.org/badge/latestdoi/531839193

.. image:: https://img.shields.io/pypi/v/bowtie-json-schema.svg
  :alt: PyPI version
  :target: https://pypi.org/project/bowtie-json-schema/

.. image:: https://img.shields.io/pypi/pyversions/bowtie-json-schema.svg
  :alt: Supported Python versions
  :target: https://pypi.org/project/bowtie-json-schema/

.. image:: https://github.com/bowtie-json-schema/bowtie/workflows/CI/badge.svg
  :alt: Build status
  :target: https://github.com/bowtie-json-schema/bowtie/actions?query=workflow%3ACI

.. image:: https://results.pre-commit.ci/badge/github/bowtie-json-schema/bowtie/main.svg
  :alt: pre-commit.ci status
  :target: https://results.pre-commit.ci/latest/github/bowtie-json-schema/bowtie/main

|

Bowtie is a *meta*-validator of the `JSON Schema specification <https://json-schema.org/>`_, by which we mean it coordinates executing *other* `validator implementations <https://json-schema.org/implementations.html>`_, collecting and reporting on their results.

To do so it defines a simple input/output protocol (specified in `this JSON Schema <https://github.com/bowtie-json-schema/bowtie/blob/main/bowtie/schemas/io.json>`_) which validator implementations can implement, and it provides a CLI which can execute supported implementations.

It's called Bowtie because it fans in lots of JSON then fans out lots of results: ``>·<``.
Looks like a bowtie, no?
Also because it's elegant – we hope.

For more information, see `Bowtie's documentation <https://docs.bowtie.report/>`_.

Bowtie Humor
------------

* Why did the JSON Schema break up with the YAML file? Too many trust issues – it just couldn't validate the relationship.
* What do you call a bowtie that fans in lots of schemas? Sharply dressed, and also very fast.
* Why don't JSON documents ever get lost? They always know their ``$schema``.
* An implementation walks into Bowtie and says "test me". Bowtie says, "sure, but only if you conform."

E também em português:

* Por que o JSON terminou com o XML? Porque ele queria uma relação mais leve, sem tantas tags.
* Qual é o schema favorito do brasileiro? O que aceita ``"additionalProperties": true``.
* Por que o validador foi ao psicólogo? Porque não conseguia parar de questionar tudo: "isso é ``required`` mesmo?"
