metadata = {
    "protocolName": "Parameterized CSV Example",
    "author": "Aske",
    "description": "Example of CSV integration with Opentrons",
    "apiLevel": "2.20",
}

########################################################################
# Parameter definitions
########################################################################
LIQUID_CLASSES = {
    "water": {
        "aspirate_rate": 150,
        "dispense_rate": 300,
        "blow_out_rate": 300,
    },
    "glycerol": {
        "aspirate_rate": 40,
        "dispense_rate": 80,
        "blow_out_rate": 100,
    }
}


def add_parameters(parameters):

    # CSV file defining cherrypicking instructions
    parameters.add_csv_file(
        variable_name="cherrypicking_parameters",
        display_name="Cherrypicking parameters",
        description=(
            "CSV with three columns: "
            "source well, destination well, and volume (µL)"
        )
    )

    # Number of destination (aliquot) plates to load
    parameters.add_int(
        variable_name="plates_added",
        display_name="Number of plates",
        description="Number of destination plates to process",
        default=1,
        minimum=1,
        maximum=7,
    )

    # Liquid class
    parameters.add_str(
        variable_name="liquid_class",
        display_name="Liquid class",
        description="Select the liquid class",
        choices=[
            {"display_name": "Water", "value": "water"},
            {"display_name": "Glycerol", "value": "glycerol"},
        ],
        default="water",
    )
########################################################################
# Protocol execution
########################################################################

def run(protocol):
    # ------------------------------------------------------------------
    # Read parameters
    # ------------------------------------------------------------------
    # Parse CSV file
    csv_data = protocol.params.cherrypicking_parameters.parse_as_csv()

    # Extract columns (skip header row)
    source_wells = [row[0] for row in csv_data][1:]
    dest_wells   = [row[1] for row in csv_data][1:]
    volumes_ul   = [row[2] for row in csv_data][1:]

    
    plates = int(protocol.params.plates_added)

    #Add liquid classes

    liquid_class = protocol.params.liquid_class

    rates = LIQUID_CLASSES[liquid_class]

    aspirate_rate = rates["aspirate_rate"]
    dispense_rate = rates["dispense_rate"]
    blow_out_rate = rates["blow_out_rate"]

    # ------------------------------------------------------------------
    # Load labware
    # ------------------------------------------------------------------

    # Source plate (slot 1)
    source_plate = protocol.load_labware(
        "corning_96_wellplate_360ul_flat",
        location=4
    )

    # Destination (aliquot) plates (slots 2+)
    destination_plates = [
        protocol.load_labware(
            "corning_96_wellplate_360ul_flat",
            location=i + 5
        )
        for i in range(plates)
    ]

    # Tip rack
    tiprack_20 = protocol.load_labware(
        "opentrons_96_tiprack_20ul",
        location=11
    )

    # ------------------------------------------------------------------
    # Load instrument
    # ------------------------------------------------------------------

    p20 = protocol.load_instrument(
        "p20_multi_gen2",
        mount="left",
        tip_racks=[tiprack_20]
    )
    p20.flow_rate.aspirate = aspirate_rate
    p20.flow_rate.dispense = dispense_rate
    p20.flow_rate.blow_out = blow_out_rate
    # ------------------------------------------------------------------
    # Cherrypicking procedure
    # ------------------------------------------------------------------

    p20.pick_up_tip(tiprack_20.wells()[95])

    for plate in destination_plates:
        for src, dst, vol in zip(source_wells, dest_wells, volumes_ul):
            p20.aspirate(vol, source_plate[src])
            p20.dispense(vol, plate[dst])


    p20.drop_tip()
