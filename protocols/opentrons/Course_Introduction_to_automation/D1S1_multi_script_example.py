from opentrons import protocol_api

# -----------------------------
# Metadata: shown in Opentrons App
# -----------------------------
metadata = {
    'protocolName': 'Example_script_multipipette',
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
    # 12-channel reservoir holding media
    media_reservois = protocol.load_labware('nest_12_reservoir_15ml', '10')

    # 96-well source plate containing cells
    source = protocol.load_labware('corning_96_wellplate_360ul_flat', '2')

    # 96-well destination plate where media + cells will be combined
    destination = protocol.load_labware('corning_96_wellplate_360ul_flat', '3')

    # -----------------------------
    # Pipette setup
    # -----------------------------

    # Multichannel P300 mounted on the left
    p300 = protocol.load_instrument('p300_multi_gen2', mount='right')
    p20 = protocol.load_instrument('p20_multi_gen2', mount='left')

    # -----------------------------
    # Step 1: Fill destination plate with media
    # -----------------------------

    # Pick up a fresh tip for all media dispensing
    p300.pick_up_tip(media_tips)

    # Pre-mix the reservoir well to ensure homogeneous media
    p300.mix(4, 160, media_reservois['A1'])

    # Dispense 195 µL of media into each well of row A (columns 1–6)
    for i in range(1, 7):
        p300.aspirate(195, media_reservois['A1'])
        p300.dispense(195, destination[f'A{i}'])

    # Discard the media tip after use
    p300.drop_tip()

    # -----------------------------
    # Step 2: Transfer cells from source plate to destination plate
    # -----------------------------

    # Loop over each column to transfer cells individually
    # A new tip is used for each column to prevent cross-contamination
    for i in range(1, 7):
        p20.pick_up_tip(cells_tips)

        # Mix cells in the source well to resuspend them evenly
        p20.mix(4, 20, source[f'A{i}'])

        # Aspirate cells from the source plate
        p20.aspirate(5, source[f'A{i}'])

        # Dispense cells into the corresponding destination well
        p20.dispense(5, destination[f'A{i}'])

        # Dispose of the tip after each transfer
        p20.drop_tip()
