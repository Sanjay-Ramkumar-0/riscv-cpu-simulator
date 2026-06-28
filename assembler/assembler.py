"""
Simple RISC-V RV64I Assembler

Converts assembly instructions into
32-bit machine instructions.
"""

from utils.helpers import mask64


class Assembler:

    # =====================================
    # R-Type Encoder
    # =====================================

    @staticmethod
    def encode_r(
        funct7,
        rs2,
        rs1,
        funct3,
        rd,
        opcode
    ):

        return (
            ((funct7 & 0x7F) << 25)
            |
            ((rs2 & 0x1F) << 20)
            |
            ((rs1 & 0x1F) << 15)
            |
            ((funct3 & 0x7) << 12)
            |
            ((rd & 0x1F) << 7)
            |
            (opcode & 0x7F)
        )

    # =====================================
    # I-Type Encoder
    # =====================================

    @staticmethod
    def encode_i(
        imm,
        rs1,
        funct3,
        rd,
        opcode
    ):

        imm &= 0xFFF

        return (
            (imm << 20)
            |
            ((rs1 & 0x1F) << 15)
            |
            ((funct3 & 0x7) << 12)
            |
            ((rd & 0x1F) << 7)
            |
            (opcode & 0x7F)
        )

    # =====================================
    # S-Type Encoder
    # =====================================

    @staticmethod
    def encode_s(
        imm,
        rs2,
        rs1,
        funct3,
        opcode
    ):

        imm &= 0xFFF

        imm_low = imm & 0x1F
        imm_high = (imm >> 5) & 0x7F

        return (
            (imm_high << 25)
            |
            ((rs2 & 0x1F) << 20)
            |
            ((rs1 & 0x1F) << 15)
            |
            ((funct3 & 0x7) << 12)
            |
            (imm_low << 7)
            |
            opcode
        )

    # =====================================
    # B-Type Encoder
    # =====================================

    @staticmethod
    def encode_b(
        imm,
        rs2,
        rs1,
        funct3,
        opcode
    ):

        imm &= 0x1FFF

        bit12 = (imm >> 12) & 1
        bit11 = (imm >> 11) & 1
        bits10_5 = (imm >> 5) & 0x3F
        bits4_1 = (imm >> 1) & 0xF

        return (
            (bit12 << 31)
            |
            (bits10_5 << 25)
            |
            ((rs2 & 0x1F) << 20)
            |
            ((rs1 & 0x1F) << 15)
            |
            ((funct3 & 0x7) << 12)
            |
            (bits4_1 << 8)
            |
            (bit11 << 7)
            |
            opcode
        )

    # =====================================
    # ADD
    # =====================================

    @staticmethod
    def add(rd, rs1, rs2):

        return Assembler.encode_r(
            0b0000000,
            rs2,
            rs1,
            0b000,
            rd,
            0b0110011
        )

    # =====================================
    # SUB
    # =====================================

    @staticmethod
    def sub(rd, rs1, rs2):

        return Assembler.encode_r(
            0b0100000,
            rs2,
            rs1,
            0b000,
            rd,
            0b0110011
        )

    # =====================================
    # ADDI
    # =====================================

    @staticmethod
    def addi(rd, rs1, imm):

        return Assembler.encode_i(
            imm,
            rs1,
            0b000,
            rd,
            0b0010011
        )

    # =====================================
    # LD
    # =====================================

    @staticmethod
    def ld(rd, rs1, imm):

        return Assembler.encode_i(
            imm,
            rs1,
            0b011,
            rd,
            0b0000011
        )

    # =====================================
    # SD
    # =====================================

    @staticmethod
    def sd(rs2, rs1, imm):

        return Assembler.encode_s(
            imm,
            rs2,
            rs1,
            0b011,
            0b0100011
        )

    # =====================================
    # BEQ
    # =====================================

    @staticmethod
    def beq(rs1, rs2, offset):

        return Assembler.encode_b(
            offset,
            rs2,
            rs1,
            0b000,
            0b1100011
        )

    # =====================================
    # BNE
    # =====================================

    @staticmethod
    def bne(rs1, rs2, offset):

        return Assembler.encode_b(
            offset,
            rs2,
            rs1,
            0b001,
            0b1100011
        )
    
if __name__ == "__main__":

    print("ADDI")
    print(hex(Assembler.addi(1, 0, 10)))

    print()

    print("ADD")
    print(hex(Assembler.add(3, 1, 2)))

    print()

    print("BEQ +8")
    print(hex(Assembler.beq(1, 0, 8)))

    print()

    print("BEQ -8")
    print(hex(Assembler.beq(1, 0, -8)))