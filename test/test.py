import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_all_combinations(dut):
    # Start a clock (even though design is combinational)
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Reset-like init
    dut.ena.value = 1
    dut.rst_n.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 1)

    # Loop through all A,B,C combinations (bits 0..2)
    for A in [0, 1]:
        for B in [0, 1]:
            for C in [0, 1]:
                dut.ui_in[0].value = A
                dut.ui_in[1].value = B
                dut.ui_in[2].value = C
                await ClockCycles(dut.clk, 1)

                Cn = 1 - C
                Fexp = (A & B) | Cn
                Yexp = Cn

                assert int(dut.uo_out[0].value) == Fexp, f"F mismatch A,B,C={A}{B}{C}"
                assert int(dut.uo_out[1].value) == Yexp, f"Y mismatch A,B,C={A}{B}{C}"
