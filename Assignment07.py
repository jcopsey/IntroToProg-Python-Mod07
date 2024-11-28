# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   jcopsey,11/27/2024,Built upon existing script
# ------------------------------------------------------------------------------------------ #
import json
from typing import TextIO

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.2

class Person:
    """
    A class for person data.

    Properties:
        first_name (str): Person's first name.
        last_name (str): Person's last name.

    ChangeLog:
    jcopsey,11/27/2024,class created
    """

# Student first and last name constructors
    def __init__(
            self,
            first_name: str ='',
            last_name: str =''
    ):  # parameters default to empty
        self.first_name = first_name  # Used for validation
        self.last_name = last_name  # Used for validation

    # Getter and setter properties
    @property
    def first_name(self):
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "": # validates input
            self.__first_name = value
        else:
            raise ValueError("A first name cannot include numbers and cannot be empty.")

    # Getter and Setter Properties for last name are created below
    @property
    def last_name(self):
        return self.__student_last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":
            self.__student_last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    # Returns first and last name comma in a comma separated string
    def __str__(self):
        return f"{self.first_name},{self.last_name}"

# Student class, inherits person class

class Student(Person):
    """
    A class for student data.

    Properties:
        course_name (str): The name of the course the student is registered in.

    ChangeLog:
    jcopsey,11/23/2024,class created
    """

    # Course name constructor
    @property
    def course_name(self):
        return self.__course_name

    def __init__(
            self,
            first_name: str = '',
            last_name: str = '',
            course_name: str = ''
    ):
        super().__init__(
            first_name=first_name,
            last_name=last_name
        )
        self.course_name = course_name

    # Getter and setter
    @property
    def course_name(self):
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value

    # Method to extract the comma separate data is presented below, it overrides the __str__() method
    def __str__(self):
        return (f'{self.first_name},'
                f'{self.last_name},'
                f'{self.course_name}')

# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of dictionary rows

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        jcopsey,11/23/2024,edited function to use new student class

        :param file_name: string data with name of file to read from
        :param student_data: list of dictionary rows to be filled with file data

        :return: list
        """

        try:
            file: TextIO = open(file_name, 'r')
            list_of_dictionary_data = json.load(file)
            for student in list_of_dictionary_data:
                student_object: Student = Student(
                    first_name=student['FirstName'],
                    last_name=student['LastName'],
                    course_name=student['CourseName']
                )
                student_data.append(student_object)
            file.close()
        except FileNotFoundError as e:  # Handles error in case there is no initial file
            file = open(FILE_NAME, "w")
            file.close()
            IO.output_error_messages(f"{FILE_NAME} was not found.", e)
            IO.output_error_messages(f"Creating {FILE_NAME}\n")
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if file.closed is False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of dictionary rows

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        jcopsey,11/27/2024,edited function to use new student class

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
        """

        try:
            list_of_dictionary_data: list = []
            file: TextIO = open(file_name, 'w')
            for student in student_data:
                student_dictionary: dict = {
                    "FirstName": student.first_name,
                    "LastName": student.last_name,
                    "CourseName": student.course_name
                }
                list_of_dictionary_data.append(student_dictionary)
            json.dump(list_of_dictionary_data, file)
            file.close()
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message,error=e)
        finally:
            if file.closed is not False:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the a custom error messages to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function


        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        jcopsey,11/27/2024,edited function to use new student class

        :param student_data: list of dictionary rows to be displayed

        :return: None
        """

        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} '
                  f'{student.last_name} is enrolled '
                  f'in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        jcopsey,11/27/2024,edited function to use new student class

        :param student_data: list of dictionary rows to be filled with input data

        :return: list
        """

        try:
            student = Student()
            student.first_name = input("Enter Student's First Name: ")
            student.last_name = input("Enter Student's Last Name: ")
            student.course_name = input("Enter Course Name: ")
            student_data.append(student)
            print(f"\nYou have registered "
                  f"{student.first_name} "
                  f"{student.last_name} for "
                  f"{student.course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was not the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data

# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
