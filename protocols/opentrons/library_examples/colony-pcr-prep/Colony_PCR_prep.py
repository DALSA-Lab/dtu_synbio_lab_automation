from opentrons import protocol_api

import csv
import json
import math


#--------(Modify) Copy and paste from excel data (1)
#Copy and paste excel green (Step 1) table
#Note that initial volume is in uL
csv_volume_data_raw = """
Labware	Initial_Wells	Initial_Volume	Liquid_Name	Description	Color
snap_caps	A1	60	Master Mix	Manually assembled master mix	#00FF00
snap_caps	A2	60	Master Mix	Manually assembled master mix	#00FF00

"""

#Copy and paste excel blue (Step 2) table
#Note that transfer_volume is in uL
csv_transfer_data_raw = """
Source_Labware	Source_Well	Destination_Labware	Destination_Well	Transfer_Volume	Pick_Up_Tip
snap_caps	A1	PCR_tubes	A1	10	TRUE
snap_caps	A1	PCR_tubes	A2	10	FALSE
snap_caps	A1	PCR_tubes	A3	10	FALSE
snap_caps	A2	PCR_tubes	A4	10	TRUE
snap_caps	A2	PCR_tubes	A5	10	FALSE
snap_caps	A2	PCR_tubes	A6	10	FALSE


"""
#---------End of modifications (1)

csv_transfer_data_raw = csv_transfer_data_raw.replace('	', ',')
csv_volume_data_raw = csv_volume_data_raw.replace('	', ',')


#Function that gets labware object to use given the string name of variable
def getLabwareObject(labware_dict, labware_name):
    for key, value in labware_dict.items():
        if str(key) == str(labware_name):
            return value
    return


#-------(Modify) Change name and description to suit your needs (2)
metadata = {
    "apiLevel": "2.16",
    "protocolName": "LM11_Colony_PCR_prep",
    "description": """A small volume transfer program to prepare for colony PCR. To use, find the areas where 
    it says (Modify) in the code and modify.""",
    "author": "Abigail Lin"
    }
#-------End of modifications (2)

#Protocol context - https://docs.opentrons.com/v2/tutorial.html
def run(protocol: protocol_api.ProtocolContext):

    #---------(Modify) Load the needed Modules, Labware, Tip racks, Pipettes  (3)

    #Loading modules

    #Load heating/cooling module and aluminum block
    #module_name = OT-2 module names (https://docs.opentrons.com/v2/new_modules.html#), location = slot num
    temp_mod = protocol.load_module(
        module_name="temperature module gen2", location="3"
    )
    temp_mod.set_temperature(celsius=4)


    #Loading tip rack, after the api name, put comma and then which slot it is in on the OT-2
    tips = protocol.load_labware(load_name="opentrons_96_filtertiprack_20ul", location=1)
    #Loading pipette, 20uL single tip
    s_20_pip = protocol.load_instrument(instrument_name="p20_single_gen2", mount="left", tip_racks=[tips])

    #Load the labware with its api name, look it up in labware library - https://labware.opentrons.com/
    #Add labware to dictionary
    labware_dict = dict([('PCR_tubes', temp_mod.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul")), 
                         ('snap_caps', protocol.load_labware("opentrons_24_aluminumblock_nest_1.5ml_snapcap", 2))])

    #----------End of modifications (3)


    #Code to read from csv to "define intial volumes"
    #Discard the blank first line of csv
    csv_iv_data = csv_volume_data_raw.splitlines()[1:]

    csv_iv_reader = csv.DictReader(csv_iv_data)
    for csv_row in csv_iv_reader:
        

        #Define variables from CSV columns
        labware = csv_row['Labware']
        liquid_well = csv_row['Initial_Wells']
        liquid_volume = float(csv_row['Initial_Volume'])
        liquid_name = csv_row['Liquid_Name']
        liquid_description = csv_row['Description']
        liquid_color = csv_row['Color']

        #Now, configure the liquids in the protocol *Note for future can also add description/color
        current_liquid = protocol.define_liquid(
            name=liquid_name,
            description=liquid_description,
            display_color=liquid_color
        )

        #Get object of current labware given the variable name
        curr_labware = getLabwareObject(labware_dict, labware)
        #Add the liquids to the current labware
        curr_labware[liquid_well].load_liquid(liquid=current_liquid, volume=liquid_volume)



    #-------(Modify) Define the starting tip for the protocol, starts from here and goes to next available one after (4)
    s_20_pip.starting_tip = tips.well('F1')
    #-------End of modifications (4)

    #Code to read from csv to "transfer volumes"
    #Discard the blank first line of csv
    csv_data = csv_transfer_data_raw.splitlines()[1:]

    first_transfer = True

    csv_reader = csv.DictReader(csv_data)
    for csv_row in csv_reader:

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
                s_20_pip.pick_up_tip()
                first_transfer = False
            else:
                #Discard the previous tip
                s_20_pip.drop_tip()
                #Pick up the next tip, will always pick up the next available tip
                s_20_pip.pick_up_tip()

            
            #Now, start the volume transfer
            
            #Aspirate [take in] liquid, with this format (amount in microliters, well location)
            s_20_pip.aspirate(transfer_volume, curr_source_labware[source_well])
            #Dispense liquid, with this format (amount in microliters, well location)
            s_20_pip.dispense(transfer_volume, curr_destination_labware[destination_well])

        elif pick_up_tip == 'FALSE':
            if first_transfer == True:
                #Pick up the first tip
                s_20_pip.pick_up_tip()
                first_transfer = False

            # Aspirate [take in] liquid, with this format (amount in microliters, well location)
            s_20_pip.aspirate(transfer_volume, curr_source_labware[source_well])
            # Dispense liquid, with this format (amount in microliters, well location)
            s_20_pip.dispense(transfer_volume, curr_destination_labware[destination_well])

        else:

            protocol.comment('Please specify whether to use new or same tip')

    #Discard the previous tip
    s_20_pip.drop_tip()

    temp_mod.deactivate()
        

