from opentrons import protocol_api

import csv
import json
import math


# --------(Modify) Copy and paste from excel data (1)
# Copy and paste excel green table
# Note that initial volume is in uL
csv_volume_data_raw = """
Labware	Initial_Wells	Initial_Volume	Liquid_Name	Description	Color
tube_rack_competent_cell	A1	180	competent cell	competent cell	#d9ead3
tube_rack_LB	A4	2000	LsLB+Amp	LsLB+Amp	#d9ead3
DNA_assembly_Plate	A1	10	DNA_Sample	DNA_Sample	#d9ead3
DNA_assembly_Plate	B1	10	DNA_Sample	DNA_Sample	#d9ead3
DNA_assembly_Plate	C1	10	DNA_Sample	DNA_Sample	#d9ead3
DNA_assembly_Plate	D1	10	DNA_Sample	DNA_Sample	#d9ead3
"""

# Copy and paste excel blue table
# Note that transfer_volume is in uL

csv_transfer_competent_cell_raw = """
Source_Labware	Source_Well	Destination_Labware	Destination_Well	Transfer_Volume	Pick_Up_Tip
tube_rack_competent_cell	A1	temp_PCR_tube	A1	15.0	TRUE
tube_rack_competent_cell	A1	temp_PCR_tube	B1	15.0	FALSE
tube_rack_competent_cell	A1	temp_PCR_tube	C1	15.0	FALSE
tube_rack_competent_cell	A1	temp_PCR_tube	D1	15.0	FALSE

"""

csv_transfer_golden_gate_mixture_raw = """
Source_Labware	Source_Well	Destination_Labware	Destination_Well	Transfer_Volume	Pick_Up_Tip
DNA_assembly_Plate	A1	temp_PCR_tube	A1	2.5	TRUE
DNA_assembly_Plate	B1	temp_PCR_tube	B1	2.5	TRUE
DNA_assembly_Plate	C1	temp_PCR_tube	C1	2.5	TRUE
DNA_assembly_Plate	D1	temp_PCR_tube	D1	2.5	TRUE

"""

csv_transfer_LB_raw = """
Source_Labware	Source_Well	Destination_Labware	Destination_Well	Transfer_Volume	Pick_Up_Tip
tube_rack_LB	A4	temp_PCR_tube	A1	150.0	TRUE
tube_rack_LB	A4	temp_PCR_tube	B1	150.0	FALSE
tube_rack_LB	A4	temp_PCR_tube	C1	150.0	FALSE
tube_rack_LB	A4	temp_PCR_tube	D1	150.0	FALSE

"""

#---------End of modifications (1)

csv_volume_data_raw = csv_volume_data_raw.replace('	', ',')
csv_transfer_competent_cell_raw = csv_transfer_competent_cell_raw.replace('	', ',')
#TELL MONI - didn't add this code for the golden gate csv. that's why there was a Keyerror
csv_transfer_golden_gate_mixture_raw = csv_transfer_golden_gate_mixture_raw.replace('	', ',')
csv_transfer_LB_raw = csv_transfer_LB_raw.replace('	', ',')
#ASK MONI - if this plate is needed. Error was that it isn't defined, since there is no csv for it above. Also it's never used again in the code
#csv_plate_Ecoli_culture_raw = csv_plate_Ecoli_culture_raw.replace('	', ',')


# Function that gets labware object to use given the string name of variable
def getLabwareObject(labware_dict, labware_name):
    for key, value in labware_dict.items():
        if str(key) == str(labware_name):
            return value
    return


#-------(Modify) Change name and description to suit your needs (2)
metadata = {
    "apiLevel": "2.16",
    "protocolName": "E.coli transformation and plating",
    "description": """Volume transfer program for E. coli transformation and plating""",
    "author": "Moni Qiande"
    }
#-------End of modifications (2)

#Protocol context - https://docs.opentrons.com/v2/tutorial.html
def run(protocol: protocol_api.ProtocolContext):

    #---------(Modify) Load the needed Modules, Labware, Tip racks, Pipettes  (3)

    # Loading modules

    # Load heating/cooling module and aluminum block
    # module_name = OT-2 module names (https://docs.opentrons.com/v2/new_modules.html#), location = slot num
    temp_mod1 = protocol.load_module(module_name="temperature module gen2", location="4")
    temp_mod1.set_temperature(celsius=4)
    
    temp_mod2 = protocol.load_module(module_name="temperature module gen2", location="3")
    temp_mod2.set_temperature(celsius=42)

    # Loading tip rack, after the api name, put comma and then which slot it is in on the Opentron
    tips = protocol.load_labware(load_name="opentrons_96_tiprack_300ul", location=9)
    # Loading pipette, 20uL single tip
    s300_pip = protocol.load_instrument(instrument_name="p300_single_gen2", mount="right", tip_racks=[tips])


    #-------(Modify) Define the starting tip for the protocol, starts from here and goes to next available one after (4)
    s300_pip.starting_tip = tips.well('A1')


    # Load the labware with its api name, look it up in labware library - https://labware.opentrons.com/
    # Add labware to dictionary
    labware_dict = dict([
                         ('DNA_assembly_Plate', protocol.load_labware("opentrons_96_aluminumblock_nest_wellplate_100ul", 2)), 
                         #ASK MONI - where this labware should be on the robot, error was that location isn't defined.
                         ('temp_PCR_tube', temp_mod1.load_labware("opentrons_96_aluminumblock_nest_wellplate_100ul")), 
                         ('tube_rack_LB', protocol.load_labware("opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical", 6)), 
                         ('tube_rack_competent_cell', protocol.load_labware("opentrons_24_aluminumblock_nest_1.5ml_snapcap", 1))
                        ])

    #----------End of modifications (3)


    # Code to read from csv to "define intial volumes"
    # Discard the blank first line of csv
    csv_iv_data = csv_volume_data_raw.splitlines()[1:]

    csv_iv_reader = csv.DictReader(csv_iv_data)
    for csv_row in csv_iv_reader:
        

        # Define variables from CSV columns
        labware = csv_row['Labware']
        liquid_well = csv_row['Initial_Wells']
        liquid_volume = float(csv_row['Initial_Volume'])
        liquid_name = csv_row['Liquid_Name']
        liquid_description = csv_row['Description']
        liquid_color = csv_row['Color']

        # Now, configure the liquids in the protocol *Note for future can also add description/color
        current_liquid = protocol.define_liquid(
            name=liquid_name,
            description=liquid_description,
            display_color=liquid_color
        )

        # Get object of current labware given the variable name
        curr_labware = getLabwareObject(labware_dict, labware)
        # Add the liquids to the current labware
        curr_labware[liquid_well].load_liquid(liquid=current_liquid, volume=liquid_volume)


    #-------End of modifications (4)

    # -------------------------------TRANSFOR COMPETENT CELLS-----------------------------------

    # Code to read from csv to "transfer_competent_cell"
    # Discard the blank first line of csv
    csv_transfer_competent_cell= csv_transfer_competent_cell_raw.splitlines()[1:]

    first_transfer = True

    csv_reader_competent = csv.DictReader(csv_transfer_competent_cell)
    for csv_row in csv_reader_competent:

        # Define variables from CSV columns
        source_labware = csv_row['Source_Labware']
        source_well = csv_row['Source_Well']
        destination_labware = csv_row['Destination_Labware']
        destination_well = csv_row['Destination_Well']
        transfer_volume = float(csv_row['Transfer_Volume'])
        pick_up_tip = str(csv_row['Pick_Up_Tip'])

        curr_source_labware = getLabwareObject(labware_dict, source_labware)
        curr_destination_labware = getLabwareObject(labware_dict, destination_labware)

        if pick_up_tip == 'TRUE':

            if first_transfer == True:
                #Pick up the first tip
                s300_pip.pick_up_tip()
                first_transfer = False
            else:
                #Discard the previous tip
                s300_pip.drop_tip()
                #Pick up the next tip, will always pick up the next available tip
                s300_pip.pick_up_tip()

            s300_pip.aspirate(transfer_volume, curr_source_labware[source_well])
            #Dispense into the current well
            s300_pip.dispense(transfer_volume, curr_destination_labware[destination_well])


        elif pick_up_tip == 'FALSE':
            if first_transfer == True:
                #Pick up the first tip
                s300_pip.pick_up_tip()
                first_transfer = False

            #Pipette aspirates from the tube at height specified
            s300_pip.aspirate(transfer_volume, curr_source_labware[source_well])
            #Dispense into the current well
            s300_pip.dispense(transfer_volume, curr_destination_labware[destination_well])

        else:
            protocol.comment('Please specify whether to use new or same tip')

    s300_pip.blow_out()
    s300_pip.drop_tip()

    # -------------------------------------TRANSFOR DNA-----------------------------------------

    # Code to read from csv to "transfer_competent_cell"
    # Discard the blank first line of csv
    csv_transfer_golden_gate_mixture = csv_transfer_golden_gate_mixture_raw.splitlines()[1:]

    first_transfer = True

    csv_reader_golden = csv.DictReader(csv_transfer_golden_gate_mixture)
    for csv_row in csv_reader_golden:

        # Define variables from CSV columns
        source_labware = csv_row['Source_Labware']
        source_well = csv_row['Source_Well']
        destination_labware = csv_row['Destination_Labware']
        destination_well = csv_row['Destination_Well']
        transfer_volume = float(csv_row['Transfer_Volume'])
        pick_up_tip = str(csv_row['Pick_Up_Tip'])

        curr_source_labware = getLabwareObject(labware_dict, source_labware)
        curr_destination_labware = getLabwareObject(labware_dict, destination_labware)

        if pick_up_tip == 'TRUE':

            if first_transfer == True:
                #Pick up the first tip
                s300_pip.pick_up_tip()
                first_transfer = False
            else:
                #Discard the previous tip
                s300_pip.drop_tip()
                #Pick up the next tip, will always pick up the next available tip
                s300_pip.pick_up_tip()

            s300_pip.aspirate(transfer_volume, curr_source_labware[source_well])
            #Dispense into the current well
            s300_pip.dispense(transfer_volume, curr_destination_labware[destination_well])


        elif pick_up_tip == 'FALSE':
            if first_transfer == True:
                #Pick up the first tip
                s300_pip.pick_up_tip()
                first_transfer = False

            #Pipette aspirates from the tube at height specified
            s300_pip.aspirate(transfer_volume, curr_source_labware[source_well])
            #Dispense into the current well
            s300_pip.dispense(transfer_volume, curr_destination_labware[destination_well])

        else:
            protocol.comment('Please specify whether to use new or same tip')

    s300_pip.blow_out()
    s300_pip.drop_tip()
    
    # ----------INCUBATION ON ICE----------    
    protocol.delay(minutes=5)
    
    # ----------HEAT SHOCK---------
    #TELL MONI - Since put labware in dictionary, name is only the label for the labware object, not the object itself.
    #SO can't use labware=temp_PCR_tube, that's just the name. Need to get labware OBJECT instead
    #TELL MONI - "temp_mod2" is a string, aka it's just letters. To refer to the actual object, can't use "". just temp_mod2
    protocol.move_labware(labware=getLabwareObject(labware_dict, 'temp_PCR_tube'), new_location=temp_mod2)
    temp_mod2.set_temperature(celsius=42)
    protocol.delay(seconds=40)

    # ----------INCUBATION ON ICE----------
    protocol.move_labware(labware=getLabwareObject(labware_dict, 'temp_PCR_tube'), new_location=temp_mod1)
    temp_mod1.set_temperature(celsius=4)
    protocol.delay(minutes=5)



    # -------------------------------------------TRANSFOR LB WITH ANTIBIOTICS-------------------------------------

    # Code to read from csv to "transfer_LB"
    # Discard the blank first line of csv
    csv_transfer_LB= csv_transfer_LB_raw.splitlines()[1:]

    first_transfer = True

    csv_reader_LB = csv.DictReader(csv_transfer_LB)
    for csv_row in csv_reader_LB:

        # Define variables from CSV columns
        source_labware = csv_row['Source_Labware']
        source_well = csv_row['Source_Well']
        destination_labware = csv_row['Destination_Labware']
        destination_well = csv_row['Destination_Well']
        transfer_volume = float(csv_row['Transfer_Volume'])
        pick_up_tip = str(csv_row['Pick_Up_Tip'])

        curr_source_labware = getLabwareObject(labware_dict, source_labware)
        curr_destination_labware = getLabwareObject(labware_dict, destination_labware)


        if pick_up_tip == 'TRUE':

            if first_transfer == True:
                #Pick up the first tip
                s300_pip.pick_up_tip()
                first_transfer = False
            else:
                #Discard the previous tip
                s300_pip.drop_tip()
                #Pick up the next tip, will always pick up the next available tip
                s300_pip.pick_up_tip()

            s300_pip.aspirate(transfer_volume, curr_source_labware[source_well].top(z=1))
            #Dispense into the current well
            s300_pip.dispense(transfer_volume, curr_destination_labware[destination_well].bottom(z=10), rate=0.25)


        elif pick_up_tip == 'FALSE':
            if first_transfer == True:
                #Pick up the first tip
                s300_pip.pick_up_tip()
                first_transfer = False

            #Pipette aspirates from the tube at height specified
            s300_pip.aspirate(transfer_volume, curr_source_labware[source_well].top(z=1))
            #Dispense into the current well
            s300_pip.dispense(transfer_volume, curr_destination_labware[destination_well].bottom(z=10), rate=0.25)

        else:
            protocol.comment('Please specify whether to use new or same tip')
            
    s300_pip.blow_out()
    s300_pip.drop_tip()

    # ----------put on air-premeable filter----------
    protocol.pause("Remember to put on air-premeable filter")


    # ----------INCUBATION AT 37C----------
    protocol.move_labware(labware=getLabwareObject(labware_dict, 'temp_PCR_tube'), new_location=temp_mod2)
    temp_mod2.set_temperature(celsius=37)
    protocol.delay(minutes=60)
    #ASK MONI - this was called temp_mod before, I assumed you wanted to deactivate temp_mod2 since there is no temp_mod 
    temp_mod2.deactivate()
