from opentrons import protocol_api

# -----------------------------
# Metadata: shown in Opentrons App
# -----------------------------
metadata = {
    'protocolName': 'Example_script_standard',
    'author': 'Aske Unger',
    'description': "A script for mixing cells and media",
    'apiLevel': '2.8'
}

def run(protocol: protocol_api.ProtocolContext):
    """
    Main protocol execution function.
    This protocol:
    1) Dispenses media into a destination plate
    2) Transfers cells from a source plate into the same destination plate
    """

    # -----------------------------
    # Labware setup
    # -----------------------------

    # Tip racks
    # One rack dedicated to media dispensing to avoid cross-contamination
    cells_tips = protocol.load_labware('opentrons_96_tiprack_20ul', '1')
    media_tips = protocol.load_labware('opentrons_96_tiprack_300ul', '11')

    # Containers
    # 12-channel reservoir holding minimal media
    media_reservois = protocol.load_labware('nest_12_reservoir_15ml', '10')

    # 96-well source plate containing cells
    source = protocol.load_labware('corning_96_wellplate_360ul_flat', '2')

    # 96-well destination plate where media + cells will be combined
    destination = protocol.load_labware('corning_96_wellplate_360ul_flat', '3')

    # -----------------------------
    # Pipette setup
    # -----------------------------

    # Multichannel P300 mounted on the left
    p300 = protocol.load_instrument('p300_single_gen2', mount='left')
    p20 = protocol.load_instrument('p20_single_gen2', mount='right')

    # -----------------------------
    # Step 1: Fill destination plate with minimal media
    # -----------------------------

    # Pick up a fresh tip for all media dispensing
    p300.pick_up_tip(media_tips['A1'])

    # Pre-mix the reservoir well to ensure homogeneous media
    p300.mix(4, 160, media_reservois['A1'])

    # Dispense 160 µL of media into each well of the destination plate
    # range(96) gives i = 0..95, matching wells()[0]..wells()[95] exactly
    for i in range(96):
        p300.aspirate(160, media_reservois['A1'])
        p300.dispense(160, destination.wells()[i])

    # Discard the media tip after use
    p300.drop_tip()

    # -----------------------------
    # Step 2: Transfer cells from source plate to destination plate
    # -----------------------------

    # Loop over each well to transfer cells individually
    # A new tip is used for each well to prevent cross-contamination
    for i in range(96):
        # wells()[i] ensures a fresh, unused tip each time
        p20.pick_up_tip(cells_tips.wells()[i])

        # Mix cells in the source well to resuspend them evenly
        p20.mix(4, 20, source.wells()[i])

        # Aspirate cells from the source plate
        p20.aspirate(5, source.wells()[i])

        # Dispense cells into the corresponding destination well
        p20.dispense(5, destination.wells()[i])

        # Dispose of the tip after each transfer
        p20.drop_tip()