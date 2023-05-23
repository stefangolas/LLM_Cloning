# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 21:12:47 2022

@author: stefa
"""
import os
from pyhamilton import (HamiltonInterface,  LayoutManager, 
 Plate96, Tip96, initialize, tip_pick_up, tip_eject, 
 aspirate, dispense,  oemerr, resource_list_with_prefix, normal_logging,
 layout_item)
import IPython
from preprompt import complete
from voice import voice_to_text



liq_class = 'StandardVolumeFilter_Water_DispenseJet_Empty'

def assist(prompt, safe = False):
    response = complete(prompt)
    lines = response.split('\n')
    d = dict(locals(), **globals())
    print("Printing response")
    for line in lines:
        print(line)
        if safe:
            input("Proceed?")
    for line in lines:
        try:
            exec(line, d, d)
        except SyntaxError:
            pass
        
lmgr = LayoutManager('deck.lay')
#plates = resource_list_with_prefix(lmgr, 'plate_', Plate96, 5)
tips_0 = layout_item(lmgr, Tip96, 'tips_0')

## Reaction plates
fragments_site = layout_item(lmgr, Plate96, 'dna_fragments_site')
pooling_site = layout_item(lmgr, Plate96, 'pooling_site')
cosmid_assembly_site = layout_item(lmgr, Plate96, 'cosmid_assembly_site')

## Equipment
thermal_cycler = layout_item(lmgr, Plate96, 'thermal_cycler')
purification_module = layout_item(lmgr, Plate96, 'purification_module')

def assemble_gibson():   
    pass

def purify_gibson():  
    pass

def cosmid_assembly():
    pass

liq_class = 'StandardVolumeFilter_Water_DispenseJet_Empty'



def pooling(source_wells, source_plate, target_well, target_plate):
    tip_idx = 0
    for source in source_wells:
        tips_poss = [(tips_0, tip_idx)] + [None]*7
        asp_poss = [(source_plate, source)] + [None]*7
        vols = [10]*1 + [None]*7
        disp_poss = [(target_plate, target_well)] + [None]*7
        
        tip_pick_up(ham_int, tips_poss)
        aspirate(ham_int, asp_poss, vols = vols, liquidClass = liq_class)
        dispense(ham_int, disp_poss, vols = vols, liquidClass = liq_class)
        tip_eject(ham_int)
        
        tip_idx += 1



print("""Be careful! The assist() function uses an AI coding assistant to interpret
      natural language into PyHamilton code. Do not use this outside of simulation
      mode until you are familiar with how it works.""")


if __name__ == '__main__': 
    with HamiltonInterface(simulate=True) as ham_int:
        normal_logging(ham_int, os.getcwd())
        initialize(ham_int)
        
        ## Pool fragments ##
        source_wells = [], target_well = 0
        pooling(source_wells, fragments_site, target_well, pooling_site)
        
        ## Gibson assembly ##
        assemble_gibson()
        
        ## Purify gibson ##
        purify_gibson()
        
        ## Cosmid assembly ##
        cosmid_assembly(source_well, target_well)