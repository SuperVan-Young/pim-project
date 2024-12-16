import os
import sys
import numpy as np
import pandas as pd
import random
import subprocess
import json
from argparse import ArgumentParser
from itertools import product

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TECH_FILE = os.path.join(PROJECT_ROOT, 'example/45nm_HP.pm')


class PIMArray():
    """
        PIM for dot-product computation using 8T SRAM array
    """

    def __init__(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.rng = random.Random()
        os.makedirs(self.run_dir, exist_ok=True)
        self.sp_file = os.path.join(self.run_dir, 'pim.sp')
        self.lis_file = os.path.join(self.run_dir, 'pim.lis')
    
    def get_circuit_code(self) -> str:
        """
            Generate SPICE code for the SRAM array
        """
        codes = f"""
* SRAM array
"""
        
        for r in range(self.num_row):
            for c in range(self.num_col):
                codes += f"""
* SRAM cell {r}x{c}
M1_{r}_{c} SL_{r}_{c} Q_{r}_{c} N_{r}_{c} 0 NMOS L=45nm W=90nm
M2_{r}_{c} N_{r}_{c} WL_{r} BL_{r}_{c} 0 NMOS L=45nm W=90nm
RBL_{r}_{c} BL_{r}_{c} BL_{r+1}_{c} {self.res_bl}
RSL_{r}_{c} SL_{r}_{c} SL_{r}_{c+1} {self.res_sl}
"""

        for c in range(self.num_col):
            codes += f"""
* Readout BL {c}
Rf_{c} BL_{self.num_row}_{c} 0 {self.res_f}
"""

        return codes

    def get_voltage_code(self) -> str:
        """
            Connect voltage to wires
        """
        codes = f"""
.PARAM VDD={self.volt_vdd}
.PARAM Vbias={self.volt_bias}
"""

        for c in range(self.num_col):
            if self.vi_dist == 'uniform':
                codes += f".PARAM Vin_{c}=UNIF({(self.vi_max+self.vi_min)/2}, {(self.vi_max-self.vi_min)/2})\n"
            elif self.vi_dist == 'worst':
                codes += f".PARAM Vin_{c}={self.vi_max}\n"
            else:
                raise NotImplementedError
            
        for r, c in product(range(self.num_row), range(self.num_col)):
            if self.vw_dist == 'uniform':
                vq = self.volt_vdd if self.rng.random() > 0.5 else 0
                codes += f".PARAM VQ_{r}_{c}={vq}\n"  # TODO: use hspice random integer
            elif self.vw_dist == 'worst':
                codes += f".PARAM VQ_{r}_{c}=VDD\n"
            else:
                raise NotImplementedError

        if self.cell_type == 'A':
            for r in range(self.num_row):
                codes += f"VWL_{r} WL_{r} 0 DC VDD\n"
                codes += f"VSL_{r} SL_{r}_0 0 DC Vin_{r}\n"
            for r, c in product(range(self.num_row), range(self.num_col)):
                codes += f"VQ_{r}_{c} Q_{r}_{c} 0 DC VQ_{r}_{c}\n"
        elif self.cell_type == 'B':
            for r in range(self.num_row):
                codes += f"VWL_{r} WL_{r} 0 DC Vin_{r}\n"
                codes += f"VSL_{r} SL_{r}_0 0 DC Vbias\n"
            for r, c in product(range(self.num_row), range(self.num_col)):
                codes += f"VQ_{r}_{c} Q_{r}_{c} 0 DC VQ_{r}_{c}\n"
        else:
            raise NotImplementedError
        
        return codes

    def get_sp_code(self) -> str:
        """
            Generate SPICE code for the SRAM array
        """
        codes = f"""
* 8 SRAM cells - Static I-V Curve Simulation for Read Port
.options list node post
*
.protect
.INCLUDE '{self.tech_file}'
.unprotect
.options post=2 list
"""
        codes += self.get_voltage_code()
        codes += self.get_circuit_code()
        
        readout = ' '.join(f'I(Rf_{c})' for c in range(self.num_col))

        if self.debug:
            # We sweep Vin_0 for calibration purpose
            codes += f"""
* Simulation
.DC Vin_0 {self.vi_min} {self.vi_max} 0.01
.PRINT {readout}
"""
        else:
            codes += f"""
* Simulation
.DC VDD {self.volt_vdd} {self.volt_vdd} 0.01
.PRINT {readout}
"""
        
        codes += "\n.END\n"
        return codes

    def run_hspice(self) -> None:
        """
            Run HSPICE simulation and return the .lis file
        """

        with open(self.sp_file, 'w') as f:
            f.write(self.get_sp_code())
        subprocess.run(f'hspice -i {self.sp_file} -o {self.lis_file}', shell=True)
        

    def parse_lis_file(self) -> np.array:
        """
            Parse the .lis file and return the result
            Return: np.array, shape=(mc_iter, num_col)
        """

        def parse_unit(s) -> float:
            """
                handle the unit of the readout current
            """
            if 'p' in s:
                return float(s.replace('p', '')) * 1e-12
            elif 'n' in s:
                return float(s.replace('n', '')) * 1e-9
            elif 'u' in s:
                return float(s.replace('u', '')) * 1e-6
            elif 'm' in s:
                return float(s.replace('m', '')) * 1e-3
            else:
                return float(s)

        results = []

        with open(self.lis_file, 'r') as f:
            line = ''
            while True:
                line = f.readline()
                if line.strip() == 'x': break
            for _ in range(3): f.readline()

            line = ''
            while True:
                line = f.readline()
                if line.strip() == 'y': break
                cur_result = line.split()
                cur_result = [parse_unit(s) for s in cur_result][1:]
                results.append(np.array(cur_result))
            
        return np.stack(results, axis=0)

    
    def calc_error_rate(self) -> float:
        """
            Calculate the average error rate
        """
        pass


def parse_args():
    parser = ArgumentParser()

    # run configs
    parser.add_argument('--run_dir', type=str, default='./run_test', help='run directory')
    parser.add_argument('--mc_iter', type=int, default=0, help='monte-carlo iteration')
    parser.add_argument('--debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--irbl_unit', type=float, default=1, help='readout current unit for linear interpolation')

    # tech file (you should specify random parameters accordingly, e.g. vth)
    parser.add_argument('--tech_file', type=str, default=TECH_FILE, help='technology file')
    
    # array config
    parser.add_argument('--cell_type', type=str, default='A', help='cell type')
    parser.add_argument('--num_row', type=int, default=1, help='number of rows')
    parser.add_argument('--num_col', type=int, default=1, help='number of columns')
    parser.add_argument('--res_sl', type=float, default=0., help='resistance on SL between cells') # TODO: add resistance on SL
    parser.add_argument('--res_bl', type=float, default=0., help='resistance on BL between cells') # TODO: add resistance on BL
    parser.add_argument('--res_f', type=float, default=50., help='readout resistance')
    parser.add_argument('--volt_vdd', type=float, default=0.65, help='supply voltage for VDD')
    parser.add_argument('--volt_bias', type=float, default=0.65, help='supply voltage for bias')

    # input voltage range (deemed as linear region)
    parser.add_argument('--vi_min', type=float, default=0., help='minimum input voltage')
    parser.add_argument('--vi_max', type=float, default=0.65, help='maximum input voltage')
    parser.add_argument('--vi_dist', type=str, default='worst', help='input voltage distribution')
    parser.add_argument('--vw_dist', type=str, default='worst', help='weight voltage distribution')

    # opamp config
    parser.add_argument('--use_opamp', type=bool, default=False, help='use opamp')
    parser.add_argument('--volt_pos', type=float, default=0.10, help='supply voltage for pos')

    # extra arguments from json
    parser.add_argument('--extra_args', type=str, default=None, help='extra arguments from json')

    args = parser.parse_args()
    kwargs = vars(args)

    if os.path.exists(args.extra_args):
        with open(args.extra_args, 'r') as f:
            extra_args = json.load(f)
        kwargs.update(extra_args)

    return kwargs


if __name__ == '__main__':
    kwargs = parse_args()
    pim = PIMArray(kwargs)
    pim.run_hspice()
    print(pim.parse_lis_file())