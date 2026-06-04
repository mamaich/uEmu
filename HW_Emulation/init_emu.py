import sys
sys.path.insert(0, r"T:\Dump\tool\uEmu\HW_Emulation")     # папка с emu_hw.py и dev_*.py — один раз

import importlib, emu_hw, dev_ao_misc
importlib.reload(emu_hw)                   # если правил хелпер
importlib.reload(dev_ao_misc)              # перечитывает файл и заново зовёт install()
