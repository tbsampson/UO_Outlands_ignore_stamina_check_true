import os
import sys
import ctypes
import json
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def update_profile_json(directory='C:\\Program Files (x86)\\Ultima Online Outlands'):
    files_found = 0
    files_updated = 0
    updated_files_list = []

    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'profile.json':
                files_found += 1
                file_path = os.path.join(root, file)
                
                try:
                    # Open the JSON file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Check if the key exists and has the value False
                    if 'ignore_stamina_check' in data and not data['ignore_stamina_check']:
                        data['ignore_stamina_check'] = True
                        
                        # Write the updated data back to the file
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=4)
                        
                        files_updated += 1
                        updated_files_list.append(file_path)
                        print(f'Updated ignore_stamina_check to true in {file_path}')
                    else:
                        print(f'No update needed for {file_path}')
                except Exception as e:
                    print(f'Failed to update {file_path}: {e}')

    print(f'\nTotal files found: {files_found}')
    print(f'Total files updated: {files_updated}')
    if files_updated > 0:
        print('\nFiles updated:')
        for file in updated_files_list:
            print(file)

if __name__ == '__main__':
    if is_admin():
        update_profile_json()
    else:
        print("Requesting administrative privileges...")
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
