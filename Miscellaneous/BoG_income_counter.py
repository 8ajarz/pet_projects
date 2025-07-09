import re
import pandas as pd
#Check for possible issues with uncorrect filename OR uninstalled openxyl lib *(to use the path)
try:
    path = input("Напиши путь и название файла в формате типа /С/user/Desktop/Файл, где надо узнать доход за день.xlsx.\n")
    end_path = input("Напиши путь и название файла, куда вывести результаты, в формате типа /С/user/Desktop/Файл\n")
    df = pd.read_excel(path)
except:
  print("Что-то пошло не так. Попробуй еще раз. Путь к файлу можна найти так: правый клик - свойства")
  exit(1)

d = dict()
previous_day = 0
#first 12 rows - are just for BoG logo
for i in range(12, len(df)):
    a = df.loc[i][5]
    date = re.findall("-\d\d-\d\d", str(df.loc[i][0]))
    if len(date) < 1:
        continue
    day = float(f"{date[0][-2]}{date[0][-1]}.{date[0][1:3]}")
    #Payment date - is the unique mark from the BoG`s report, that this is an income
    if re.findall("^Payment - Date:", a):
        income = re.findall("\w*:\sGEL\s(\d*.\d*);", a)
        income = float(income[0])
        time = re.findall("\d\d:\d\d", a)
        time = int(time[0][0:2])
        # if time of the income is before 1 AM - it means, that guests made an order before midnight,
        # wich means, that this income belongs to previous day
        if time <= 1:
            previous_day = day - 1
            d[previous_day] = d.get(previous_day, 0) + income
        else:
            d[day] = d.get(day, 0) + income
    #5th column (df.loc[i][4]) - to distinguish income exactly because transfers could be income and expenses.
    if re.findall("National currency transfer:", a) and df.loc[i][4] > 0:
        income = float(df.loc[i][4])
        d[day] = d.get(day, 0) + income

#extract day and income per day and prepare them to be inserted in the new excel file (requires lists)
days = []
inc = []

for key in d.items():
    days.append(key[0])
    inc.append(round(key[1], 2))

data = {"Дата": days,
        "Доход в GEL": inc
        }

d_frame = pd.DataFrame(data, columns=["Дата", "Доход в GEL"])
d_frame.to_excel(f'{end_path}.xlsx', index=False, header=True)

print("Готово!")
