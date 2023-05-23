# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 11:07:50 2023

@author: stefa
"""
import openai
import IPython






pre_prompt = """
Here are some training examples. At the end I will give a prompt, and
you will supply the code based on the training.
"""

prompt_1 = """
# Aspirate 50 uL from the first column of plate_1 and 
# dispense to second column of plate_2
"""

completion_1 = """
aspiration_poss = [(plate_1, idx) for idx in range(8)]
aspirate(ham_int, aspiration_poss, vols = [50]*8, liquidClass = liq_class)

dispense_poss = [(plate_2, idx) for idx in range(8,16)]
dispense(ham_int, dispense_poss, vols = [50]*8, liquidClass = liq_class)
"""

prompt_2 = """
# Aspirate 50 uL from the wells 5-8 of plate_1 and 
# dispense to wells 16-19 of plate_2
"""

completion_2 = """
aspiration_poss = [(plate_1, idx) for idx in range(5,9)]
aspirate(ham_int, aspiration_poss, vols = [50]*8, liquidClass = liq_class)

dispense_poss = [(plate_2, idx) for idx in range(16,20)]
dispense(ham_int, dispense_poss, vols = [50]*8, liquidClass = liq_class)
"""


prompt_3 = """
#Aspirate 100 uL from the first column of plate_1 and dispense 20uL to each well in columns
# 3, 5, and 7 of plate_2
"""

completion_3 = """
aspiration_poss = [(plate_1, idx) for idx in range(8)]
vols = [100]*8
aspirate(ham_int, aspiration_poss, vols = vols, liquidClass = liq_class)
dispense_cols = [3,5,7]
for i in dispense_cols:
    dispense_poss = [(plate_2, idx) for idx in range(8*i,8*i+8)]
    dispense(ham_int, dispense_poss, vols = [20]*8, liquidClass = liq_class)


"""

prompt_4 = """
#Pick up tips from the first column of tips_0
"""

completion_4 = """
tips_poss = [(tips_0, idx) for idx in range(8)]
tip_pick_up(ham_int, tips_poss)
"""

prompt_5 = """
# Aspirate 25 uL from the first column of plate_1 at liquid height 5 and with 2 mix cycles
"""

completion_5 = """
aspiration_poss = [(plate_1, idx) for idx in range(8)]
vols = [25]*8
aspirate(ham_int, aspiration_poss, vols = vols, liquidClass = liq_class, liquidHeight = 5.0, mixCycles = 2)
"""

prompt_6 = """
# pool fragments from wells 10, 19, and 23 on plate 0 into well 1 on plate 1
"""

completion_6 = """
source_wells = [10, 19, 23]
source_plate = plate_0

target_well = 1
target_plate = plate_1

pooling(source_wells, source_plate, target_well, target_plate)
"""

prompt_7 = """
# pool fragments from wells 12, 54, and 63 on plate 0 into well 1 on plate 1
"""

completion_7 = """
# Here's the pooling code you asked for, with wells 12, 54, and 63 on plate_0 as source
# wells and well 1 on plate_1 as a target well:
target_well = 1
target_plate = plate_1

source_wells = [12, 54, 63]
source_plate = plate_0


pooling(source_wells, source_plate, target_well, target_plate)
"""

prompt_8 = """
# pool fragments from wells 2, 4, 6, 7, and 8 on plate 0 into well 3 on plate 0
"""

completion_8= """
# Here's the pooling code you asked for, with wells 2, 4, 6, 7, and 8 on plate_0 as source
# wells and well 3 on plate_1 as a target well:
source_wells = [2, 4, 6, 7, 8]
source_plate = plate_0

target_well = 3
target_plate = plate_0

pooling(source_wells, source_plate, target_well, target_plate)
"""

prompt_9 = """
# pool fragments from wells 2, 28, 31, 33, and 35 on plate 0 into well 6 on plate 1
"""

completion_9= """
# Here's the pooling code you asked for, with wells 2, 28, 31, 33, and 35 on plate_0 as source
# wells and well 6 on plate_1 as a target well:
source_wells = [2, 28, 31, 33, 35]
source_plate = plate_0

target_well = 6
target_plate = plate_1

pooling(source_wells, source_plate, target_well, target_plate)
"""

prompt_10 = """
# pool from wells 52, 68, and 91 on plate 0 into well 10 on plate 1
"""

completion_10= """
# Here's the pooling code you asked for, with wells 15, 28, and 31 on plate_0 as source
# wells and well 7 on plate_1 as a target well:

pooling([52, 68, 91], plate_0, 7, plate_1)
"""


def complete(prompt):
    res = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": """You are an assistant for generating code for 
             a liquid handling robot. I will give you examples. The function you have available
             to you is pooling. Make sure to construct a response with respect to the specific
             well indices and plates specified in the user prompt"""},
            {"role": "user", "content": prompt_6},
            {"role": "assistant", "content": completion_6},
            {"role": "user", "content": prompt_7},
            {"role": "assistant", "content": completion_7},
            # {"role": "user", "content": prompt_8},
            # {"role": "assistant", "content": completion_8},
            # {"role": "user", "content": prompt_9},
            # {"role": "assistant", "content": completion_9},
            {"role": "user", "content": prompt},
        ]
    )
    
    response = res['choices'][0]['message']['content']
    return response


    
