import gc
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE

def _find_plugin():
    for o in gc.get_objects():
        try:
            if "uEmuPlugin" in [c.__name__ for c in type(o).__mro__]:
                return o
        except Exception:
            continue
    return None

def get_uc():
    plug = _find_plugin()
    if plug is None:
        raise RuntimeError("Инстанс uEmu не найден — загружен ли uEmu?")
    mu = getattr(getattr(plug, "unicornEngine", None), "mu", None)
    if mu is None:
        raise RuntimeError("Uc == None — сначала нажми Start в uEmu.")
    return mu

def ensure_mapped(uc, base, size=0x1000):
    start = base & ~0xFFF
    for b, e, _ in uc.mem_regions():
        if b <= start <= e:
            return                      # страница уже замаплена
    uc.mem_map(start, ((size + 0xFFF) & ~0xFFF) or 0x1000)

def read_const(uc, addr, width, value):
    """Чтение из [addr, addr+width) всегда возвращает value."""
    def _cb(uc, access, address, size, val, ud):
        masked = value & ((1 << (size * 8)) - 1)
        uc.mem_write(address, masked.to_bytes(size, "little"))
    uc.hook_add(UC_HOOK_MEM_READ, _cb, begin=addr, end=addr + width - 1)

def log_writes(uc, addr, width, name="dev"):
    def _cb(uc, access, address, size, value, ud):
        print("[%s] WRITE %#010x = %#x (size %d)" % (name, address, value, size))
    uc.hook_add(UC_HOOK_MEM_WRITE, _cb, begin=addr, end=addr + width - 1)
