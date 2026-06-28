"""
5-Stage Pipeline

IF
ID
EX
MEM
WB

Single Thread
Single Issue
"""

from isa.decoder import Decoder
from execution.alu import ALU
from execution.branch_unit import BranchUnit
from cpu.hazard_unit import HazardUnit
from cpu.forwarding_unit import ForwardingUnit


class Pipeline:

    def __init__(self, cpu):

        self.cpu = cpu

        # Current Pipeline Registers

        self.IF_ID = None
        self.ID_EX = None
        self.EX_MEM = None
        self.MEM_WB = None

        # Next Pipeline Registers

        self.next_IF_ID = None
        self.next_ID_EX = None
        self.next_EX_MEM = None
        self.next_MEM_WB = None

        self.cycle_count = 0

        # Hazard / Stall Control

        self.stall = False

        # ----------------------------
        # Branch Control
        # ----------------------------

        self.flush = False
        self.branch_target = None

        # ---------------------------------
        # Branch Prediction
        # ---------------------------------

        self.prediction = False
        self.predicted_target = None
        self.prediction_correct = True

        # ---------------------------------
        # Branch Prediction Statistics
        # ---------------------------------

        self.total_predictions = 0
        self.correct_predictions = 0
        self.mispredictions = 0

    # =====================================
    # IF
    # =====================================

    def IF(self):

        # Don't fetch during stall
        if self.stall:
            return

        # Don't fetch during flush
        if self.flush:
            return

        thread = self.cpu.threads[0]

        pc = thread.get_pc()

        print(
            f"FETCH PC = 0x{pc:08X}"
        )

        inst = self.cpu.icache.read32(pc)

        # ---------------------------------
        # Branch Prediction
        # ---------------------------------

        prediction = False
        predicted_target = None

        if Decoder.is_branch(inst):

            prediction = self.cpu.predictor.predict(pc)

            if prediction:

                predicted_target = self.cpu.btb.lookup(pc)

                if predicted_target is not None:

                    print(
                        f"PREDICT: TAKEN -> 0x{predicted_target:08X}"
                    )

                else:

                    print(
                        "PREDICT: TAKEN (BTB MISS)"
                    )

            else:

                print(
                    "PREDICT: NOT TAKEN"
                )

        # ---------------------------------
        # Save into IF/ID Pipeline Register
        # ---------------------------------

        self.next_IF_ID = {

            "pc": pc,

            "inst": inst,

            "prediction": prediction,

            "predicted_target": predicted_target

        }

        # ---------------------------------
        # Speculative Fetch
        # ---------------------------------

        if prediction and predicted_target is not None:

            thread.set_pc(
                predicted_target
            )

        else:

            thread.advance_pc()

    # =====================================
    # ID
    # =====================================

    def ID(self):

        self.stall = False

        if self.IF_ID is None:
            return

        inst = self.IF_ID["inst"]

        if inst == 0:
            return

        decoded = Decoder.decode(inst)

        # ---------------------------------
        # Hazard Detection
        # ---------------------------------

        if HazardUnit.has_raw_hazard(
            decoded,
            self.ID_EX,
            self.EX_MEM,
            self.MEM_WB
        ):

            print(
                f"STALL: RAW Hazard on {decoded['op']}"
            )

            self.stall = True

            # Freeze IF/ID

            self.next_IF_ID = self.IF_ID

            # Bubble

            self.next_ID_EX = None

            return

        # ---------------------------------
        # Normal Decode
        # ---------------------------------

        thread = self.cpu.threads[0]

        rs1_val = 0
        rs2_val = 0

        if decoded["rs1"] is not None:

            rs1_val = thread.read_reg(
                decoded["rs1"]
            )

        if decoded["rs2"] is not None:

            rs2_val = thread.read_reg(
                decoded["rs2"]
            )

        self.next_ID_EX = {

            "pc": self.IF_ID["pc"],

            "decoded": decoded,

            "rs1_val": rs1_val,

            "rs2_val": rs2_val,

            "prediction": self.IF_ID["prediction"],

            "predicted_target": self.IF_ID["predicted_target"]

        }

    # =====================================
    # EX
    # =====================================

    def EX(self):

        if self.ID_EX is None:
            return

        decoded = self.ID_EX["decoded"]

        op = decoded["op"]

        # ----------------------------------
        # Original values from ID stage
        # ----------------------------------

        rs1_val = self.ID_EX["rs1_val"]
        rs2_val = self.ID_EX["rs2_val"]

        # ----------------------------------
        # Forwarding
        # ----------------------------------

        rs1_reg = decoded.get("rs1")
        rs2_reg = decoded.get("rs2")

        rs1_val = ForwardingUnit.forward_operand(
            rs1_reg,
            rs1_val,
            self.EX_MEM,
            self.MEM_WB
        )

        rs2_val = ForwardingUnit.forward_operand(
            rs2_reg,
            rs2_val,
            self.EX_MEM,
            self.MEM_WB
        )

        result = None

        # ----------------------------------
        # ADD
        # ----------------------------------

        if op == "ADD":

            result = ALU.execute(
                "ADD",
                rs1_val,
                rs2_val
            )

        # ----------------------------------
        # SUB
        # ----------------------------------

        elif op == "SUB":

            result = ALU.execute(
                "SUB",
                rs1_val,
                rs2_val
            )

        # ----------------------------------
        # ADDI
        # ----------------------------------

        elif op == "ADDI":

            result = ALU.execute(
                "ADD",
                rs1_val,
                decoded["imm"]
            )
            
        # ----------------------------------
        # Branch Instructions
        # ----------------------------------

        elif op in {

            "BEQ",
            "BNE",
            "BLT",
            "BGE",
            "BLTU",
            "BGEU"

        }:

            print(
                f"EX: PC=0x{self.ID_EX['pc']:08X}, "
                f"IMM={decoded['imm']}, "
                f"RS1={rs1_val}, "
                f"RS2={rs2_val}"
            )

            taken, target = BranchUnit.execute(

                op,

                self.ID_EX["pc"],

                rs1_val,

                rs2_val,

                decoded["imm"]

            )

            # For debugging
            if taken:

                print(
                    f"BRANCH TAKEN -> 0x{target:08X}"
                )

            else:

                print(
                    "BRANCH NOT TAKEN"
                )

            # Resolve prediction
            self.resolve_branch(

                self.ID_EX,

                taken,

                target

            )

            # Pass through pipeline

            self.next_EX_MEM = {

                "decoded": decoded,

                "result": None

            }

            return
        # ----------------------------------
        # LD
        # ----------------------------------

        elif op == "LD":

            addr = (
                rs1_val +
                decoded["imm"]
            )

            self.next_EX_MEM = {
                "decoded": decoded,
                "addr": addr
            }

            return

        # ----------------------------------
        # SD
        # ----------------------------------

        elif op == "SD":

            addr = (
                rs1_val +
                decoded["imm"]
            )

            self.next_EX_MEM = {
                "decoded": decoded,
                "addr": addr,
                "store_value": rs2_val
            }

            return

                # ----------------------------------
                # Pass to MEM
                # ----------------------------------

        self.next_EX_MEM = {
            "decoded": decoded,
            "result": result
        }

        # =====================================
        # MEM
        # =====================================

    def MEM(self):

        if self.EX_MEM is None:
            return

        decoded = self.EX_MEM["decoded"]

        op = decoded["op"]

        # ==================================
        # LD
        # ==================================

        if op == "LD":

            addr = self.EX_MEM["addr"]

            value = self.cpu.dcache.read64(
                addr
            )

            self.next_MEM_WB = {
                "decoded": decoded,
                "result": value
            }

        # ==================================
        # SD
        # ==================================

        elif op == "SD":

            addr = self.EX_MEM["addr"]

            value = self.EX_MEM[
                "store_value"
            ]

            self.cpu.dcache.write64(
                addr,
                value
            )

            self.next_MEM_WB = {
                "decoded": decoded,
                "result": None
            }

        # ==================================
        # ALU Instructions
        # ==================================

        else:

            self.next_MEM_WB = self.EX_MEM
    # =====================================
    # WB
    # =====================================

    def WB(self):

        if self.MEM_WB is None:
            return

        decoded = self.MEM_WB["decoded"]

        result = self.MEM_WB["result"]

        rd = decoded["rd"]

        if rd is not None:

            thread = self.cpu.threads[0]

            thread.write_reg(
                rd,
                result
            )

            print(
                f"WB: {decoded['op']} -> x{rd} = {result}"
            )

    # =====================================
    # Branch Resolution
    # =====================================

    def resolve_branch(
        self,
        branch_info,
        taken,
        target
    ):

        # ---------------------------------
        # Information from pipeline register
        # ---------------------------------

        pc = branch_info["pc"]

        prediction = branch_info["prediction"]

        predicted_target = branch_info["predicted_target"]

        # ---------------------------------
        # Update Branch Predictor
        # ---------------------------------

        print(
            f"RESOLVE: PC=0x{pc:08X}, "
            f"TARGET=0x{target:08X}, "
            f"TAKEN={taken}"
        )

        self.cpu.predictor.update(
            pc,
            taken
        )

        # ---------------------------------
        # Update Branch Target Buffer
        # ---------------------------------

        if taken:

            self.cpu.btb.update(
                pc,
                target
            )

        # ---------------------------------
        # Prediction Correct?
        # ---------------------------------

        prediction_correct = (

            prediction == taken
            and
            (
                not taken
                or
                predicted_target == target
            )
        )

        # ---------------------------------
        # Statistics
        # ---------------------------------

        self.total_predictions += 1

        # Future:
        # if prediction was TAKEN,
        # also compare predicted_target
        # with actual target.

        if prediction_correct:

            self.correct_predictions += 1

            print(
                "BRANCH PREDICTION CORRECT"
            )

            return

        # ---------------------------------
        # Branch Misprediction
        # ---------------------------------
        self.mispredictions += 1
        print(
            "BRANCH MISPREDICTION"
        )

        self.flush = True

        if taken:

            self.branch_target = target

        else:

            self.branch_target = pc + 4

    # =====================================
    # Branch Prediction Statistics
    # =====================================

    def print_branch_statistics(self):

        print("\n========== Branch Prediction ==========")

        print(
            f"Total Predictions : {self.total_predictions}"
        )

        print(
            f"Correct           : {self.correct_predictions}"
        )

        print(
            f"Mispredictions    : {self.mispredictions}"
        )

        if self.total_predictions > 0:

            accuracy = (

                self.correct_predictions
                /
                self.total_predictions

            ) * 100

            print(
                f"Accuracy          : {accuracy:.2f}%"
            )

        else:

            print(
                "Accuracy          : N/A"
            )

        print("=======================================\n")

    # =====================================
    # Commit
    # =====================================

    def commit(self):

        # ------------------------------------
        # Branch Flush
        # ------------------------------------

        if self.flush:

            thread = self.cpu.threads[0]

            # Redirect PC
            thread.set_pc(
                self.branch_target
            )

            # Flush wrong instructions
            self.IF_ID = None
            self.ID_EX = None

            # Keep older instructions
            self.EX_MEM = self.next_EX_MEM
            self.MEM_WB = self.next_MEM_WB

            print(
                "PIPELINE FLUSH"
            )

            # Reset control signals
            self.flush = False
            self.branch_target = None

        else:

            self.IF_ID = self.next_IF_ID
            self.ID_EX = self.next_ID_EX
            self.EX_MEM = self.next_EX_MEM
            self.MEM_WB = self.next_MEM_WB

        self.next_IF_ID = None
        self.next_ID_EX = None
        self.next_EX_MEM = None
        self.next_MEM_WB = None

    # =====================================
    # One Cycle
    # =====================================

    def cycle(self):

        self.cycle_count += 1

        print(
            f"\n===== Cycle {self.cycle_count} ====="
        )

        self.WB()
        self.MEM()
        self.EX()
        self.ID()
        self.IF()

        self.commit()


# =====================================
# Test - Repeated Branch Prediction
# =====================================

if __name__ == "__main__":

    from cpu.cpu import CPU

    cpu = CPU()

    # ---------------------------------
    # Register Setup
    # ---------------------------------

    # x1 == x0
    # Therefore BEQ is ALWAYS TAKEN

    cpu.threads[0].write_reg(
        1,
        0
    )

    # ---------------------------------
    # Program
    #
    # 0x00 : BEQ x1,x0,+8
    # 0x04 : ADDI x2,x2,1
    # 0x08 : BEQ x1,x0,-8
    #
    # Infinite Loop
    # ---------------------------------

    # BEQ x1,x0,+8
    cpu.memory.write32(
        0,
        0x00008463
    )

    # ADDI x2,x2,1
    cpu.memory.write32(
        4,
        0x00110113
    )

    # BEQ x1,x0,-8
    cpu.memory.write32(
        8,
        0xFE008CE3
    )

    pipe = Pipeline(cpu)

    # ---------------------------------
    # Run Many Cycles
    # ---------------------------------

    for _ in range(60):

        pipe.cycle()

    print("\nRegisters")

    print(
        "x2 =",
        cpu.threads[0].read_reg(2)
    )

    pipe.print_branch_statistics()

    print("\nPredictor State")

    cpu.predictor.dump()