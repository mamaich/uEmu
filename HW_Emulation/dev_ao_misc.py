from emu_hw import get_uc, ensure_mapped, read_const, log_writes

def install():
    uc = get_uc()
    ensure_mapped(uc, 0xFF800000)            # AO-страница
    read_const(uc, 0xFF800228, 4, 0xFFFF)    # устройство @0xFF800228 -> 0xFFFF
    log_writes(uc, 0xFF800228, 4, "AO_0228") # пока просто логируем записи
    print("[dev_ao_misc] installed")

install()
