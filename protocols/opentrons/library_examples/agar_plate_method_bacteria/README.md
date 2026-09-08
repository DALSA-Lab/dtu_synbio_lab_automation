# Automated Agar Plate Method for Viable Bacteria Assessment

Source: [Opentrons Protocol Library](https://library.opentrons.com/p/agar_plate_method_bacteria)

Downloaded script: [`BacteriaInoculation_Flex_6plates.py`](BacteriaInoculation_Flex_6plates.py)

## Why This Is Useful

Viable-count workflows are directly relevant to bacterial strain characterization, culture QC, and growth-condition screening. This protocol is a more advanced example than a simple dilution, but still maps clearly to everyday microbiology operations.

## What The Protocol Does

The Flex prepares ten-fold bacterial dilutions, dispenses droplets onto rectangular agar plates, uses a tilting adapter to spread droplets, and prompts the operator to move plates for incubation.

## Automation Setup

| Item | Details |
| --- | --- |
| Robot | Flex |
| Protocol type | Python with Liquid Properties |
| Library category | Cell and Tissue Culture |
| Verification | Opentrons verified |
| Pipettes | Flex 8-channel 50 uL, Flex 1-channel 1000 uL |
| Modules | Heater-Shaker Module GEN1, custom tilting adapter |
| Labware | NEST 96 deep-well plate, Flex tip racks, NEST conical tube rack, OmniTray-style agar plates |

## Workflow Interpretation

| Level | Mapping |
| --- | --- |
| DBTL stage | Test |
| Workflow | Viable bacteria assessment by agar spotting |
| Unit operations | Serial dilution, droplet spotting, plate tilt/spread, incubation handoff |
| Reusable idea | Combine liquid handling with mechanical plate handling while keeping incubation as a tracked handoff |

## Before Running

- Confirm access to the required tilting adapter and compatible rectangular agar plates.
- Validate sample count, dilution scheme, and medium-only controls.
- Check contamination-control practices for open agar handling.
- Review every prompt in simulation before running live cultures.
