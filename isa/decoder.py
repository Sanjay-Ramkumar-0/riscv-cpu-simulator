"""
decodes the data from memory. For example cpu sees 0x00C585B3 as 00000000110001011000010110110011, but the decoder decodes it into {"op":"ADD", "rd":11, "rs1":11, "rs2":12,"imm":None}. The format is 
31-----25 24---20 19---15 14--12 11---7 6----0
funct7     rs2     rs1    f3      rd    opcode
each thread has 32 registers, 2^5, that's why rs1,rs2,rd are 5 bits

R-Type (ADD, SUB, AND, OR, XOR, MUL, DIV), format:
31-----25 24---20 19---15 14--12 11---7 6----0
funct7     rs2     rs1    f3      rd    opcode

I-Type (ADDI, LD, JALR), format:
31-------------20 19---15 14--12 11---7 6----0
imm[11:0]        rs1      f3      rd    opcode

S-Type (SD, SW, SH, SB), format:
31-----25 24---20 19---15 14--12 11---7 6----0
imm[11:5] rs2     rs1    f3   imm[4:0] opcode

B-Type (BEQ, BNE, BLT, BGE), format:
31    30---25 24---20 19---15 14--12 11---8 7 6----0
imm12 imm10:5 rs2     rs1    f3   imm4:1 imm11 opcode

U-Type (LUI, AUIPC), format:
31----------------12 11---7 6----0
imm[31:12]          rd    opcode

J-Type (JAL), format:
31 30--------21 20 19----------12 11---7 6----0
imm20 imm10:1 imm11 imm19:12     rd    opcode


"""

from utils.helpers import (
    get_bits,
    sign_extend
)


class Decoder:

    @staticmethod
    def decode_b_imm(inst: int) -> int:

        imm = (
            (get_bits(inst, 31, 31) << 12)
            |
            (get_bits(inst, 7, 7) << 11)
            |
            (get_bits(inst, 30, 25) << 5)
            |
            (get_bits(inst, 11, 8) << 1)
        )

        return sign_extend(imm, 13)

    @staticmethod
    def decode_u_imm(inst: int) -> int:

        return get_bits(inst, 31, 12) << 12

    @staticmethod
    def decode_j_imm(inst: int) -> int:

        imm = (
            (get_bits(inst, 31, 31) << 20)
            |
            (get_bits(inst, 19, 12) << 12)
            |
            (get_bits(inst, 20, 20) << 11)
            |
            (get_bits(inst, 30, 21) << 1)
        )

        return sign_extend(imm, 21)

    @staticmethod
    def is_branch(inst: int) -> bool:
        """
        Returns True if the instruction is a control-flow instruction.
        Used by the IF stage for branch prediction.
        """

        opcode = get_bits(inst, 6, 0)

        return opcode in {

            0b1100011,   # BEQ/BNE/BLT/BGE/BLTU/BGEU

            0b1101111,   # JAL

            0b1100111    # JALR (future)

        }

    @staticmethod
    def decode(inst: int) -> dict:

        opcode = get_bits(inst, 6, 0)
        rd = get_bits(inst, 11, 7)
        funct3 = get_bits(inst, 14, 12)
        rs1 = get_bits(inst, 19, 15)
        rs2 = get_bits(inst, 24, 20)
        funct7 = get_bits(inst, 31, 25)

        # ----------------------------------------
        # R-Type
        # ----------------------------------------

        if (
            opcode == 0b0110011 and
            funct3 == 0b000 and
            funct7 == 0b0000000
        ):
            return {
                "op": "ADD",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }

        elif (
            opcode == 0b0110011 and
            funct3 == 0b000 and
            funct7 == 0b0100000
        ):
            return {
                "op": "SUB",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }
        elif (
            opcode == 0b0110011 and
            funct3 == 0b100 and
            funct7 == 0b0000000
        ):
            return {
                "op": "XOR",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }
        elif (
            opcode == 0b0110011 and
            funct3 == 0b001 and
            funct7 == 0b0000000
        ):
            return {
                "op": "SLL",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }
        elif (
            opcode == 0b0110011 and
            funct3 == 0b101 and
            funct7 == 0b0000000
        ):
            return {
                "op": "SRL",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }
        elif (
            opcode == 0b0110011 and
            funct3 == 0b101 and
            funct7 == 0b0100000
        ):
            return {
                "op": "SRA",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }
        elif (
            opcode == 0b0110011 and
            funct3 == 0b010 and
            funct7 == 0b0000000
        ):
            return {
                "op": "SLT",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }
        elif (
            opcode == 0b0110011 and
            funct3 == 0b011 and
            funct7 == 0b0000000
        ):
            return {
                "op": "SLTU",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }
        elif (
            opcode == 0b0110011 and
            funct3 == 0b000 and
            funct7 == 0b0000001
        ):
            return {
                "op": "MUL",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }
        elif (
            opcode == 0b0110011 and
            funct3 == 0b100 and
            funct7 == 0b0000001
        ):
            return {
                "op": "DIV",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }
        elif (
            opcode == 0b0110011 and
            funct3 == 0b110 and
            funct7 == 0b0000001
        ):
            return {
                "op": "REM",
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }
        # ----------------------------------------
        # I-Type
        # ----------------------------------------

        imm_i = sign_extend(
            get_bits(inst, 31, 20),
            12
        )

        if (
            opcode == 0b0010011 and
            funct3 == 0b000
        ):
            return {
                "op": "ADDI",
                "rd": rd,
                "rs1": rs1,
                "rs2": None,
                "imm": imm_i
            }

        elif (
            opcode == 0b0000011 and
            funct3 == 0b011
        ):
            return {
                "op": "LD",
                "rd": rd,
                "rs1": rs1,
                "rs2": None,
                "imm": imm_i
            }

        # ----------------------------------------
        # S-Type
        # ----------------------------------------

        imm_s = (
            (get_bits(inst, 31, 25) << 5)
            |
            get_bits(inst, 11, 7)
        )

        imm_s = sign_extend(imm_s, 12)

        if (
            opcode == 0b0100011 and
            funct3 == 0b011
        ):
            return {
                "op": "SD",
                "rd": None,
                "rs1": rs1,
                "rs2": rs2,
                "imm": imm_s
            }

        # ----------------------------------------
        # B-Type
        # ----------------------------------------

        imm_b = Decoder.decode_b_imm(inst)

        if (
            opcode == 0b1100011 and
            funct3 == 0b000
        ):
            return {
                "op": "BEQ",
                "rd": None,
                "rs1": rs1,
                "rs2": rs2,
                "imm": imm_b
            }

        elif (
            opcode == 0b1100011 and
            funct3 == 0b001
        ):
            return {
                "op": "BNE",
                "rd": None,
                "rs1": rs1,
                "rs2": rs2,
                "imm": imm_b
            }

        elif (
            opcode == 0b1100011 and
            funct3 == 0b100
        ):
            return {
                "op": "BLT",
                "rd": None,
                "rs1": rs1,
                "rs2": rs2,
                "imm": imm_b
            }

        elif (
            opcode == 0b1100011 and
            funct3 == 0b101
        ):
            return {
                "op": "BGE",
                "rd": None,
                "rs1": rs1,
                "rs2": rs2,
                "imm": imm_b
            }

        elif (
            opcode == 0b1100011 and
            funct3 == 0b110
        ):
            return {
                "op": "BLTU",
                "rd": None,
                "rs1": rs1,
                "rs2": rs2,
                "imm": imm_b
            }

        elif (
            opcode == 0b1100011 and
            funct3 == 0b111
        ):
            return {
                "op": "BGEU",
                "rd": None,
                "rs1": rs1,
                "rs2": rs2,
                "imm": imm_b
            }

        # ----------------------------------------
        # J-Type
        # ----------------------------------------

        imm_j = Decoder.decode_j_imm(inst)

        if opcode == 0b1101111:

            return {
                "op": "JAL",
                "rd": rd,
                "rs1": None,
                "rs2": None,
                "imm": imm_j
            }

        # ----------------------------------------
        # U-Type
        # ----------------------------------------

        imm_u = Decoder.decode_u_imm(inst)

        if opcode == 0b0110111:

            return {
                "op": "LUI",
                "rd": rd,
                "rs1": None,
                "rs2": None,
                "imm": imm_u
            }

        elif opcode == 0b0010111:

            return {
                "op": "AUIPC",
                "rd": rd,
                "rs1": None,
                "rs2": None,
                "imm": imm_u
            }

        raise ValueError(
            f"Unknown instruction: 0x{inst:08X}"
        )