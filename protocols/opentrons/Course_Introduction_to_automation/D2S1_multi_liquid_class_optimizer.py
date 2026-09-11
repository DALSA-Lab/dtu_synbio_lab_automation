from opentrons import protocol_api

metadata = {
    'protocolName': 'Liquid class tester with plate reader',
    'author': 'Aske Unger',
    'description': "Transfers a colored-liquid volume series (p20 + p300), pre-filled with "
                    "water (p300) so every destination well ends at the same total volume — "
                    "useful for building a standard curve on a plate reader. Mixing is left "
                    "to the plate reader's shake step, not performed on-deck"
                    "Fill source plate with 1: your liquid, 2/3: Water",
    'apiLevel': '2.8'
}

# -----------------------------
# Liquid classes (modifiable)
# -----------------------------
# Three separate classes, keyed by role rather than pipette alone:
#   - "p20"        : colored liquid, low-volume range
#   - "p300"       : colored liquid, high-volume range
#   - "water_p300" : water fill, always via p300
# Kept separate so tuning the colored-liquid behavior (p20/p300) never
# accidentally changes how the water fill step behaves, even though
# water_p300 runs on the same physical pipette as "p300".

##Leading and trailing airgaps, prewet added
LIQUID_CLASSES = {
    "p20": {
        "aspirate_rate": 7,       # µL/s - conservative for p20 multi gen2
        "dispense_rate": 7,         
        "touch_tip": False,        #Touch plate sides to remove liquid
        "blow_out": False          #Blow out to remove liquid
    },
    "p300": {
        "aspirate_rate": 150,     # µL/s
        "dispense_rate": 300,
        "touch_tip": False,
        "blow_out": False
    },
    "water_p300": {
        "aspirate_rate": 150,     # µL/s - independent of "p300" above by design
        "dispense_rate": 300,
        "touch_tip": False,
        "blow_out": False
    }
}

def apply_liquid_class(pipette, liquid_class):
    """
    Apply liquid class flow rates to a pipette.
    """
    pipette.flow_rate.aspirate = liquid_class["aspirate_rate"]
    pipette.flow_rate.dispense = liquid_class["dispense_rate"]
    pipette.flow_rate.blow_out = liquid_class["dispense_rate"]


def run(protocol: protocol_api.ProtocolContext):

    # -----------------------------
    # Labware setup
    # -----------------------------
    tips_p20 = protocol.load_labware('opentrons_96_tiprack_20ul', '10')
    tips_p300 = protocol.load_labware('opentrons_96_tiprack_300ul', '11')

    # Single 12-well reservoir supplies BOTH liquids from fixed positions:
    #   A1 = colored liquid (source for p20 + p300 volume series)
    #   A2/A3 = water (source for the volume-normalizing fill)
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', '1')

    destination = protocol.load_labware('corning_96_wellplate_360ul_flat', '2')

    # -----------------------------
    # Pipette setup
    # -----------------------------
    p20 = protocol.load_instrument('p20_multi_gen2', mount='left')
    p300 = protocol.load_instrument('p300_multi_gen2', mount='right')

    # -----------------------------
    # Volume series
    # -----------------------------
    # Columns 1-6  -> p20  (low-volume range)
    # Columns 7-12 -> p300 (high-volume range)
    p20_volumes = [1, 3, 5, 10, 15, 20]
    p300_volumes = [30, 50, 80, 100, 150, 200]
    all_volumes = p20_volumes + p300_volumes  # index 0 = column 1, ... index 11 = column 12

    TARGET_TOTAL_VOLUME = 200  # µL - final volume in every destination well

    # -----------------------------
    # Step 1: Water fill (p300) — done FIRST so colored liquid lands on
    # top of the water rather than the other way around.
    # Water volume per well = TARGET_TOTAL_VOLUME - colored liquid volume,
    # so every well ends up at the same total (200 µL) regardless of how
    # much colored liquid it later receives.
    # -----------------------------
    water_class = LIQUID_CLASSES["water_p300"]
    apply_liquid_class(p300, water_class)

    # Single tip for the whole water fill: pure water dispensed into
    # empty wells carries no cross-contamination risk, so one tip
    # across all 12 columns is fine and saves tips.
    p300.pick_up_tip(tips_p300['A2'])

    for col in range(1, 13):
        water_vol = TARGET_TOTAL_VOLUME - all_volumes[col - 1]

        if water_vol <= 0:
            # Column 12 (p300 @ 200 µL) needs no water — skip a 0 µL dispense
            continue
        if col<7:
            position_reservois='A2'
        else: 
            position_reservois='A3'
        p300.aspirate(water_vol, reservoir[position_reservois])
        p300.dispense(water_vol, destination[f'A{col}'])

        if water_class["blow_out"]:
            p300.blow_out(destination[f'A{col}'])

    p300.drop_tip()

    # -----------------------------
    # Step 2: p20 colored liquid transfers (columns 1-6)
    # Source is always reservoir A1 (single position).
    # Same tip reused across all 6 columns since volume only increases —
    # no risk of small-volume residue skewing a later larger draw.
    # -----------------------------
    p20_class = LIQUID_CLASSES["p20"]
    apply_liquid_class(p20, p20_class)

    p20.pick_up_tip(tips_p20['A1'])
    for idx, vol in enumerate(p20_volumes):
        col = idx + 1

        p20.aspirate(vol, reservoir['A1'])
        p20.dispense(vol, destination[f'A{col}'])

        if p20_class["touch_tip"]:
            p20.touch_tip(destination[f'A{col}'])  # touches the side of the well
        if p20_class["blow_out"]:
            p20.blow_out(destination[f'A{col}'])

    p20.drop_tip()

    # -----------------------------
    # Step 3: p300 colored liquid transfers (columns 7-12)
    # Source is always reservoir A1 (single position).
    # -----------------------------
    p300_class = LIQUID_CLASSES["p300"]
    apply_liquid_class(p300, p300_class)

    p300.pick_up_tip(tips_p300['A1'])
    for idx, vol in enumerate(p300_volumes):
        col = idx + 7  # destination column: 7-12

        p300.aspirate(vol, reservoir['A1'])
        p300.dispense(vol, destination[f'A{col}'])

        if p300_class["touch_tip"]:
            p300.touch_tip(destination[f'A{col}'])
        if p300_class["blow_out"]:
            p300.blow_out(destination[f'A{col}'])

    p300.drop_tip()
    #-----------------------------
    # A final pipetting step going from low to high concentration using 300µL pipette to mix the wells in the destination plate. 
    # This is done to ensure that the liquid is well mixed before reading the plate.
    #-----------------------------
    p300.pick_up_tip(tips_p300['A2'])
    for col in range(1, 13):
        p300.mix(3, 100, destination[f'A{col}'])
    p300.drop_tip()