import os
import json
from itertools import product

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_ROOT = os.path.join(PROJECT_ROOT, 'config')
RUN_ROOT = os.path.join(PROJECT_ROOT, 'run')

SZ_LIST = [4, 8, 16, 32]
CT_LIST = ['A', 'B']
DIST_LIST = ['worst']

def gen_base_configs():
    for sz, ct, dist in product(SZ_LIST, CT_LIST, DIST_LIST):
        if ct == 'A':
            vi_min, vi_max = 0, 0.15
            irbl_unit = 12.6757e-6
        elif ct == 'B':
            vi_min, vi_max = 0.45, 0.65
            irbl_unit = 18.7875e-6
        else:
            raise ValueError(f'Unknown computing type {ct}')
        
        config_name = f'sz_{sz}-ct_{ct}-dist_{dist}-base'

        config = {
            'run_dir': os.path.join(RUN_ROOT, config_name),
            'extra_args': os.path.join(CONFIG_ROOT, f'{config_name}.json'),
            'num_row': sz,
            'num_col': sz,
            'vi_min': vi_min,
            'vi_max': vi_max,
            'vi_dist': dist,
            'vw_dist': dist,
            'irbl_unit': irbl_unit,
        }
        with open(os.path.join(CONFIG_ROOT, f'{config_name}.json'), 'w') as f:
            json.dump(config, f, indent=4)


def gen_res_configs():
    for sz, ct, dist in product(SZ_LIST, CT_LIST, DIST_LIST):
        if ct == 'A':
            vi_min, vi_max = 0, 0.15
            irbl_unit = 12.6757e-6
        elif ct == 'B':
            vi_min, vi_max = 0.45, 0.65
            irbl_unit = 18.7875e-6
        else:
            raise ValueError(f'Unknown computing type {ct}')
        
        config_name = f'sz_{sz}-ct_{ct}-dist_{dist}-res'

        config = {
            'run_dir': os.path.join(RUN_ROOT, config_name),
            'extra_args': os.path.join(CONFIG_ROOT, f'{config_name}.json'),
            'num_row': sz,
            'num_col': sz,
            'vi_min': vi_min,
            'vi_max': vi_max,
            'vi_dist': dist,
            'vw_dist': dist,
            'irbl_unit': irbl_unit,
            'res_sl': 1.25,
            'res_bl': 2.5,
        }
        with open(os.path.join(CONFIG_ROOT, f'{config_name}.json'), 'w') as f:
            json.dump(config, f, indent=4)


def gen_pvt_configs():
    for sz, ct, dist in product(SZ_LIST, CT_LIST, DIST_LIST):
        if ct == 'A':
            vi_min, vi_max = 0, 0.15
            irbl_unit = 12.6757e-6
        elif ct == 'B':
            vi_min, vi_max = 0.45, 0.65
            irbl_unit = 18.7875e-6
        else:
            raise ValueError(f'Unknown computing type {ct}')
        
        config_name = f'sz_{sz}-ct_{ct}-dist_{dist}-pvt'

        config = {
            'run_dir': os.path.join(RUN_ROOT, config_name),
            'tech_file': os.path.join(PROJECT_ROOT, 'example/45nm_HP_mc.pm'),
            'extra_args': os.path.join(CONFIG_ROOT, f'{config_name}.json'),
            'num_row': sz,
            'num_col': sz,
            'vi_min': vi_min,
            'vi_max': vi_max,
            'vi_dist': dist,
            'vw_dist': dist,
            'irbl_unit': irbl_unit,
            'res_sl': 1.25,
            'res_bl': 2.5,
        }
        with open(os.path.join(CONFIG_ROOT, f'{config_name}.json'), 'w') as f:
            json.dump(config, f, indent=4)

if __name__ == '__main__':
    os.makedirs(CONFIG_ROOT, exist_ok=True)
    gen_base_configs()
    gen_res_configs()
    gen_pvt_configs()