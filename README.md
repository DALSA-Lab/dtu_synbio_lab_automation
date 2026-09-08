# DTU Synbio Lab Automation

![DTU_BIOENGINEERING_SYNBIO_PIC](references/syn_biopic.png)

Automation protocols, robot guides, and reusable unit operations for synthetic biology workflows at DTU.

This repository is the working home for lab automation code that is clear enough for scientists to review, structured enough for developers to maintain, and explicit enough for reliable robot execution.

## At a Glance

| Area | What belongs here |
| --- | --- |
| `protocols/opentrons/` | Robot-ready Opentrons protocols. |
| `unit_operations/` | Reusable liquid-handling and workflow building blocks. |
| `workflows/` | Workflow descriptions mapped to DBTL stages. |
| `guides/robots/` | Robot setup, calibration, run, and troubleshooting guides. |
| `labware/` | Custom or validated labware definitions. |
| `data/raw/` | Original input data. |
| `data/interim/` | Intermediate working data. |
| `data/processed/` | Cleaned or analysis-ready data. |
| `data/external/` | Third-party reference data. |
| `notebooks/` | Analysis, planning, and workflow-development notebooks. |
| `src/` | Python helpers for data handling, protocol generation, validation, and analysis. |
| `docs/` | Longer documentation built with Sphinx or similar tooling. |
| `references/` | Figures, papers, diagrams, and supporting material. |

## Quickstart

Install:

- Git: <https://git-scm.com/install>
- VS Code: <https://code.visualstudio.com/download>

Clone:

```bash
git clone https://github.com/DALSA-Lab/dtu_synbio_lab_automation.git
cd dtu_synbio_lab_automation
```

Set up Python dependencies with `uv`:

```bash
uv sync
uv run python test_environment.py
```

Simulate every Opentrons protocol before robot use:

```bash
uv run opentrons_simulate protocols/opentrons/<protocol>.py
```

## Workflow Abstraction

The repository follows the hierarchy described in:

> **Abstraction hierarchy to define biofoundry workflows and operations for interoperable synthetic biology research and applications**  
> Nature Communications 16, Article 6056 (2025)  
> <https://www.nature.com/articles/s41467-025-61263-6>

| Level | Name | In this repo |
| --- | --- | --- |
| 0 | Project | Scientific objective or campaign. |
| 1 | Service/Capability | Automation capability offered by the lab. |
| 2 | Workflow | Goal-oriented experimental procedure. |
| 3 | Unit Operation | Executable robot or software action. |

Opentrons protocols should be documented at the **workflow level** and implemented as clear, reusable **unit operations**. Workflows should be mapped to the Design-Build-Test-Learn cycle when relevant.

## Capabilities

| Capability | Examples |
| --- | --- |
| Liquid handling | Transfers, aliquoting, normalization, reagent distribution. |
| Plate setup | Plate maps, controls, standards, randomized layouts. |
| Serial dilution | Gradients, calibration curves, assay preparation. |
| Culture handling | Media addition, inoculation, induction, sampling. |
| DNA assembly setup | Golden Gate or Gibson-style reaction setup. |
| Assay preparation | Reporter assays, growth assays, enzyme assays. |
| Instrument handoff | Thermocycler, incubator, shaker, plate reader, centrifuge. |
| Data workflows | Plate map joins, QC, run metadata, downstream exports. |

## Workflows and Unit Operations

Suggested workflow ID:

```text
W-<DBTL>-<number>-<short-name>
```

Example workflows:

| Workflow ID | Name | Stage |
| --- | --- | --- |
| `W-BUILD-001-dna-assembly-setup` | DNA assembly reaction setup | Build |
| `W-BUILD-002-culture-inoculation` | Culture inoculation | Build |
| `W-TEST-001-serial-dilution` | Serial dilution | Test |
| `W-TEST-002-assay-plate-setup` | Assay plate setup | Test |
| `W-LEARN-001-plate-data-qc` | Plate data quality control | Learn |

Core unit operations:

`load_labware`, `transfer`, `distribute`, `consolidate`, `mix`, `serial_dilution`, `normalize`, `pause_handoff`, `incubate`, `export_metadata`

## Clean Opentrons Code

Good automation code is explicit, readable, and hard to misuse.

- Write around biological intent, not only robot commands.
- Separate deck setup, input parsing, calculations, validation, and execution.
- Use descriptive names for reagents, labware, wells, and workflow steps.
- Keep volumes, labware names, module names, and flow-rate assumptions visible.
- Validate inputs before moving liquid.
- Make tip use, dead volume, mix volume, and manual pauses intentional.
- Simulate before running on real samples.

Recommended protocol shape:

```python
from opentrons import protocol_api

metadata = {
    "protocolName": "Example workflow",
    "author": "DTU Synbio Lab Automation",
    "description": "Short workflow-level description.",
}

requirements = {"robotType": "OT-2", "apiLevel": "2.20"}


def run(protocol: protocol_api.ProtocolContext) -> None:
    deck = load_deck(protocol)
    plan = build_liquid_handling_plan()
    validate_plan(plan, deck)
    execute_plan(protocol, deck, plan)
```

## Robot Guides

Robot-specific guides live in `guides/robots/` and should cover:

- Setup and startup checks.
- Calibration and labware positioning.
- Protocol upload and simulation.
- Run monitoring and cleanup.
- Known failures and troubleshooting.

Suggested guides:

- `guides/robots/opentrons-ot2.md`
- `guides/robots/opentrons-flex.md`
- `guides/robots/plate-reader.md`
- `guides/robots/thermocycler.md`

## Repository Structure

```text
.
|-- README.md
|-- references/
|-- guides/
|   |-- robots/
|   `-- workflows/
|-- protocols/
|   |-- opentrons/
|   `-- shared/
|-- workflows/
|-- unit_operations/
|-- labware/
|-- data/
|   |-- raw/
|   |-- interim/
|   |-- processed/
|   `-- external/
|-- notebooks/
|-- src/
|-- docs/
|-- reports/
|-- tests/
`-- pyproject.toml
```

## Safety

Before running a protocol on real samples, confirm the deck layout, labware definitions, reagent identities, volumes, pipette compatibility, module settings, and simulation result. New or modified workflows should be reviewed by both an automation developer and a trained lab operator.

## Citation

Kim, H., Hillson, N.J., Cho, B.-K. et al. **Abstraction hierarchy to define biofoundry workflows and operations for interoperable synthetic biology research and applications.** *Nature Communications* 16, 6056 (2025). <https://doi.org/10.1038/s41467-025-61263-6>
