import pandas as pd
import re
import csv
import sqlite3
import json
from lxml import etree

def create_xml(x):
    file_name = x.replace("[CHECKED]", "")
    open_db = sqlite3.connect(file_name + ".s3db")
    data_from_table = pd.read_sql("SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load FROM convoy WHERE score <= 3", open_db)
    if len(data_from_table.index) > 0:
        data_from_table.to_xml(path_or_buffer=file_name + ".xml", index=False, root_name="convoy", row_name="vehicle", xml_declaration=False)
    else:
        elem = etree.Element("convoy")
        empty_xml = etree.tostring(elem, method="html", encoding="unicode")
        with open(file_name + ".xml", "w") as f:
                f.write(empty_xml)
    open_db.close()
    print(f"{len(data_from_table)} {'vehicles were' if len(data_from_table) > 1 or len(data_from_table) == 0 else 'vehicle was'} saved into {file_name}.xml")

def create_json(x):
    file_name = x.replace("[CHECKED]", "")
    open_db = sqlite3.connect(file_name + ".s3db")
    modify_db = open_db.cursor()
    records = modify_db.execute("SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load FROM convoy WHERE score > 3").fetchall()
    headers = [i[1] for i in modify_db.execute("pragma table_info(convoy)").fetchall()]
    to_write = {'convoy':[dict(zip(headers, i)) for i in records]}
    with open(file_name + ".json", "w") as final_file:
        json.dump(to_write, final_file)
    open_db.close()
    print(f"{len(records)} {'vehicles were' if len(records) > 1 or len(records) == 0 else 'vehicle was'} saved into {file_name}.json")

def create_db(x):
    file_name = x.replace("[CHECKED]", "")
    open_db = sqlite3.connect(file_name + ".s3db")
    modify_db = open_db.cursor()
    modify_db.execute(f"""CREATE TABLE IF NOT EXISTS convoy (vehicle_id INTEGER PRIMARY KEY,
                                                             engine_capacity INTEGER NOT NULL,
                                                             fuel_consumption INTEGER NOT NULL,
                                                             maximum_load INTEGER NOT NULL);""")
    entries = [tuple(i.replace("\n", "").split(",")) for i in open(x + ".csv")]
    modify_db.executemany(f"INSERT INTO convoy VALUES (?, ?, ?, ?)", entries)
    open_db.commit()
    print(f"{len(entries)} {'records were' if len(entries) > 1 else 'record was'} inserted into {file_name}.s3db")
    data_from_table = pd.read_sql("SELECT * FROM convoy", open_db)
    data_from_table["burned"] = 450 * (data_from_table["fuel_consumption"] / 100)
    data_from_table["stops"] = (data_from_table["burned"] / data_from_table["engine_capacity"])
    data_from_table["score_burned"] = data_from_table["burned"].apply(lambda x: 2 if x <= 230 else 1)
    data_from_table["score_stops"] = data_from_table["stops"].apply(lambda x: 0 if x >= 2 else 1 if x >=1 else 2)
    data_from_table["score_load"] = data_from_table["maximum_load"].apply(lambda x: 2 if x >= 20 else 0)
    data_from_table["score"] = data_from_table["score_burned"] + data_from_table["score_stops"] + data_from_table["score_load"]
    data_from_table.drop(columns=["burned", "stops", "score_burned", "score_stops", "score_load"], inplace=True)
    modify_db.execute("ALTER TABLE convoy ADD score;")
    open_db.commit()
    data_from_table.to_sql("convoy", open_db, schema="dbo", if_exists='replace', index=None, dtype={'vehicle_id': 'INTEGER PRIMARY KEY', 
                                                                                                    'engine_capacity': 'INTEGER NOT NULL', 
                                                                                                    'fuel_consumption': 'INTEGER NOT NULL', 
                                                                                                    'maximum_load': 'INTEGER NOT NULL',
                                                                                                    'score': 'INTEGER NOT NULL'})
    open_db.close()

def fix_csv(x):
    to_search = '[a-zA-Z_ .]'
    list_to_operate = [line.replace("\n", "").split(",") for line in open(x + ".csv")][1:]
    to_count = [True if re.search(to_search, ii) else False for i in list_to_operate for ii in i].count(True)
    to_read = [re.sub(to_search, "", line.replace("\n", "")).split(",") for line in open(x + ".csv")][1:]
    if "[CHECKED]" in x:
        to_write = csv.writer(open(x + ".csv", "w"), delimiter=",", lineterminator='\n')
        file_name = x
    else:
        to_write = csv.writer(open(x + "[CHECKED].csv", "w"), delimiter=",", lineterminator='\n')
        file_name = x + "[CHECKED]"
    to_write.writerows(to_read)
    if to_count != 0:
        print(f"{to_count} {'cells were' if to_count > 1 else 'cell was'} corrected in {file_name}.csv")

def from_xlsx(x):
    new_table = pd.read_excel(x, sheet_name='Vehicles', dtype=str)
    s1, s2 = new_table.shape
    new_table.to_csv(x.split(".")[0] +'.csv', index=None)
    print(f"{s1} {'lines were' if s1 > 1 else 'line was'} imported to {x.split('.')[0]}.csv")

file_name = input("Input file name\n")
formats = file_name.split(".")
if "xlsx" in formats[1]:
    from_xlsx(file_name)
    fix_csv(formats[0])
    create_db(formats[0] + "[CHECKED]")
    create_json(formats[0] + "[CHECKED]")
    create_xml(formats[0] + "[CHECKED]")
elif "csv" in formats[1] and "[CHECKED]" not in formats[0]:
    fix_csv(formats[0])
    create_db(formats[0] + "[CHECKED]")
    create_json(formats[0] + "[CHECKED]")
    create_xml(formats[0] + "[CHECKED]")
elif "csv" in formats[1] and "[CHECKED]" in formats[0]:
    fix_csv(formats[0])
    create_db(formats[0])
    create_json(formats[0])
    create_xml(formats[0])
elif "s3db" in formats[1]:
    create_json(formats[0])
    create_xml(formats[0])