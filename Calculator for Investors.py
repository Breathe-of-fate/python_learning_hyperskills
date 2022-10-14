import csv
from sqlalchemy import create_engine, String, Column, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

engine = create_engine('sqlite:///investor.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Companies(Base):
    __tablename__ = 'companies'

    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)

class Financial(Base):
    __tablename__ = 'financial'
    
    ticker = Column(String, primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)

Base.metadata.create_all(engine)

def file_to_db(table_class, data) -> None:
    for dic in data:
        for column_name, row_value in dic.items():
            if row_value == '':
                dic[column_name] = None
        session.add(table_class(**dic))
    session.commit()

def open_n_read(x):
    with open(x) as file:
        return list(csv.DictReader(file))

file_to_db(Companies, open_n_read('companies.csv'))
file_to_db(Financial, open_n_read('financial.csv'))

def input_to_db(a, b):
    table = a.__table__.columns.keys()
    db = [{}]
    for i in range(len(table)):
        db[0][table[i]] = b[i]
    for dic in db:
        session.add(a(**dic))
    session.commit()

def search_data(a):
    names = [ii for i in session.query(Companies.name) for ii in i if a.lower() in ii.lower()]
    if len(names) > 0:
        [print(*i) for i in enumerate(names)]
        tickers = [i[0] for i in session.query(Companies.ticker, Companies.name).filter(Companies.name == names[int(input("Enter company number:\n"))])]
        session.close()
        return "".join(tickers)
    else:
        print("Company not found!")

def isnone(a, b):
    if a is None or b is None:
        return None
    return round(a / b, 2)

def show_top_10(a, b, c):
    print(c)
    for i, ii, iii in session.query(Financial.ticker, a, b).filter(a != None, b != None).order_by(-func.round(a / b, 2)).limit(10).all():
        print(i, round(ii / iii, 2))
    
def main_menu():
    user_choice = input("\nMAIN MENU\n0 Exit\n1 CRUD operations\n2 Show top ten companies by criteria\n\nEnter an option:\n")
    if user_choice not in "012":
        print("Invalid option!")
    return user_choice

def crud_menu():
    user_choice = input("\nCRUD MENU\n0 Back\n1 Create a company\n2 Read a company\n3 Update a company\n4 Delete a company\n5 List all companies\n\nEnter an option:\n")
    if user_choice not in "012345":
        print("Invalid option!")
    elif user_choice == "0":
        return False
    elif user_choice == "1":
        inputs = [input("Enter ticker (in the format 'MOON'):\n"), 
                  input("Enter company (in the format 'Moon Corp'):\n"), 
                  input("Enter industries (in the format 'Technology'):\n"),
                  input("Enter ebitda (in the format '987654321'):\n"), 
                  input("Enter sales (in the format '987654321'):\n"), 
                  input("Enter net profit (in the format '987654321'):\n"),
                  input("Enter market price (in the format '987654321'):\n"),
                  input("Enter net dept (in the format '987654321'):\n"),
                  input("Enter assets (in the format '987654321'):\n"),
                  input("Enter equity (in the format '987654321'):\n"),
                  input("Enter cash equivalents (in the format '987654321'):\n"),
                  input("Enter liabilities (in the format '987654321'):\n")]
        to_companies = inputs[:3]
        to_financial = [inputs[0], *[i for i in inputs[3:]]]
        input_to_db(Companies, to_companies)
        input_to_db(Financial, to_financial)
        print("Company created successfully!")
    elif user_choice == "2":
        founded = search_data(input("Enter company name:\n"))
        if founded is not None:
            for i, ii, iii in session.query(Companies.ticker, Companies.name, Companies.sector).filter(Companies.ticker == founded).all():
                print(i, ii)
                for n1, n2, n3, n4, n5, n6, n7, n8, n9, n10 in \
                    session.query(Financial.ticker, Financial.ebitda, Financial.sales, 
                                  Financial.net_profit, Financial.market_price, Financial.net_debt,
                                  Financial.assets, Financial.equity, Financial.cash_equivalents, Financial.liabilities).filter(Financial.ticker == founded).all():
                    print(f"P/E = {isnone(n5, n4)}", f"P/S = {isnone(n5, n3)}", f"P/B = {isnone(n5, n7)}", f"ND/EBITDA = {isnone(n6, n2)}", f"ROE = {isnone(n4, n8)}", f"ROA = {isnone(n4, n7)}", f"L/A = {isnone(n10, n7)}", sep="\n")
    elif user_choice == "3":
        founded = search_data(input("Enter company name:\n"))
        if founded is not None:
            session.query(Financial).filter(Financial.ticker == founded).update({Financial.ebitda: input("Enter ebitda (in the format '987654321'):\n")}) 
            session.query(Financial).filter(Financial.ticker == founded).update({Financial.sales: input("Enter sales (in the format '987654321'):\n")})
            session.query(Financial).filter(Financial.ticker == founded).update({Financial.net_profit: input("Enter net profit (in the format '987654321'):\n")})
            session.query(Financial).filter(Financial.ticker == founded).update({Financial.market_price: input("Enter market price (in the format '987654321'):\n")})
            session.query(Financial).filter(Financial.ticker == founded).update({Financial.net_debt: input("Enter net dept (in the format '987654321'):\n")})
            session.query(Financial).filter(Financial.ticker == founded).update({Financial.assets: input("Enter assets (in the format '987654321'):\n")})
            session.query(Financial).filter(Financial.ticker == founded).update({Financial.equity: input("Enter equity (in the format '987654321'):\n")})
            session.query(Financial).filter(Financial.ticker == founded).update({Financial.cash_equivalents: input("Enter cash equivalents (in the format '987654321'):\n")})
            session.query(Financial).filter(Financial.ticker == founded).update({Financial.liabilities: input("Enter liabilities (in the format '987654321'):\n")})
            session.commit()
            print("Company updated successfully!")
    elif user_choice == "4":
        founded = search_data(input("Enter company name:\n"))
        if founded is not None:
            session.query(Companies).filter(Companies.ticker == founded).delete()
            session.query(Financial).filter(Financial.ticker == founded).delete()
            session.commit()
            print("Company deleted successfully!")
    elif user_choice == "5":
        print("COMPANY LIST")
        for i, ii, iii in session.query(Companies.ticker, Companies.name, Companies.sector).order_by(Companies.ticker):
            print(i, ii, iii)

def top_ten_menu():
    user_choice = input("\nTOP TEN MENU\n0 Back\n1 List by ND/EBITDA\n2 List by ROE\n3 List by ROA\n\nEnter an option:\n")
    if user_choice not in "0123":
        print("Invalid option!")
    elif user_choice == "0":
        return False
    elif user_choice == "1":
        show_top_10(Financial.net_debt, Financial.ebitda, "TICKER ND/EBITDA")
    elif user_choice == "2":
        show_top_10(Financial.net_profit, Financial.equity, "TICKER ROE")
    elif user_choice == "3":
        show_top_10(Financial.net_profit, Financial.assets, "TICKER ROA")
  
print("Welcome to the Investor Program!")
while True:
    user_choice = main_menu()
    if user_choice == "0":
        print("Have a nice day!")
        break
    elif user_choice == "1":
        if crud_menu():
            break
    elif user_choice == "2":
        if top_ten_menu():
            break