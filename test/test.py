import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

@cocotb.test()
async def test_all_combinations(dut):
    # Start a clock (safe for template)
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    # Initialize
    dut.ena.value = 1
    dut.rst_n.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    await Timer(20, unit="ns")

    # Iterate all 8 combinations: ui_in[2:0] = C B A (bit2 bit1 bit0)
    for i in range(8):
        # Drive inputs: A=bit0, B=bit1, C=bit2
        dut.ui_in.value = i
        await Timer(20, unit="ns")  # settle

        A = (i >> 0) & 1
        B = (i >> 1) & 1
        C = (i >> 2) & 1

        Cn = 1 - C
        Fexp = (A & B) | Cn      # F = AB + C'
        Yexp = Cn                # Y = C'

        uo = int(dut.uo_out.value)
        Fgot = (uo >> 0) & 1
        Ygot = (uo >> 1) & 1

        assert Fgot == Fexp, f"Input {i:03b} (A={A},B={B},C={C}) F got={Fgot} exp={Fexp}"
        assert Ygot == Yexp, f"Input {i:03b} (A={A},B={B},C={C}) Y got={Ygot} exp={Yexp}"
