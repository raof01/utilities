# -*- coding: utf-8 -*-
import xlrd
import pandas as pd
from datetime import datetime
from pathlib2 import Path
import matplotlib.pyplot as plt


def xl_date_to_date_str(d, mode):
    return datetime.strptime(
        str(datetime(*xlrd.xldate_as_tuple(d, mode)))[:10], '%Y-%m-%d')

def append_to_csv(df, file_name):
    f = Path(file_name)
    if not f.exists():
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        with open(file_name, 'a') as output:
            df.to_csv(output, header=False, index=False, encoding='utf-8-sig')

def get_running_sum(ds):
    running_sum = [ds[0]]
    for i in range(1, bc.size):
        running_sum.append(bc[i] + running_sum[i-1])
    return running_sum

file_name = 'wacai_2016-11-2017-07.xls'
car_cost_file_name = 'car-cost.csv'
baby_cost_file_name = 'baby-cost.csv'
car_cost_cata = ['加油', '停车费', '过路过桥', '保养维修', '车款车贷', '罚款赔偿', '车险','驾照费用']
# load cost data to data frame
workbook = xlrd.open_workbook(file_name)
sheet = workbook.sheet_by_name('支出')
cata_l1 = [sheet.col(0)[i].value for i in range(1, sheet.nrows)]
cata_l2 = [sheet.col(1)[i].value for i in range(1, sheet.nrows)]
date = [xl_date_to_date_str(sheet.col(7)[i].value, workbook.datemode) for i in range(1, sheet.nrows)]
amount = [sheet.col(8)[i].value for i in range(1, sheet.nrows)]
data = pd.DataFrame()
data['cata_l1'] = pd.Series(cata_l1)
data['cata_l2'] = pd.Series(cata_l2)
data['date'] = pd.Series(date)
data['amount'] = pd.Series(amount)
data.sort_values(by='date', inplace=True)
car_cost = data[data['cata_l1'].__eq__('交通')
                & data['cata_l2'].__eq__(car_cost_cata[0])
                | data['cata_l2'].__eq__(car_cost_cata[1])
                | data['cata_l2'].__eq__(car_cost_cata[2])
                | data['cata_l2'].__eq__(car_cost_cata[4])
                | data['cata_l2'].__eq__(car_cost_cata[5])
                | data['cata_l2'].__eq__(car_cost_cata[6])
                | data['cata_l2'].__eq__(car_cost_cata[7])]
car_cost = car_cost.drop({'cata_l1', 'cata_l2'}, axis=1)
income_sheet = workbook.sheet_by_name('收入')
income_date = [xl_date_to_date_str(income_sheet.col(5)[i].value,
                                   workbook.datemode) for i in range(1, income_sheet.nrows)]
income_amount = [income_sheet.col(6)[i].value for i in range(1, income_sheet.nrows)]
income_data = pd.DataFrame()
income_data['date'] = income_date
income_data['amount'] = income_amount
balance = income_data
spent = data.drop({'cata_l1', 'cata_l2'}, axis=1)
spent['amount'] = spent['amount'].apply(lambda x: -x)
balance = balance.append(spent, ignore_index=True)
balance.sort_values('date', inplace=True)
#car_cost
baby_cost = data[data['cata_l1'].__eq__('育儿')
                 | data['cata_l2'].__eq__('婴儿用品')
                 | data['cata_l2'].__eq__('宝宝用品')
                 | data['cata_l2'].__eq__('婴幼儿用品')
                 | data['cata_l2'].__eq__('母婴用品')
                 | data['cata_l2'].__eq__('婴幼儿门诊')]
baby_cost = baby_cost.drop({'cata_l1', 'cata_l2'}, axis=1)
baby_cost_sum = baby_cost.groupby('date')['amount'].sum()
baby_cost_sum_df = pd.DataFrame(baby_cost_sum).reset_index()
car_cost_sum = car_cost.groupby('date')['amount'].sum()
car_cost_sum_df = pd.DataFrame(car_cost_sum).reset_index()
#car_cost_sum_df
append_to_csv(car_cost_sum_df, car_cost_file_name)
baby_cost_file_name
append_to_csv(baby_cost_sum_df, baby_cost_file_name)
bc = baby_cost_sum_df['amount']#.apply(lambda x: -x)
running_sum = get_running_sum(bc)

plt.plot(running_sum)
plt.show()
