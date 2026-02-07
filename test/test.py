import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

def all_01(s: str) -> bool:
    s = s.lower().replace("_", "")
    return all(c in "01" for c in s)

@cocotb.test()
async def test_all_combinations(tb):
    cocotb.start_soon(Clock(tb.clk, 10, unit="ns").start())

    tb.ena.value = 1
    tb.rst_n.value = 1
    tb.uio_in.value = 0
    tb.ui_in.value = 0

    # extra settle time for gate-level + unit delays
    await Timer(500, unit="ns")

    for i in range(8):
        tb.ui_in.value = i
        await Timer(200, unit="ns")

        A = (i >> 0) & 1
        B = (i >> 1) & 1
        C = (i >> 2) & 1

        Cn = 1 - C
        Fexp = (A & B) | Cn
        Yexp = Cn

        # wait until outputs are not X/Z
        ok = False
        for _ in range(300):
            if all_01(str(tb.uo_out.value)):
                ok = True
                break
            await Timer(10, unit="ns")

        assert ok, f"uo_out stayed X/Z at input {i:03b}: {str(tb.uo_out.value)}"

        uo = int(tb.uo_out.value)
        Fgot = (uo >> 0) & 1
        Ygot = (uo >> 1) & 1

        assert Fgot == Fexp, f"Input {i:03b} F got={Fgot} exp={Fexp}"
        assert Ygot == Yexp, f"Input {i:03b} Y got={Ygot} exp={Yexp}"
