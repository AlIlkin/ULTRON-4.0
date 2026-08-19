import traceback
import sys
import os

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import action_engine as act

locations = ['Moscow', 'London', None]
for loc in locations:
    try:
        print('---')
        print('Location:', loc)
        print(act.get_time(loc))
    except Exception:
        print('Error for', loc)
        traceback.print_exc()
