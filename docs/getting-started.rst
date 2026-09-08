Getting Started
===============

This project uses ``uv`` for Python environment and dependency management.

Install the project dependencies from the repository root:

.. code-block:: bash

   uv sync

Run the environment check:

.. code-block:: bash

   uv run python test_environment.py

Run linting once protocol code has been added:

.. code-block:: bash

   uv run ruff check .

Simulate Opentrons protocols before robot use:

.. code-block:: bash

   uv run opentrons_simulate protocols/opentrons/<protocol>.py
