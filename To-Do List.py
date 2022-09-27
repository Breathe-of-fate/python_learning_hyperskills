from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer
from datetime import datetime
from datetime import timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Table(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

while True:
    print("\n1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Missed tasks", "5) Add a task", "6) Delete a task", "0) Exit", sep="\n")
    user_choice = input()
    if user_choice == "1":
        for_today = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        if len(for_today) == 0:
            for_today = ["Nothing to do!"]
        print(f"\nToday {datetime.today().strftime('%d %b')}:", *for_today, "", sep="\n")

    elif user_choice == "2":
        for i in range(8):
            dd_mon = (datetime.today() + timedelta(days=i)).strftime('%A %d %b')
            tasks = session.query(Table).filter(Table.deadline == datetime.today().date() + timedelta(days=i)).all()
            if len(tasks) == 0:
                tasks = ["Nothing to do!"]
            print("", f"{dd_mon}:", *tasks, sep="\n")

    elif user_choice == "3":
        print("\nAll tasks:")
        for id, task, date in session.query(Table.id, Table.task, Table.deadline).order_by(Table.deadline, Table.task):
            print(f"{id}. {task}. {datetime.strftime(date, '%#d %b')}", sep="\n")

    elif user_choice == "4":
        print("\nMissed tasks:")
        missed = session.query(Table.id, Table.task, Table.deadline).order_by(Table.deadline, Table.task).filter(Table.deadline < datetime.today().date()).all()
        if len(missed) == 0:
            print("All tasks have been completed!")
        else:
            for id, task, date in missed:
                print(f"{id}. {task}. {datetime.strftime(date, '%#d %b')}", sep="\n")

    elif user_choice == "5":
        new_task = Table(task=input("\nEnter a task:\n"), deadline=datetime.strptime(input("\nEnter a deadline\n"), '%Y-%m-%d'))
        session.add(new_task)
        session.commit()
        print("The task has been added!")

    elif user_choice == "6":
        print("\nChoose the number of the task you want to delete:")
        for id, task, date in session.query(Table.id, Table.task, Table.deadline).order_by(Table.deadline, Table.task):
            print(f"{id}. {task}. {datetime.strftime(date, '%#d %b')}", sep="\n")
        session.query(Table).filter(Table.id == int(input())).delete()
        session.commit()
        print("The task has been deleted!")

    elif user_choice == "0":
        break