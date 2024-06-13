# junsCommon.py
import os
import sys
from __init__ import root_folder_path
sys.path.append(root_folder_path)
# from _workplace.library.junLib_importlib import auto_import
# auto_import('moviepy', 'moviepy')
import shutil
import re
import subprocess
# from moviepy.editor import VideoFileClip
# move_up_batch_file_path = path = os.path.join(root_folder_path, 'util', 'files_move', 'moveUp.bat')

def clear():
    subprocess.run(['cmd', '/c', 'cls'])
    
def rename_folder(old_folder_path, new_name:str):
    """
    폴더의 이름을 변경하는 함수

    :param old_name: 변경하려는 폴더의 현재 이름 (경로 포함)
    :param new_name: 폴더에 부여하려는 새 이름(경로 미포함)
    """
    new_folder_path = join_folder_path(os.path.dirname(old_folder_path), new_name)
    try:
        os.rename(old_folder_path, new_folder_path)
        print(f"'{old_folder_path}' has been renamed to '{new_folder_path}'")
    except Exception as e:
        print(f"Error renaming folder: {e}")

def convert_to_korean_numbers(number:int|str):
    korean_numbers = ['영', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
    korean_units = ['', '십', '백', '천']

    # 입력된 숫자를 문자열로 변환하여 자릿수를 분리

    number_str = str(number) if isinstance(number, int) else number
    if number_str == '0': return '영'
    digits = list(number_str)

    # 숫자를 한국어로 변환
    korean_number_str = ''
    for i, digit in enumerate(digits):
        # 0은 생략
        if digit == '0': continue
        # 한국어 숫자 추가
        korean_number_str += korean_numbers[int(digit)]
        # 자릿수 단위 추가
        t = len(digits) - i - 1 if (len(digits) - i - 1) >= 0 else 0
        if t >= len(korean_units):
            t = len(korean_units)-1
        korean_number_str += korean_units[t]
    korean_number_str = korean_number_str.replace('일십', '십').replace('일백', '백').replace('일천', '천').replace('일만', '만')
    return korean_number_str

def change_encoding(file_path, old_encoding:str, new_encoding:str):
    # 기존 파일 열기
    with open(file_path, 'r', encoding=old_encoding) as old_file:
        # 내용 읽어오기
        content = old_file.read()

    # 새로운 인코딩 방식으로 파일 열기
    with open(file_path, 'w', encoding=new_encoding) as new_file:
        # 내용 쓰기
        new_file.write(content)

def ifinput(variable='', string='folder path'):
    return variable if variable else strip_quotes(input(string))

def is_convertible_to_number(s, target='int', return_value:bool=False):
    if target == 'int':
        try:
            int(s)  # 문자열을 실수로 변환 시도
            return int(s) if return_value else True
        except ValueError:  # 변환 실패 시
            return False
    elif target == 'float':
        try:
            float(s)  # 문자열을 실수로 변환 시도
            return float(s) if return_value else True
        except ValueError:  # 변환 실패 시
            return False


def stqinput(variable=None, string='folder path'):
    if not variable:
        return strip_quotes(input(f'Enter {string} : '))
    return variable

def save_to_audacity_label(segments, output_file):
    with open(output_file, 'w') as f:
        for part in segments:
            words = part['words']
            for wordinfo in words:
                start_time = float(f"{float(wordinfo['start']):.6f}")
                start_time = 0 if start_time < 0 else start_time
                end_time = f"{float(wordinfo['end']):.6f}"
                word_text = str(wordinfo['word']).strip()
                f.write(f"{start_time}\t{end_time}\t{word_text}\n")

def format_time(total_seconds):
    print(f"seconds: {total_seconds}")
    total_seconds = float(total_seconds)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = (total_seconds % 3600) % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return "{:02d}:{:02d}:{:02d},{:03d}".format(hours, minutes, int(seconds), milliseconds)

def strip_quotes(text):
    if str(text).startswith('"') and str(text).endswith('"'):
        return str(text).strip('"')
    return str(text)

def path_exist(file_path):
    return os.path.exists(file_path)

def split_str(string_split_by, split_code='\t'):
    result = str(string_split_by).split(str(split_code))
    return result

def move_file(need_to_move_file_path, target_path, show_msg=False):
    """ 
    1. target_path is file path or folder path.
    2. file path -> just do
    3. folder path -> basename of need_to_move_file_path is target_file_name
    """
    if os.path.isfile(target_path):
        if not path_exist(os.path.dirname(target_path)):create_folder(os.path.dirname(target_path))
    elif os.path.isdir(target_path):
        if not path_exist(target_path):create_folder(target_path)
        target_path = join_folder_path(target_path, os.path.basename(need_to_move_file_path))
    if show_msg:print("\n", need_to_move_file_path, ' ->\n', target_path)
    try:
        shutil.move(need_to_move_file_path, target_path)
        if show_msg:print("파일을 이동했습니다.")
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except PermissionError:
        print("파일 이동 권한이 없습니다.")
    except Exception as e:
        print("파일 이동 중 오류가 발생했습니다:", str(e))

def lift_folders(base_path):
    # 입력받은 폴더 내의 모든 하위 폴더를 가져옵니다.
    subfolders = [f.path for f in os.scandir(base_path) if f.is_dir()]

    for subfolder in subfolders:
        print("process ", os.path.basename(subfolder))
        # 각 하위 폴더 내의 폴더들을 가져옵니다.
        inner_subfolders = [f.path for f in os.scandir(subfolder) if f.is_dir()]

        for inner_subfolder in inner_subfolders:
            # 하위 폴더의 이름을 가져옵니다.
            inner_subfolder_name = os.path.basename(inner_subfolder)
            # 새로운 경로를 생성합니다.
            new_path = os.path.join(base_path, inner_subfolder_name)

            # 해당 폴더가 이미 존재하는지 확인하고, 없으면 폴더를 생성합니다.
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                print(new_path)

            # 파일들을 새로운 폴더로 옮깁니다.
            for item in os.listdir(inner_subfolder):
                s = os.path.join(inner_subfolder, item)
                d = os.path.join(new_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            # 옮긴 후 원래의 폴더를 삭제합니다.
            shutil.rmtree(inner_subfolder)

        # 모든 파일을 옮긴 후 상위 폴더도 삭제합니다.
        os.rmdir(subfolder)

def open_folder_path(folder_path):
    import sys
    if sys.platform == 'win32':
        # subprocess.run(['explorer', os.path.abspath(folder_path)])
        os.startfile(folder_path)
    elif sys.platform == 'darwin':  # macOS
        subprocess.run(['open', folder_path])
    else:  # Linux 및 기타 유닉스 시스템
        subprocess.run(['xdg-open', folder_path])

def move_file_to_current_other_folder(need_to_move_file_path, folder_name='backup', overwrite:bool=False, show_msg:bool=True, show_err:bool=True) -> str:
    target_folder = join_folder_path(os.path.dirname(need_to_move_file_path), folder_name)
    if not path_exist(target_folder): create_folder(target_folder)
    target_path = join_folder_path(target_folder, os.path.basename(need_to_move_file_path))
    try:
        if overwrite:
            if path_exist(target_path):
                if path_exist(rename(target_path, suffix='_back')):
                    delete_file(rename(target_path, suffix='_back'))
                else:
                    rename_and_move_file(target_path, rename(target_path, suffix='_back'))
        shutil.move(need_to_move_file_path, target_path)
        if show_msg: print(f"{need_to_move_file_path} to {target_path} 파일을 이동했습니다.")
    except FileNotFoundError:
        if show_err: print("파일을 찾을 수 없습니다.")
    except PermissionError:
        if show_err: print("파일 이동 권한이 없습니다.")
    except Exception as e:
        if show_err: print("파일 이동 중 오류가 발생했습니다:", str(e))
    finally:
        return target_path

def create_folder(folder_path, show_msg:bool=True):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        if show_msg: print(f"폴더를 생성했습니다: {folder_path}")
    else:
        if show_msg: print(f"폴더가 이미 존재합니다: {folder_path}")
    return folder_path
def file_name_folder_path(file_path):
    return join_folder_path(os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0])

def join_folder_path(*args):
    path = str(os.path.join(*args))
    return path

# def move_backup(folder_path, file_name):
#     file_path = os.path.join(folder_path, file_name)

def remove_extra_tabs(text:str):
    lines = text.split('\n')
    processed_lines = []

    for line in lines:
        parts = line.split('\t')
        if len(parts) > 1:
            processed_line = ''
            for part in parts:
                if part == parts[0]:
                    continue
                processed_line = processed_line + part.strip('\t')
            processed_lines.append(parts[0] + '\t' + processed_line)
        else:
            processed_lines.append(line)

    processed_text = '\n'.join(processed_lines)
    return processed_text

def delete_file(file_path:str, show_msg:bool=True):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            if show_msg: print(f"파일 '{file_path}'이(가) 삭제되었습니다.")
        else:
            if show_msg: print(f"파일 '{file_path}'을(를) 찾을 수 없습니다.")
    except Exception as e:
        print(e)

# if __name__ == "__main__":
#     folder_path = '/경로/폴더'  # 실제 폴더 경로로 대체해야 합니다.
#     file_name = 'example.txt'  # 실제 파일명으로 대체해야 합니다.
#     delete_file(folder_path, file_name)

def get_txt_files_in_folder(folder_path):
    txt_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            txt_files.append(file_name)
    return txt_files

def get_files_in_folder_via_ext(folder_path, extension='txt'):
    target_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.'+extension):
            target_files.append(file_name)
    return target_files


def remove_empty_folders(folder_path): # type: ignore
    # 폴더 내의 모든 파일과 폴더를 가져옵니다.
    all_contents = os.listdir(folder_path)
    
    # 하위 폴더를 탐색합니다.
    for content in all_contents:
        content_path = os.path.join(folder_path, content)
        
        # 폴더인 경우 재귀적으로 함수를 호출하여 하위 폴더를 탐색합니다.
        if os.path.isdir(content_path):
            remove_empty_folders(content_path)
            
            # 폴더가 비어있는지 확인하고 비어있다면 삭제합니다.
            if not os.listdir(content_path):
                os.rmdir(content_path)

def get_specific_sub_folder_path(folder_path, target_folder_name):
    for root, dirs, files in os.walk(folder_path):
        for directory in dirs:
            if directory == target_folder_name:
                return os.path.join(root, directory)
    return None

def get_specific_sub_folder_paths(folder_path, target_folder_name, recursive=False):
    result_paths = []
    for root, dirs, files in os.walk(folder_path):
        if not recursive and root != folder_path:
            continue
        for directory in dirs:
            if directory == target_folder_name:
                result_paths.append(os.path.join(root, directory))
    return result_paths


def get_startwith_sub_folder_path(folder_path, contained_folder_name):
    for root, dirs, files in os.walk(folder_path):
        for directory in dirs:
            if str(directory).startswith(contained_folder_name):
                return os.path.join(root, directory)
    return None

def move_files_to_subfolders(target_folder_path, match_length, extension=None, move_contain_resource:bool=True, show_msg:bool=True):
    # 대상 폴더 내 파일 목록을 가져옵니다.
    files = os.listdir(target_folder_path)

    for file in files:
        if extension:
            if not os.path.splitext(file)[1].__contains__(extension):
                if show_msg: print(os.path.basename(file), ' is not contain ', extension)
                continue
        # 파일명에서 일치하는 글자 개수만큼의 글자를 가져옵니다.
        matching_text = split_filename(file)[0][:match_length]
        print('matching_text : ',matching_text)
        if move_contain_resource == False and os.path.splitext(os.path.basename(file))[0] == matching_text:
            if show_msg: print(os.path.splitext(os.path.basename(file))[0], ' and ', matching_text, ' is same. skip this.')
            continue
        # 일치하는 글자를 폴더명으로 하는 하위 폴더 경로를 생성합니다.
        subfolder_path = os.path.join(target_folder_path, matching_text)

        # 하위 폴더가 존재하지 않을 경우 폴더를 생성합니다.
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        # 파일을 하위 폴더로 이동시킵니다.
        source_path = os.path.join(target_folder_path, file)
        destination_path = os.path.join(subfolder_path, file)
        move_file(source_path, destination_path)
    return target_folder_path

def move_file_to_subfolders(file_path, match_length:int):
    # 파일명에서 일치하는 글자 개수만큼의 글자를 가져옵니다.
    matching_text = basename(file_path)[:match_length]

    # 일치하는 글자를 폴더명으로 하는 하위 폴더 경로를 생성합니다.
    subfolder_path = os.path.join(parent_path(file_path), matching_text)

    # 하위 폴더가 존재하지 않을 경우 폴더를 생성합니다.
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    # 파일을 하위 폴더로 이동시킵니다.
    # source_path = os.path.join(parent_path(file), file)
    destination_path = os.path.join(subfolder_path, basename(file_path))
    shutil.move(file_path, destination_path)

def get_matching_sub_folder_paths(folder_path, regex_pattern:str):
    matching_paths = []
    for root, dirs, files in os.walk(folder_path):
        for directory in dirs:
            print(os.path.basename(directory))
            match = re.match(regex_pattern, directory)
            if match and match.group() == directory:
                matching_paths.append(os.path.join(root, directory))
    return matching_paths

def move_folder_structure(src_path: str, dest_path: str, show_msg:bool=True):
    """
    원본 폴더의 파일 및 폴더 구조를 그대로 도착지 폴더로 이동합니다.

    :param src_path: 원본 폴더 경로
    :param dest_path: 도착지 폴더 경로
    """
    # 원본 폴더의 이름을 가져옵니다.
    src_folder_name = os.path.basename(src_path)
    # 도착지 폴더 내에 원본 폴더와 동일한 이름의 폴더 경로를 생성합니다.
    final_dest_path = os.path.join(dest_path, src_folder_name)

    # 원본 폴더를 도착지 폴더로 이동합니다.
    shutil.move(src_path, final_dest_path)
    if show_msg: print(f"'{src_path}'를 '{final_dest_path}'로 이동했습니다.")

def is_empty_folder(folder_path):
    # 폴더 내의 파일 목록을 가져옵니다.
    files = os.listdir(folder_path)

    # 폴더 내에 파일이 존재하는지 여부를 확인합니다.
    if files:
        return False  # 파일이 존재함
    else:
        return True  # 파일이 존재하지 않음

def get_files_path_in_folder_via_ext(folder_path, extension='txt', recursive=False, show_msg=False):
    target_files = []
    
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name)
        
        # 파일이면 확장자 확인 후 리스트에 추가
        if os.path.isfile(full_path) and file_name.endswith('.' + extension):
            target_files.append(full_path)
            if show_msg:
                clear()
                print(f"getting files... {len(target_files)}")
        
        # 재귀적으로 탐색 옵션이 활성화되고, 현재 경로가 폴더면 함수를 재귀적으로 호출
        elif recursive and os.path.isdir(full_path):
            target_files.extend(get_files_path_in_folder_via_ext(full_path, extension, recursive))
    
    return target_files

def get_files_path_in_folder_via_ext_yield(folder_path, extension='txt', recursive=False, show_msg=False):
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name)
        
        # 파일이면 확장자 확인 후 경로 yield
        if os.path.isfile(full_path) and file_name.endswith('.' + extension):
            yield full_path
            if show_msg:
                print(f"Getting files...") # 실시간 메시지 출력, 필요에 따라 조정 가능
        
        # 재귀적으로 탐색 옵션이 활성화되고, 현재 경로가 폴더면 함수를 재귀적으로 호출
        elif recursive and os.path.isdir(full_path):
            yield from get_files_path_in_folder_via_ext_yield(full_path, extension, recursive, show_msg)


def get_files_path_in_folder_via_startwith(folder_path, startwith:str, extension:str=None, contain_origin:bool=True, recursive=False): # type: ignore
    target_files = []
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name)
        
        file_name = str(file_name)
        
        # 파일이면 확장자 확인 후 리스트에 추가
        if os.path.isfile(full_path) and file_name.startswith(startwith):
            if extension:
                if file_name.endswith('.'+extension):
                    if contain_origin is False and os.path.splitext(file_name)[0] == startwith:
                        continue
                    target_files.append(join_folder_path(folder_path, file_name))
                else:
                    continue
            else:
                target_files.append(join_folder_path(folder_path, file_name))
        # 재귀적으로 탐색 옵션이 활성화되고, 현재 경로가 폴더면 함수를 재귀적으로 호출
        elif recursive and os.path.isdir(full_path):
            target_files.extend(get_files_path_in_folder_via_startwith(full_path, startwith=startwith, extension=extension, contain_origin=contain_origin, recursive=recursive))
    return target_files

def get_files_path_in_folder_via_endswith(folder_path, endswith:str, extension:str=None): # type: ignore
    target_files = []
    for file_name in os.listdir(folder_path):
        file_basename, ext = os.path.splitext(os.path.basename(file_name))
        if file_basename.endswith(endswith):
            if extension:
                if ext == ('.' + extension):
                    target_files.append(join_folder_path(folder_path, file_name))
                else:
                    continue
            else:
                target_files.append(join_folder_path(folder_path, file_name))
        else:
            continue
    return target_files

def get_files_path_in_folder_via_contain(folder_path, contain_str:str, extension:str=None): # type: ignore
    target_files = []
    for file_name in os.listdir(folder_path):
        file_name = str(file_name)
        if file_name == contain_str:
            continue
        if file_name.__contains__(contain_str):
            if extension:
                if file_name.endswith('.'+extension):
                    target_files.append(join_folder_path(folder_path, file_name))
            elif not extension:
                target_files.append(join_folder_path(folder_path, file_name))
            else:
                continue
    return target_files

def get_files_path_in_folder_at_all(folder_path):
    target_files = []
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name)
        if os.path.isfile(full_path):  # 파일인 경우에만 추가
            target_files.append(full_path)
    return target_files
# ===============
def find_files_with_extension(directory, extension):
    """
    Searches for all files with a given extension in the specified directory and its subdirectories.

    :param directory: Path to the directory to start the search from.
    :param extension: File extension to search for (e.g. '.txt', '.xml').
    :return: List of file paths with the specified extension.
    """
    matching_files = []

    # Walk through directory
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                matching_files.append(os.path.join(dirpath, filename))

    return matching_files
    
def get_files_path_at_all(folder_path, extension=None, show_msg=True):
    result_files = []
    for root, dirs, files in os.walk(folder_path):
        if show_msg: print('파일 탐색 중')
        for file in files:
            # _, extension = os.path.splitext(file)
            file_path = os.path.join(root, file)
            if show_msg:print(f'파일 경로 추출 중...{file_path}')
            if extension:
                if os.path.splitext(os.path.basename(file_path))[1].__contains__(extension):
                    result_files.append(file_path)
                else:
                    continue
            else:
                result_files.append(file_path)
    if show_msg: print(f"{folder_path} 경로에서 총 {len(result_files)}개의 파일을 찾았습니다.")
    return result_files

def get_files(folder_path, target='text'):
    if not target:
        # 대상을 선택합니다. video, text, audio 등을 입력할 수 있습니다.
        target = input("대상을 선택하세요 (video, text, audio): ")

    extension_map = {
        'video': ['.mp4', '.avi', '.mkv', '.mov'],
        'text': ['.txt'],
        'audio': ['.mp3', '.wav', '.flac'],
        'csv': ['.csv']
        # 추가적인 확장자와 대상을 필요에 따라 지정할 수 있습니다.
    }

    target_extensions = extension_map.get(target.lower(), [])
    result_files = []
    if path_exist(folder_path):
        for root, dirs, files in os.walk(folder_path):
            print('파일 탐색 중')
            for file in files:
                _, extension = os.path.splitext(file)
                if extension.lower() in target_extensions:
                    file_path = os.path.join(root, file)
                    print(f'파일 경로 추출 중...{file_path}')
                    result_files.append(file_path)
        print(f"{folder_path} 경로에서 총 {len(result_files)}개의 파일을 찾았습니다.")
    return result_files

def move_files_up_batch(folder_path):
    batch_process = subprocess.Popen(move_up_batch_file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    batch_process.communicate(input=folder_path + '\n')

def move_files_up(folder_path):
    # 입력받은 폴더 경로 내의 모든 파일과 하위 폴더를 탐색
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 파일의 현재 경로
            current_file_path = os.path.join(root, file)
            # 파일을 입력받은 폴더 경로 바로 아래로 이동
            new_file_path = os.path.join(folder_path, file)
            shutil.move(current_file_path, new_file_path)
        for dir in dirs:
            # 하위 폴더의 현재 경로
            current_dir_path = os.path.join(root, dir)
            # 하위 폴더를 입력받은 폴더 경로 바로 아래로 이동
            new_dir_path = os.path.join(folder_path, dir)
            # if not path_exist(new_dir_path):
            shutil.move(current_dir_path, new_dir_path)

def remove_empty_folders(parent_folder_path=''): # type: ignore
    parent_folder_path = strip_quotes(input('Enter folder path : '))  if not parent_folder_path else parent_folder_path
    target_folder_path = get_sub_folder_path(parent_folder_path)
    
# 특정 폴더 경로를 입력합니다.
# folder_path = input("폴더 경로를 입력하세요: ")


# 파일 경로를 가져옵니다.
# files = get_files(folder_path, target)

# # 결과 출력
# print(f"{target.capitalize()} 파일 목록:")
# for file in files:
#     print(file)

# ===============

# def read_line_list_from_lines(text_file):
#     pass
# if __name__ == "__main__":
#     folder_path = '/path/to/your/folder'  # 실제 폴더 경로로 변경해주세요
#     txt_files_list = get_txt_files_in_folder(folder_path)
#     print(txt_files_list)
def read_lines(text_file):
    lines = []
    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        lines[i] = line.replace('\n', '')
    return lines
    
def cut_after_dot(float_number, length_after_dot=2):
    split_number = split_str(str(float_number),'.')
    print(split_number)
    return (split_number[0] + '.' + split_number[1][:length_after_dot]) if len(split_number)>1 else float_number



def write_to_file(filename, value:str='', mode:str='w'):
    with open(filename, mode, encoding='utf-8') as file:
        if isinstance(value, list):  # value가 리스트인 경우
            value = '\n'.join(value)  # 리스트를 개행 문자로 연결하여 하나의 문자열로 만듭니다.
        file.write(value + '\n')
    return filename

def write_to_xmlfile(filename, list_value):
    with open(filename, 'w', encoding="UTF-8") as file:
        for value in list_value:
            file.write(value)
    return filename

def change_extension(file_path, new_extension=None):
    file_name, extension= os.path.splitext(file_path)
    if new_extension:
        return file_name + '.' + new_extension
    elif extension:
        return file_name + extension
    else:
        return file_name

def add_suffix(file_name, suffix=''):
    file_path, ext = os.path.splitext(file_name)
    return file_path+suffix+ext

def get_suffix(file_name, split_char:str='_'):
    file_basename, ext = os.path.splitext(basename(file_name))
    split = str(file_basename).split(split_char)
    suffix = split.pop(-1)
    return split_char.join(split), suffix

def change_underbar_suffix(file_name, suffix=''):
    return rename(file_name, suffix=('_'+suffix) if suffix else '') 

def remove_or_replace_last_underbar_suffix(file_name, suffix=''):
    file_name, extension = split_filename(file_name=file_name)
    split_underbar = file_name.split('_')
    split_underbar.pop(-1)
    rebuild_file_name = None
    for i, split_str_name in enumerate(split_underbar):
        if i == 0:
            rebuild_file_name = split_str_name
        else:
            rebuild_file_name += '_' + split_str_name # type: ignore
    if extension:
        extension = '.' + extension
    else:
        extension = ""
    if not suffix:
        return rebuild_file_name + suffix + extension # type: ignore
    return rebuild_file_name + '_' + suffix + extension # type: ignore

def except_ext_filename(file_path):
    splited = split_filename(basename(file_path))
    if len(splited)>1:
        file_name = splited[0]
        extension = splited[1]
        return file_name, extension
    else:
        return splited, None

def split_filename(file_name):
    file_name, extension = os.path.splitext(file_name)
    if file_name and extension:
        # 파일명과 확장자를 분리
        # file_name = ".".join(parts[:-1])  # 파일명 부분
        # extension = parts[-1]  # 확장자 부분
        return str(file_name), str(extension)
    else:
        # 확장자가 없는 경우
        return str(file_name), None

def rename(file_path, prefix="", suffix="", new_name="", new_extension=None):
    parentpath = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    file_name, extension = os.path.splitext(base_name)
    if new_extension:
        extension = '.' + new_extension
    if new_name:
        file_name_final = prefix + new_name + suffix + extension
    else:
        file_name_final = prefix + file_name + suffix + extension
    final_path = os.path.join(parentpath, file_name_final)
    return final_path

def rename_and_move_file(old_path, new_path, show_msg:bool=True, show_err:bool=True, overwrite:bool=False):
    try:
        os.rename(old_path, new_path)
        if show_msg: print(f"File renamed and moved successfully from {old_path} to {new_path}")
    except FileNotFoundError:
        if show_err: print(f"File not found at {old_path}")
    except FileExistsError:
        if overwrite:
            delete_file(new_path)
            rename_and_move_file(old_path, new_path, show_msg, show_err)
            return
        elif show_err:
            print(f"A file already exists at \'{new_path}\'. Rename and move operation failed.")

def move_with_backup(source_file_path, destination_file_path):
    """
    파일을 지정된 경로로 이동하며, 이미 해당 경로에 같은 이름의 파일이 존재하는 경우 백업 폴더에 이동할 파일을 백업한 뒤 이동합니다.

    Args:
        source_file_path (str): 원본 파일의 경로
        destination_path (str): 이동할 대상 경로
    """
    print(f"source_file_path: {source_file_path}")
    print(f"destination_path: {destination_file_path}")
    if not path_exist((os.path.dirname(destination_file_path))):
        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
    file_name = os.path.basename(source_file_path)

    # 대상 경로에 같은 이름의 파일이 이미 존재하는지 확인합니다.
    if os.path.exists(destination_file_path):
        # 백업 폴더 생성 (이미 존재하면 생성되지 않음)
        backup_folder = os.path.join(os.path.dirname(destination_file_path), "backup")
        if not path_exist(backup_folder):
            os.makedirs(backup_folder, exist_ok=True)

        # 백업 폴더에 새로운 파일명을 부여하여 중복을 피합니다.
        backup_file_name, backup_file_extension = os.path.splitext(file_name)
        count = 1
        while True:
            new_backup_file_name = f"{backup_file_name}_backup_{str(count).zfill(3)}{backup_file_extension}"
            new_backup_file_path = os.path.join(backup_folder, new_backup_file_name)
            if not os.path.exists(new_backup_file_path):
                break
            count += 1

        # 백업 폴더로 기존 파일을 이동시킵니다.
        shutil.move(destination_file_path, new_backup_file_path)
        print(f"Existing file moved to backup folder: {new_backup_file_path}")

    # 대상 경로의 중간 디렉토리가 존재하지 않는 경우 생성합니다.
    if not path_exist(os.path.dirname(destination_file_path)):
        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

    # 원본 파일을 대상 경로로 이동합니다.
    shutil.move(source_file_path, destination_file_path)
    print(f"File moved to destination: {destination_file_path}")

def copy_and_rename_folder(src_path, dest_path, overwrite:bool=False):
    """
    Copies a folder and renames the copied folder.

    Parameters:
    - src_path (str): The path of the directory to be copied.
    - dest_name (str): The new name for the copied directory.
    - overwrite (bool): Whether to overwrite the destination files if they already exist.

    Returns:
    - str: The path of the renamed directory.
    """
    # Determine the destination path
    # dest_path = os.path.join(os.path.dirname(src_path), dest_name)
    
    def _copytree(src, dst, overwrite=False, show_msg:bool=True):
        """ Custom copytree function that overwrites files if they already exist. """
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                _copytree(s, d, overwrite=overwrite)
                if show_msg: print(f"{os.path.basename(src)}\t{item} to {os.path.basename(dst)}")
            else:
                if os.path.exists(d) and overwrite:
                    os.remove(d)
                if not os.path.exists(d) or overwrite:
                    shutil.copy2(s, d)
    
    # Check if the destination directory already exists
    if os.path.exists(dest_path):
        if overwrite:
            _copytree(src_path, dest_path, overwrite=True)
        else:
            print(f"Directory {dest_path} already exists. Skipping...")
            return dest_path
    else:
        # if not path_exist(dest_path):
        #     create_folder(dest_path)
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
    
    return dest_path

def copy_and_rename_file(source_path, destination_path, overwrite=True, show_msg:bool=True):
    # Check if destination is a directory
    if os.path.isdir(destination_path):
        # If it's a directory, use the original filename but place it in the new directory
        destination_path = os.path.join(destination_path, os.path.basename(source_path))
    if overwrite:
        try:
            shutil.copy2(source_path, destination_path)
            if show_msg: print(f"{source_path} to {destination_path} copied")
        except Exception as e:
            print(f"Error copying file: {e}")
            print(f"Source: {source_path}")
            print(f"Destination: {destination_path}")
        return destination_path
    else:
        if path_exist(destination_path):
            print(f"{destination_path} is already existed.")
            return None
        else:
            shutil.copy(source_path, destination_path)


def basename(file_path):
    base_name = os.path.basename(file_path)
    return base_name

def parent_path(file_path):
    return os.path.dirname(file_path)

def move_files_to_parent_folder(folder_path):
    # 폴더 내의 모든 파일과 폴더를 가져옵니다.
    all_contents = os.listdir(folder_path)
    
    # 하위 폴더를 탐색합니다.
    for content in all_contents:
        content_path = os.path.join(folder_path, content)
        
        # 폴더인 경우 재귀적으로 함수를 호출하여 하위 폴더를 탐색합니다.
        if os.path.isdir(content_path):
            move_files_to_parent_folder(content_path)
        else:
            # 파일인 경우 상위 폴더로 이동시킵니다.
            # move_file(content_path, join_folder_path(folder_path, basename(content_path)))
            shutil.move(content_path, join_folder_path(folder_path, content))

def remove_empty_folders(folder_path):
    # 폴더 내의 모든 파일과 폴더를 가져옵니다.
    all_contents = os.listdir(folder_path)
    
    # 하위 폴더를 탐색합니다.
    for content in all_contents:
        content_path = os.path.join(folder_path, content)
        
        # 폴더인 경우 재귀적으로 함수를 호출하여 하위 폴더를 탐색합니다.
        if os.path.isdir(content_path):
            remove_empty_folders(content_path)
            
            # 폴더가 비어있는지 확인하고 비어있다면 삭제합니다.
            if not os.listdir(content_path):
                os.rmdir(content_path)

def sub_path_dict(folder_path):
    subdirectories = {}
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            dir_path = os.path.abspath(os.path.join(root, dir_name))
            if path_exist(dir_path):
                subdirectories[dir_name] = dir_path
    return subdirectories

def has_subfolders(root_path: str) -> bool:
    """Check if the given directory has any subdirectories."""
    for item in os.listdir(root_path):
        if os.path.isdir(os.path.join(root_path, item)):
            return True
    return False

def get_dir_sub_folder_path(folder_path, show_msg:bool=False):
    subdirectories = get_dir_sub_folders(folder_path)
    return subdirectories
    subdirectories = []
    current_root = None
    for root, dirs, files in os.walk(folder_path):
        if not current_root:
            if str(root) == str(folder_path):
                continue
            else:
                current_root = root
                subdirectories.append(current_root)
        elif str(root).startswith(current_root):
            continue
        else:
            current_root = root
            subdirectories.append(current_root)
        if show_msg: print(current_root)
    return subdirectories

def get_dir_sub_folders(path):
    """ 주어진 경로의 바로 아래 있는 모든 하위 폴더 목록을 반환합니다. """
    subdirectories = [join_folder_path(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return subdirectories

def get_subdirectories(path):
    """
    Get a list of immediate subdirectories' absolute paths.

    Parameters:
    - path (str): The path of the directory to get subdirectories from.

    Returns:
    - list: A list of absolute paths of immediate subdirectories.
    """
    # List all entries in the directory
    entries = os.listdir(path)
    
    # Filter out entries that are directories and get their absolute paths
    subdirs = [os.path.join(path, entry) for entry in entries if os.path.isdir(os.path.join(path, entry))]
    
    return subdirs

def sub_path(folder_path):
    subdirectories = []
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            subdirectories.append(os.path.abspath(os.path.join(root, dir_name)))
    return subdirectories

def get_sub_folder_path(folder_path):
    sub_folder_paths = []
    for root, dirs, files in os.walk(folder_path):
        for directory in dirs:
            sub_folder_paths.append(os.path.join(root, directory))
    return sub_folder_paths
def bro_folder_path(folder_path, bro_name:str):
    return join_folder_path(os.path.dirname(folder_path), bro_name)

def move_folder(source_folder, destination_parent, destination_folder_name=None):
    # 이동할 폴더의 이름 추출
    folder_name = os.path.basename(source_folder)
    # 이동할 폴더의 새 경로 생성
    destination_folder = os.path.join(destination_parent, destination_folder_name or folder_name)

    try:
        # 폴더 이동
        shutil.move(source_folder, destination_folder)
        print(f"폴더 이동 완료: {destination_folder}")
    except Exception as e:
        print(f"폴더 이동 실패: {e}")

def delete_folders_by_name(parent_folder, folder_name):
    for root, dirs, files in os.walk(parent_folder):
        for dir_name in dirs:
            if dir_name == folder_name:
                folder_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(folder_path)
                    print(f"폴더 삭제 완료: {folder_path}")
                except Exception as e:
                    print(f"폴더 삭제 실패: {e}")
                    
def create_folders(parent_path, folder_tree):
    """
    입력으로 주어진 폴더 트리 구조를 기반으로 지정한 부모 폴더 아래에 폴더를 일괄적으로 생성합니다.

    Args:
        parent_folder (str): 폴더를 생성할 부모 폴더의 경로.
        folder_tree (dict): 폴더 트리를 표현하는 dict 자료형. key값에 폴더명, value값에 하위폴더명을 가집니다.

    Returns:
        None
    """
    for folder_name, subfolders in folder_tree.items():
        folder_path = os.path.join(parent_path, folder_name)
        create_folder(folder_path)
        # os.makedirs(folder_path, exist_ok=True)
        if isinstance(subfolders, dict):
            create_folders(folder_path, subfolders)

def get_files_info(folder_path, extension='jpg'):
    file_count = 0
    file_size = 0
    files = get_files_path_in_folder_via_ext(folder_path, extension)
    for i, file in enumerate(files):
        file_count += 1
        file_size += os.path.getsize(file)
    return file_count, file_size

def get_size_in_kb(size_in_bytes):
    return size_in_bytes / 1024

def get_size_in_mb(size_in_bytes):
    return size_in_bytes / (1024 * 1024)

def seconds_to_hms(seconds:int|float):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
def seconds_to_ms(seconds:int|float):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"
    # for root, dirs, files in os.walk(folder_path):
    #     for file in files:
    #         file_path = os.path.join(root, file)
    #         file_extension = os.path.splitext(file)[1].lower()

    #         if file_extension == ".mp4":
    #             mp4_count += 1
    #             file_size = os.path.getsize(file_path)
    #             mp4_size += file_size
    #             try:
    #                 clip = VideoFileClip(file_path)
    #                 mp4_length += clip.duration
    #                 clip.close()
    #             except Exception:
    #                 pass

    # return mp4_count, mp4_size, mp4_length

class path_func():

    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.basename = os.path.basename(file_path)
        self.parent_path = os.path.dirname(file_path)
        self.ext = os.path.splitext(os.path.basename(file_path))[1]
        self.file_name = os.path.splitext(os.path.basename(file_path))[0]

    def get_basename(self):
        return self.basename

    def get_parent(self):
        return self.parent_path

    def get_ext(self):
        return self.ext
    
    def rename(self, prefix="", suffix="", ext=""):
        file_name_final = prefix + self.file_name + suffix + '.' + (self.ext if not ext else ext)
        final_path = os.path.join(self.parent_path, file_name_final)
        return final_path

if __name__ == "__main__":
    folder_path = strip_quotes(input("Enter folder path : "))
    delete_folders_by_name(folder_path, 'backup2')