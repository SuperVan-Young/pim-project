import os
import pandas as pd

def get_rpt_list() -> list:
    rpt_list = []
    for root, dirs, files in os.walk("report"):
        for file in files:
            if file.endswith(".rpt"):
                rpt_list.append(os.path.join(root, file))
    return rpt_list

def parse_rpt_name(rpt_file: str) -> dict:
    config = {}
    data = os.path.splitext(os.path.basename(rpt_file))[0].split('-')
    for i, pair in enumerate(data):
        if i == len(data) - 1:
            config['suffix'] = pair
        else:
            key, value = pair.split('_')
            config[key] = value

    return config

def read_rpt(rpt_file: str) -> pd.DataFrame:
    with open(rpt_file, 'r') as f:
        lines = f.readlines()

    data = None
    for line in lines:
        if line.startswith('Average mape val = '):
            data = float(line.split('=')[1])

    return data

def dump_table():
    df = pd.DataFrame(columns=['dist', 'ct', 'suffix', 'sz'])
    for rpt_file in get_rpt_list():
        config = parse_rpt_name(rpt_file)
        data = read_rpt(rpt_file)
        data = pd.DataFrame({
            'sz': [config['sz']],
            'ct': [config['ct']],
            'dist': [config['dist']],
            'suffix': [config['suffix']],
            'mape': [data]
        })
        df = pd.concat([df, data], ignore_index=True)
    df.to_csv('report/table.csv', index=False)

if __name__ == '__main__':
    dump_table()