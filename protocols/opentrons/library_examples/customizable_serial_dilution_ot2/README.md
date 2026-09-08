# Customizable Serial Dilution for OT-2

Source: [Opentrons Protocol Library](https://library.opentrons.com/p/customizable_serial_dilution_ot2)

## Why This Is Useful

Serial dilution is one of the cleanest starter workflows for automation. It appears in growth assays, standard curves, antimicrobial testing, viable-count workflows, inducer titration, and concentration-response experiments.

## What The Protocol Does

The OT-2 prepares a dilution series across a 96-well plate. The protocol calculates transfer volumes from the dilution factor and total mixing volume, then performs repeated transfer and mixing steps across the plate.

## Automation Setup

| Item | Details |
| --- | --- |
| Robot | OT-2 |
| Protocol type | Python with Liquid Properties |
| Library category | General Liquid Handling |
| Verification | Opentrons verified |
| Pipette | P300 single-channel |
| Modules | None |
| Labware | NEST 12-well reservoir, NEST 96-well flat plate, two 300 uL tip racks |

## Workflow Interpretation

| Level | Mapping |
| --- | --- |
| DBTL stage | Test |
| Workflow | Serial dilution plate preparation |
| Unit operations | Load diluent, transfer sample, mix, repeat dilution, track final concentration |
| Reusable idea | Encode dilution math once, then reuse it across assays with different sample maps |

## Before Running

- Confirm the dilution factor, total mixing volume, and final assay volume.
- Check pipette limits for each calculated transfer.
- Preload samples and diluent according to the deck map.
- Include blank and positive controls when the dilution plate feeds an assay.
