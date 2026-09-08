# E. coli Transformation and Recovery

Source: [Opentrons Protocol Library](https://library.opentrons.com/p/ecoli-transformation-recovery)

## Why This Is Useful

Transformation links DNA assembly to living bacterial strains. This is a readable example of a semi-automated workflow where the robot handles liquid transfers while timed manual interventions remain explicit.

## What The Protocol Does

The OT-2 combines competent E. coli cells with plasmid DNA, supports heat-shock handling through temperature-controlled deck positions, adds recovery medium, and pauses when the operator needs to move labware or complete off-deck handling.

## Automation Setup

| Item | Details |
| --- | --- |
| Robot | OT-2 |
| Protocol type | Python |
| Library category | Education |
| Verification | Opentrons education protocol |
| Pipette | P300 single-channel |
| Modules | Two Temperature Module GEN2 units |
| Labware | 300 uL tip rack, NEST snapcap tube aluminum block, Falcon tube rack, two NEST well plate aluminum blocks |

## Workflow Interpretation

| Level | Mapping |
| --- | --- |
| DBTL stage | Build |
| Workflow | Bacterial transformation and recovery |
| Unit operations | Combine cells and DNA, temperature-controlled incubation, add recovery medium, manual pause/handoff |
| Reusable idea | Make manual timing and labware movement visible in the protocol rather than hiding it in operator memory |

## Before Running

- Confirm the competent-cell handling protocol for the strain being used.
- Pre-chill compatible blocks and labware when required.
- Verify antibiotic and recovery-medium identity before loading the deck.
- Treat this as a template: transformation conditions may need strain- and plasmid-specific tuning.
