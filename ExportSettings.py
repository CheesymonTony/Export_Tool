import json
import os
import sys
from pathlib import Path
import maya.cmds as mc

class ExportSettings(object):
    def __init__(self, settings_file='exportSettings.json'):
        # Directly use __dict__ to avoid recursion in __setattr__
        self.__dict__['settings_file'] = self._determine_settings_file_path(settings_file)
        self.__dict__['_data'] = {
            'type': '',
            'save_file': True,
            'save_location_type': 'default',
            'save_location': '',
            'import_reference': False,
            'hand_side': '',
            'tool_side': '',
            'time_range': {'start': 0, 'end': 0},
            'clip_type': 'anim',
            'clip_name': '',
            'export_location': '',
        }
        self.load_settings()

    def _determine_settings_file_path(self, filename):
        home_dir = Path(os.getenv('USERPROFILE', os.getenv('HOME', '')))
        if not home_dir:
            print('Error: Unable to determine home directory.')
            sys.exit(1)

        sans_one_drive = home_dir / 'Documents'
        one_drive_dir = home_dir / 'OneDrive' / 'Documents'
        maya_dir_name = 'maya'

        maya_dir = one_drive_dir / maya_dir_name if (one_drive_dir / maya_dir_name).exists() else sans_one_drive / maya_dir_name

        temp_files_dir = maya_dir / 'tempFiles'
        temp_files_dir.mkdir(parents=True, exist_ok=True)

        return temp_files_dir / filename

    def __setattr__(self, key, value):
        if key.startswith('_'):
            # Bypass __setattr__ for private attributes
            self.__dict__[key] = value
        else:
            self._data[key] = value
            self.save_settings()

    def __getattr__(self, item):
        return self._data.get(item, None)

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self._data, f, indent=4)

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                self._data = json.load(f)
        except (IOError, ValueError):
            pass  # Keep default _data if loading fails