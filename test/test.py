import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

@cocotb.test()
async def test_all_combinations(dut):
    # Clock (not required logically, but safe for template)
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    # Init
    dut.ena.value = 1
    dut.rst_n.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    await Timer(20, unit="ns")

    for A in [0, 1]:
        for B in [0, 1]:
            for C in [0, 1]:
                # Drive ui_in as a full 8-bit value (A->bit0, B->bit1, C->bit2)
                val = (A << 0) | (B << 1) | (C << 2)
                dut.ui_in.value = val

                await Timer(20, unit="ns")  # settle

                Cn = 1 - C
                Fexp = (A & B) | Cn
                Yexp = Cn

                uo = int(dut.uo_out.value)
                F
