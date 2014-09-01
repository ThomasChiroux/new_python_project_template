{{ "=" * (cookiecutter.repo_name|length + 13) }}
{{cookiecutter.repo_name}} documentation
{{ "=" * (cookiecutter.repo_name|length + 13) }}

Contents:

.. toctree::
    :maxdepth: 5
    :numbered:
    :glob:

    source_doc/{{cookiecutter.repo_name}}
    todo


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

