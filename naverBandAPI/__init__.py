# -*- coding: utf-8 -*-
import os
import sys
current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
root_folder_path = current_directory

while(True):
    if os.path.basename(root_folder_path) == 'naverBandGUI':
        break
    else:
        root_folder_path = os.path.dirname(root_folder_path)
        continue

config_file_path = os.path.join(root_folder_path,'config.yaml')