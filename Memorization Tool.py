from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class MyClass(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    first_column = Column(String)
    second_column = Column(String)
    box = Column(Integer, default=1)

Base.metadata.create_all(engine)

def check_input_base(x):
    question_or_answer = input(x)
    while question_or_answer == "" or question_or_answer == " ":
        question_or_answer = input(x)
    return question_or_answer

def check_input_menu(x, y):
    user_choice = input(x)
    while user_choice not in y:
        print(user_choice, "is not an option")
        user_choice = input(x)
    return user_choice

def add_flashcard():
    while True:
        user_choice = check_input_menu("\n1. Add a new flashcard\n2. Exit\n", ["1", "2", "3"])
        if user_choice == "1":
            new_flashcard = MyClass(first_column=check_input_base("\nQuestion:\n"), second_column=check_input_base("Answer:\n"))
            session.add(new_flashcard)
            session.commit()
            continue
        elif user_choice == "2":
            break

def check_questions_base():
    if len(session.query(MyClass).all()) == 0:
        print("\nThere is no flashcard to practice!")
    else:
        for question, answer, box in session.query(MyClass.first_column, MyClass.second_column, MyClass.box).all():
            print("\nQuestion:", question)
            user_choice = check_input_menu('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n', ["y", "n", "u"])
            if user_choice == "y":
                print("\nAnswer:", answer)
                user_choice = check_input_menu('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n', ["y", "n"])
                if user_choice == "y" and box == 1:
                    session.query(MyClass).filter(MyClass.first_column == question).update({MyClass.box: 2})
                    session.commit
                elif user_choice == "y" and box == 2:
                    session.query(MyClass).filter(MyClass.first_column == question).update({MyClass.box: 3})
                    session.commit
                elif user_choice == "y" and box == 3:
                    session.query(MyClass).filter(MyClass.first_column == question).delete()
                    session.commit()
                elif user_choice == "n" and box > 1:
                     session.query(MyClass).filter(MyClass.first_column == question).update({MyClass.box: box - 1})
                     session.commit                                      
            elif user_choice == "u":
                user_choice = check_input_menu('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n', ["d", "e"])
                if user_choice == "d":
                    session.query(MyClass).filter(MyClass.first_column == question).delete()
                    session.commit()
                elif user_choice == "e":
                    print("\ncurrent question:", question)
                    fixed_question = input("please write a new question:\n")
                    session.query(MyClass).filter(MyClass.first_column == question).update({MyClass.first_column: fixed_question})
                    session.commit()
                    print("\ncurrent answer:", answer)
                    fixed_answer = input("please write a new answer:\n")
                    session.query(MyClass).filter(MyClass.first_column == fixed_question).update({MyClass.second_column: fixed_answer})
                    session.commit()

while True:
    user_choice = check_input_menu("\n1. Add flashcards\n2. Practice flashcards\n3. Exit\n", ["1", "2", "3"])
    if user_choice == "1":
        add_flashcard()
    elif user_choice == "2":
        check_questions_base()
    elif user_choice == "3":
        print("Bye!")
        break