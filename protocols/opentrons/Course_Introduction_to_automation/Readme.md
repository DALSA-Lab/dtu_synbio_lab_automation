
# Introduction to Automation

This folder contains small Opentrons examples used to introduce core concepts in laboratory automation. The examples progress from a fixed protocol, through single- and multichannel pipetting, to reusable protocols that accept runtime parameters and CSV input.
For teaching, write askung@dtu.dk. I have presentations for learning this but I am awaiting if this material is open source or not currently. 

## Learning path

Work through the examples in using either single or multichannel depending on your configuration:

1. `D1S1_single_script_example.py` demonstrates a single-channel P20 and P300 workflow. It fills a 96-well destination plate with media, then transfers cells from a source plate one well at a time.
2. `D1S1_multi_script_example.py` shows the same general workflow using multichannel P20 and P300 pipettes. It processes six columns instead of all 96 wells individually.
3. `D2S1_single_liquid_class_optimizer.py` introduces liquid classes. Use this with a plate reader to optimize the liquid classes for whatever you want. 
4. `D2S1_multi_liquid_class_optimizer.py` applies the same liquid-class idea to multichannel pipettes. It also demonstrates separate water source positions and optional pipetting behaviors such as touch-tip and blow-out.
5. `D4S1_single_parameter_inputs(recommended).py` is a starting point for parameterized protocols. It lets the operator select a CSV file, the number of destination plates, and a liquid class at run setup. With the example, the single channel is a bit more stable than the multichannel in its current configuration. 
6. `D4S1_multi_parameter_inputs.py` is the multichannel version of the parameterized protocol. Review the deck layout and well handling carefully before running it. There is some instability when grabbing one tip at a time. 

## File overview

| File | Purpose |
| --- | --- |
| `D1S1_single_script_example.py` | Fixed single-channel cell and media transfer example. |
| `D1S1_multi_script_example.py` | Fixed multichannel version processing six columns. |
| `D2S1_single_liquid_class_optimizer.py` | Single-channel liquid-class and standard-curve example. |
| `D2S1_multi_liquid_class_optimizer.py` | Multichannel liquid-class and standard-curve example. |
| `D4S1_single_parameter_inputs(recommended).py` | CSV-driven cherrypicking with a single-channel P20. |
| `D4S1_multi_parameter_inputs.py` | CSV-driven cherrypicking with a multichannel P20. |
| `D4_L1_task.csv` | Example sample-volume table with `Sample` and `Sampleamount` columns. |
| `D4_L1_task.xlsx` | Spreadsheet version of the D4/L1 task data. |

## CSV input for the parameterized protocols

The D4S1 protocols read the uploaded CSV by column position. The file must have a header row followed by rows containing:

```csv
Source,Destination,Liquid_added
A1,A1,12
A1,B1,15
A1,C1,10
```

The first column is the source well, the second is the destination well, and the third is the transfer volume in microliters. Volumes are read as strings by the current examples, so validate or convert input values before adapting the protocols for production use.

`D4_L1_task.csv` has a different layout and is not a direct input for the D4S1 protocols.

## Protocol assumptions

- The examples target Opentrons API `2.8` for D1 and D2, and API `2.20` for D4S1.
- The protocols use Opentrons standard labware, including Corning 96-well plates, NEST 12-well reservoirs, and 20 or 300 µL tip racks.
- The D1 examples use a reservoir in slot 10, source plate in slot 2, and destination plate in slot 3.
- The D2 examples build a 200 µL final-volume series across destination columns 1 to 12. Columns 1 to 6 use the P20 range; columns 7 to 12 use the P300 range.
- The D4S1 single-channel example loads its source plate in slot 1 and destination plates from slot 2 onward. The multichannel example uses source slot 4 and destination slots 5 onward.
- Confirm pipette type, deck slots, labware, tip strategy, liquid properties, and source volumes against the actual run before using samples.

## Simulation
If possible: 
Install the repository dependencies from the project root, then simulate a protocol before loading it on a robot:

```powershell
uv sync
uv run opentrons_simulate protocols/opentrons/Course_Introduction_to_automation/D1S1_single_script_example.py
```

Replace the filename to simulate another example. Parameterized protocols require the corresponding CSV file and runtime parameters to be supplied through the Opentrons App or an equivalent execution workflow; simulation alone does not replace checking those inputs.

If this doesnt work, the newest OT2 software can actually simulate from the app: 
https://opentrons.com/app

## Suggested exercises

- Change the number of wells or columns processed in the D1 examples.
- Compare the number of pipetting actions and tips used by the single- and multichannel versions.
- Tune the liquid classes in the D2 examples and compare the resulting liquid-handling behavior.
- Extend the D4S1 protocols with alternative inputs and play around with the parameters
- Keep the CSV format stable and document any new columns before adding them to a protocol.

These are teaching examples, not validated production protocols. Simulate them, inspect the generated commands, and verify the deck setup and liquid-handling assumptions before a real run.
