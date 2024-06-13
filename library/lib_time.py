# junsCommon.py
import os
import sys
import time
from __init__ import root_folder_path
sys.path.append(root_folder_path)

# epoch_time = 1554723620
# time_formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(epoch_time))
# print("Formatted Date:", time_formatted)
def is_millisecond_epoch(epoch):
    # 현재 시간을 밀리초 단위로 가져와서, 주어진 에포크와 비교합니다.
    current_time_millis = int(time.time() * 1000)
    if len(str(epoch)) == 13 or epoch > current_time_millis:
        # 주어진 에포크가 13자리이거나 현재 시간보다 크면 밀리초로 간주합니다.
        return True
    else:
        # 그렇지 않으면 초 단위로 간주합니다.
        return False

def epoch_to_time(epoch:int, format:str="yyyy-MM-dd HH:mm:ss"):
    format = format.replace('yyyy', '%Y').replace('MM', '%m').replace('dd', '%d').replace('HH', '%H').replace('mm', '%M').replace('ss', '%S')
    if is_millisecond_epoch(epoch):
        epoch = int(epoch/1000)
    return time.strftime(format, time.localtime(epoch))