import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

def _get_bit(value, bit_index):
    # This works for integer-like values
    return (value >> bit_index) & 1

@cocotb.test()
async def test_all_combinations(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    # 1. HARD RESET
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await Timer(200, unit="ns")
    dut.rst_n.value = 1
    await Timer(200, unit="ns")

    for i in range(8):
        dut.ui_in.value = i
        
        # 2. WAIT FOR VALID OUTPUT
        # Wait up to 500ns for the 'X' to go away
        success = False
        for _ in range(50):
            val_str = str(dut.uo_out.value).lower()
            if 'x' not in val_str and 'z' not in val_str:
                success = True
                break
            await Timer(10, unit="ns")

        assert success, f"Input {i:03b} stuck at X: {str(dut.uo_out.value)}"

        # 3. CHECK LOGIC
        A = (i >> 0) & 1
        B = (i >> 1) & 1
        C = (i >> 2) & 1
        
        Fexp = (A & B) | (1 - C)
        Yexp = (1 - C)

        # Convert the LogicArray to int now that we know it has no X
        actual_uo = int(dut.uo_out.value)
        Fgot = _get_bit(actual_uo, 0)
        Ygot = _get_bit(actual_uo, 1)

        assert Fgot == Fexp, f"F error at {i:03b}: exp {Fexp}, got {Fgot}"
        assert Ygot == Yexp, f"Y error at {i:03b}: exp {Yexp}, got {Ygot}"

    dut._log.info("GATE LEVEL SUCCESS!")
