import pandas as pd
from numpy import int64, float64


class DF:

    def __init__(self):
        self.path = input("Path: ")
        try:
            self.__file = pd.ExcelFile(self.path)
        except FileNotFoundError:
            print(f"There is no excel file at ({self.path})")
            exit(1) 
        self.bonus = 0

    def blanks(self, param):
        return param in ["-", "--", "--//--", None]

    def check_total(self, tot, res, lic, partn, i, name, j):
        types = (int64, float64, int,  float,)
        lst = []
        for lit in [tot, res, lic]:
            if type(lit) in types:
                lst.append(float(lit))
            elif type(lit) not in types:
                lit = 0
                lst.append(lit)
        if lst[0] == lst[1] + lst[2]:
            if i == 0:
                return lst[0]
            elif i > 0 and self.blanks(partn):
                return lst[1]
            else:
                return 0
        else:
            raise ValueError(f"Sum of values in sheet {name} does not match Total in line {j+2}")
    
    def coef(self, page_num):
        return [.2, .05, .05, .05, .05, .05, .03, .03, .03, .02, .02, .02][page_num]
    


def main():
    df = DF()
    for i in range(min(len(df._DF__file.sheet_names), 12)):
        name = df._DF__file.sheet_names[i]
        sheet = df._DF__file.parse(name)
        for j in range(sheet.shape[0]):
                df.bonus += df.check_total(sheet.iloc[j][1], sheet.iloc[j][2], sheet.iloc[j][3], sheet.iloc[j][7], i, name, j) * df.coef(i)

    df._DF__file.close()

    print("%.2f" % df.bonus)


if __name__ == "__main__":
    main()