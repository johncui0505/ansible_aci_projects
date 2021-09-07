#!/usr/local/bin/python3
import json
import pandas as pd

class json2xlsx(object):

    def __init__(self):
        self.JSON_PATH = "./"
        self.XLSX_PATH = "./"
    
    def main(self):
        with open(self.JSON_PATH + "interface_status.json") as json_file:
            data = json.load(json_file)
        
        df = pd.DataFrame(data)
        df.to_excel(self.XLSX_PATH + "인터페이스_상태.xlsx")

if __name__ == "__main__":
    func = json2xlsx()
    func.main()
