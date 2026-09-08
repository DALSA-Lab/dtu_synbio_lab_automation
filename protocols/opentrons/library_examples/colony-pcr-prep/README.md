# Colony PCR Preparation

Source: [Opentrons Protocol Library](https://library.opentrons.com/p/colony-pcr-prep)

## Why This Is Useful

Colony PCR is a common test-stage screen after bacterial or fungal transformation. This protocol is short, educational, and helpful as a first example of automating PCR reaction preparation.

## What The Protocol Does

The OT-2 dispenses assembled PCR master mix into strip tubes held on a Temperature Module. DNA samples are added manually, making the protocol useful for teaching how automation can prepare standardized reactions while leaving biological sampling under operator control.

## Automation Setup

| Item | Details |
| --- | --- |
| Robot | OT-2 |
| Protocol type | Python |
| Library category | Education |
| Verification | Opentrons education protocol |
| Pipette | P20 single-channel |
| Modules | Temperature Module GEN2 |
| Labware | PCR strip tube aluminum block, NEST snapcap tube aluminum block, 20 uL filter tip rack |

## Workflow Interpretation

| Level | Mapping |
| --- | --- |
| DBTL stage | Test |
| Workflow | Colony PCR reaction setup |
| Unit operations | Cool reagent block, distribute master mix, pause for manual template addition |
| Reusable idea | Keep assay setup reproducible while preserving manual checkpoints for colony selection |

## Before Running

- Confirm primer pairs, control wells, and expected amplicon sizes.
- Keep master mix cold and minimize time on deck.
- Ensure the plate or strip-tube map matches the colony picking record.
- Simulate after editing wells, volumes, or labware.
