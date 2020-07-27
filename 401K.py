"""
401K

Created by Jas Lau on 7/25/19.
Copyright © 2019 Jas Lau. All rights reserved.
"""

from enum import Enum
import numpy
import random
import string


class Error(Exception):
    """Base class for other exceptions"""
    pass

class EmpNumError(Error):
    """Raised when the employee number is invalid"""
    pass

class IsFull(Error):
    """Raised when the supervisor array is full"""
    pass


# ====================== Base Class: Employee Class ======================
class Employee:
    # static member
    DEFAULT_NAME = "unidentified"
    DEFAULT_NUM = 999
    BENEFIT_ID = 500
    MIN_EMPLY_NUM = 100
    MAX_EMPLY_NUM = 999

    # constructor
    def __init__(self, name=DEFAULT_NAME, number=DEFAULT_NUM):
        self.employee_name = name
        self.employee_num = number

    # accessors
    @property
    def employee_name(self):
        return self.__name

    @property
    def employee_num(self):
        return self.__number

    def get_determine_benefits(self):
        return self.__benefits

    # mutators
    @employee_name.setter
    def employee_name(self, name):
        """Set the employee name.

        Args:
            name (str): Employee name
        """
        if self.validate_name(name):
            self.__name = name
        else:
            self.__name = self.DEFAULT_NAME   

    @employee_num.setter
    def employee_num(self, number):
        """Set employee's number. This method will call determine_benefits().
           - benefits (bool): Hold the boolean value of the employee benefits.

        Args:
            number (int): Employee id 
        
        Returns:
            self.number = self.DEFAULT_NUM
        """        
        if self.validate_id(number):
            self.__number = number
        else:
            self.__number = self.DEFAULT_NUM
        
        if self.determine_benefits(number):
            self.__benefits = True
        else:
            self.__benefits = False

    # helper function
    def __str__(self):
        """Print employees' information in format: 
           'Name #id (Benefits) Shift: DAY.'

        Returns:
            str: Return a string. 
        """
        if self.get_determine_benefits():
            ret_str_bnft = "Benefits"
        else:
            ret_str_bnft = "No Benefits"

        ret_str = '\n\n{} # {} ({})'.format(self.employee_name,
                                        str(self.employee_num), ret_str_bnft)
        return ret_str

    def determine_benefits(self, number):
        """Determine if an employee can get benefits.

        Args:
            number (int): Employee id

        Returns:
            bool: True for eligible. False otherwise.
        """        
        return number < Employee.BENEFIT_ID
            

    @classmethod
    def validate_name(cls, the_name):
        """Check if the input employee name is valid.

        Args:
            the_name (str): Employee name

        Returns:
            bool: True for valid. False otherwise.
        """        
        return (type(the_name) is str and the_name.isnumeric() is False)

    @classmethod
    def validate_id(cls, employee_id):
        """Check if the input employee id is valid and if it is in range.

        Args:
            employee_id (int): Employee id

        Returns:
            bool: True for valid. False otherwise.
        """        
        return (type(employee_id) is int and
                Employee.MIN_EMPLY_NUM <= employee_id <= Employee.MAX_EMPLY_NUM)
            


# ====================== End of Base Class: Employee Class ======================


# ================= Derived Class: Production Worker Class =================
# inherit from Enum
class Shift(Enum):
    DAY = 1
    SWING = 2
    NIGHT = 3

    def __str__(self):
        ret_str = self.__str__()
        return ret_str


class ProductionWorker(Employee):
    # class constant
    DEFAULT_SHIFT = Shift.DAY
    DEFAULT_HOURLY_RAY_RATE = 1
    DEFAULT_HOURS_WORKED = 0
    MIN_HOURLY_PAY_RATE = 0
    MAX_HOURLY_PAY_RATE = 20
    MIN_HOURS_WORKED = 0
    MAX_HOURS_WORKED = 40

    # constructor
    def __init__(self, *args, shift=DEFAULT_SHIFT, rate=DEFAULT_HOURLY_RAY_RATE,
                 hour=DEFAULT_HOURS_WORKED, **kwargs):
        """
        Instance variable:
        employee_shift: Hold the employee shift (Day, Swing, Night)
        rate: Hold the hourly pay rate of production workers
        hour: Hold the hours worked by production workers
        """
        # Call Base Class
        super().__init__(*args, **kwargs)

        # Derived Class attributes
        self.employee_shift = shift
        self.hourly_pay_rate = rate
        self.hours_worked = hour

    # accessors
    @property
    def employee_shift(self):
        return self.__shift

    @property
    def hourly_pay_rate(self):
        return self.__rate

    @property
    def hours_worked(self):
        return self.__hour

    # mutators
    @employee_shift.setter
    def employee_shift(self, shift):
        """ Set employee shift.

        Args:
            shift (Shift): Employee shift.

        Returns:
            Shift: Set instance variable shift to input shift if valid. Set to default shift otherwise.
        """
        if type(shift) is Shift:
            self.__shift = shift
        elif type(shift) is int and (1 <= shift <= 3):
            self.__shift = Shift(shift)
        else:
            self.__shift = self.DEFAULT_SHIFT

    @hourly_pay_rate.setter
    def hourly_pay_rate(self, rate):
        """Set the hourly pay rate.

        Args:
            rate (int): Hourly pay rate
        """        
        if self.validate_rate(rate):
            self.__rate = rate
        else:
            self.__rate = self.DEFAULT_HOURLY_RAY_RATE

    @hours_worked.setter
    def hours_worked(self, hour):
        """Set the hour worked.
        
        Args:
            hour (int): Hour worked
        """
        if self.validate_hour(hour):
            self.__hour = hour
        else:
            self.__hour = self.DEFAULT_HOURS_WORKED
        

    def gross_pay(self, rate, hour):
        """ Calculate the gross pay for production workers.
        
        Args:
            rate (int): Hourly pay rate
            hour (int): Hour worked

        Returns:
            int: Return rate * hour for valid input. Zero otherwise.
        """
        if self.validate_rate(rate) and self.validate_hour(hour):
            return rate * hour
        else:
            return 0

    # stringizer and console output
    def __str__(self):
        """ Call Base Class to_string to display name and id. Concatenate
        Production Workers' shift, hourly rate, hours worked and gross pay. 
        
        Returns:
            str: Return a string.
        """
        me = super().__thisclass__
        mro = super().__self_class__.__mro__
        if len(mro) - mro.index(me) > 2:
            ret_str = super().__str__()
        ret_str += "\nShift: {} \n${} per hour \n{} hours this week \n${} " \
                   "gross pay\n" \
                   "".format(str(self.employee_shift.name),
                             str(self.hourly_pay_rate), str(self.hours_worked),
                             str(self.gross_pay(self.hourly_pay_rate,
                                                self.hours_worked)))
        return ret_str

    # helper functions
    @classmethod
    def validate_rate(cls, rate):
        """Check if the hourly pay rate valid.

        Args:
            rate (int): hourly pay rate

        Returns:
            bool: True for valid. False otherwise.
        """        
        return (type(rate) is int and
                cls.MIN_HOURLY_PAY_RATE <= rate <= cls.MAX_HOURLY_PAY_RATE)

    @classmethod
    def validate_hour(cls, hour):
        """Check if the hours worked valid.

        Args:
            rate (int): hour worked

        Returns:
            bool: True for valid. False otherwise.
        """
        return (type(hour) is int and
                cls.MIN_HOURS_WORKED <= hour <= cls.MAX_HOURS_WORKED)


# ================= Derived Class: Shift Supervisor Class =================


class ShiftSupervisor(Employee):
    DEFAULT_SALARY = 50000
    MIN_SALARY = 50000
    MAX_SALARY = 200000
    DEFAULT_SHIFT = Shift.DAY
    DEFAULT_CAPACITY = 10
    DEFAULT_NUM_OF_WORKERS = 0
    BONUS_ADD_TO_SALARY = 10000
    WORKERS_REQUIRED = 5

    # constructor
    def __init__(self, *args, salary=DEFAULT_SALARY, shift=DEFAULT_SHIFT,
                 emp_array=DEFAULT_CAPACITY, num_worker=DEFAULT_NUM_OF_WORKERS,
                 **kwargs):
        """
        Instance variable:
        salary: Hold the annual salary of supervisor
        shift: Hold the shift of supervisor
        emp_array: The array of employees
        num_workers: Hold the number of workers under the supervisor
        """
        super().__init__(*args, **kwargs)
        self.annual_salary = salary
        self.supervisor_shift = shift
        self.emp_array = numpy.empty(
            shape=(1, self.valid_arr_capacity(emp_array)),
            dtype=ProductionWorker)
        self.num_worker = num_worker

    # accessors
    @property
    def annual_salary(self):
        return self.__salary

    @property
    def supervisor_shift(self):
        return self.__shift

    @property
    def add_to_array(self):
        return self.__emp_array

    @property
    def number_of_workers(self):
        return self.__num_worker

    # mutators
    @annual_salary.setter
    def annual_salary(self, salary):
        """Set the annual salary.

        Args:
            salary (int): Annual salary of supervisor
        """        
        if self.valid_salary(salary):
            self.__salary = salary
        else:
            self.__salary = self.DEFAULT_SALARY

    @supervisor_shift.setter
    def supervisor_shift(self, shift):
        """Set the shift of supervisor.

        Args:
            shift (Shift): Shift of supervisor
        """        
        if type(shift) is Shift:
            self.__shift = shift
        elif type(shift) is int and (1 <= shift <= 3):
            self.__shift = Shift(shift)
        else:
            self.__shift = self.DEFAULT_SHIFT

    @add_to_array.setter
    def add_to_array(self, production_worker):
        """ Determine if the production worker should be added to the
        supervisor array. Raise error if the array is full. If it is not full
        and is in shift, append to the supervisor array and then delete the
        extra length of 1. Increment self.num_worker by 1."""
        if not self.shift_valid(production_worker):
            return
        try:
            if self.emp_array.size <= self.num_worker:
                raise IsFull
        except ValueError:
            return

        # Append production worker to the array
        self.emp_array = numpy.append(self.emp_array, production_worker)

        # Remove extra space = 1, because using append method will increase
        # size by 1
        self.emp_array = numpy.delete(self.emp_array, 0)
        # update worker's number
        self.num_worker += 1

    # helper functions
    @classmethod
    def valid_salary(cls, salary):
        """Check if the salary input valid.

        Args:
            salary (int): Annul salary

        Returns:
            bool: True for valid. False otherwise.
        """        """ """
        return (type(salary) is int and cls.MIN_SALARY <= salary <= cls.MAX_SALARY)

    @classmethod
    def valid_arr_capacity(cls, emp_array):
        """Check if the array capacity of employee array valid.

        Args:
            emp_array (ProductionWorker): Employee array

        Returns:
            ProductionWorker: Array
        """        
        if type(emp_array) is int and emp_array > 0:
            return emp_array
        # else
        return ShiftSupervisor.DEFAULT_CAPACITY

    def shift_valid(self, worker_obj):
        """ Check if the worker is in the same shift as supervisor."""
        return worker_obj.shift is self.supervisor_shift()

    def bonus(self):
        """Check if the supervisor get bonus or not."""
        if self.num_worker > self.WORKERS_REQUIRED:
            self.salary = self.salary + self.BONUS_ADD_TO_SALARY
            return True
        else:
            return False

    def __str__(self):
        """Call Base Class to_string to display employee's name, employee's
        id and benefits status. """
        me = super().__thisclass__
        mro = super().__self_class__.__mro__
        if len(mro) - mro.index(me) > 2:
            ret_str = super().__str__()
        ret_str += "\nSalary ${} \nShift: {} \n{} workers in their " \
                   "shift\n".format(self.get_annual_salary(),
                                    self.get_supervisor_shift().name,
                                    self.get_number_of_workers())

        # Check if there's any worker under a supervisor
        # List Comprehension to obtain only Non-None type element
        the_array = numpy.array([i for i in self.emp_array if i is not None])
        if self.get_number_of_workers() > 0:
            for i in the_array:
                ret_str += "\nWorkers: \n{}".format(i.to_string())

        return ret_str


# ====================== END OF SHIFT SUPERVISOR CLASS ======================

# ====================== START OF 401K CLASS ======================
class Member401k(ShiftSupervisor, ProductionWorker):
    # constant
    DEFAULT_401K_ACCT_NUM = '123-4567890'
    DEFAULT_MIN_AMOUNT = 0
    DEFAULT_MAX_AMOUNT = 5000
    LEN_LETTERS = 3
    DEFAULT_MATCH = 0.05

    # constructor
    def __init__(self, *args, account_num=DEFAULT_401K_ACCT_NUM,
                 amount=DEFAULT_MIN_AMOUNT, **kwargs):
        super().__init__(*args, **kwargs)
        # 401k class attributes
        self.is_supervisor = False
        self.account_number = account_num
        self.max_value = self.max_match(**kwargs)
        self.contributed_amount = amount
        self.actual_value = self.actual_max(amount)

    # accessors
    @property
    def get_max_match(self):
        return self.max_value

    @property
    def get_actual_value(self):
        return self.actual_value

    @property
    def account_number(self):
        return self.account_num

    @property
    def contributed_amount(self):
        return self.amount

    # mutators
    @account_number.setter
    def account_number(self, account_num):
        """ Create a string combined with 3 random letters and employee's id

        Args:
            account_num (str): employee account number
        """        
        if type(account_num) is str and len(account_num) is 10:
            self.account_num = '{}-{}'.format(account_num[0:3], account_num[3:])
        else:
            self.account_num = self.DEFAULT_401K_ACCT_NUM
            

    @contributed_amount.setter
    def contributed_amount(self, amount):
        """Calculate the actual value.

        Args:
            amount (int): Amount contributed
        """        
        if self.validate_contribute_amount(amount):
            self.amount = amount
            self.actual_max(self.amount)
        else:
            self.amount = self.DEFAULT_MIN_AMOUNT
        

    @classmethod
    def validate_contribute_amount(cls, amount):
        """Check if the contributed amount input valid.

        Args:
            amount (int): Amount contributed

        Returns:
            bool: True for valid. False otherwise.
        """        
        return (type(amount) is int and
                cls.DEFAULT_MIN_AMOUNT <= amount <= cls.DEFAULT_MAX_AMOUNT)


    def max_match(self, **kwargs):
        """Calculate the max value.
            Supervisor's monthly pay = salary / 12
            Worker's monthly pay = gross pay * 4

        Returns:
            int: Max value = monthly pay * default match
        """        
        # local variable
        monthly_pay = 0
        # check if the instantiated object is a worker or supervisor
        # check if 'salary' in dictionary
        if 'salary' in kwargs:
            monthly_pay = self.annual_salary // 12
            # mark this object as a supervisor
            self.is_supervisor = True
        # check if 'rate' in dictionary
        if 'rate' in kwargs:
            rt = kwargs.get('rate')
            hr = kwargs.get('hour')
            monthly_pay = self.gross_pay(rt, hr) * 4
            # mark this object as a worker
            self.is_supervisor = False
        self.max_value = int(monthly_pay * self.DEFAULT_MATCH)
        return self.max_value

    def actual_max(self, amount):
        """Set the actual value.

        Args:
            amount (int): Amount contributed

        Returns:
            int: Actual value.
        """        
        self.actual_value = amount
        # check if the contributed amount larger than max_match value
        if self.actual_value > self.max_value:
            # if true, match the amount to max match
            self.actual_value = self.max_value
        else:
            # set the actual value to the input amount
            self.actual_value = self.actual_value
        return int(self.actual_value)

    def __str__(self):
        me = super().__thisclass__
        mro = super().__self_class__.__mro__
        mro1 = mro[3]

        # create an Employee's __str__
        ret_str = mro1.__str__(self)
        # check if the object is supervisor or worker
        if self.is_supervisor is True:
            emp_salary = self.annual_salary / 12
        else:
            emp_salary = self.gross_pay(self.hourly_pay_rate, self.hours_worked) * 4

        ret_str += "\nAccount #{} \nMonthly Pay ${} \nAmount contributed: " \
                   "${} \nMax match: ${} \nActual Match: ${}\n".format(
                       self.account_number, int(
                           emp_salary), self.contributed_amount,
                       self.get_max_match, self.get_actual_value)
        return ret_str


# ====================== END OF 401K CLASS ======================


# ====================== Client (As a Function) ======================


def main():
    answer1 = str(input('\n\nEmployee name (Use empty value to skip): '))
    answer2 = int(input('Employee number (Use empty value to skip): '))
    answer3 = int(input('Shift (DAY = 1, SWING = 2, NIGHT = 3): '))
    position = str(input('Worker or Supervisor? (w for worker, s for supervisor): '))
    
    if position == 'w':
        answer5 = int(input('Rate per hour: '))
        answer6 = int(input('Hour per week: '))
        answer7 = str(input('Account number (Use empty value to skip): '))
        answer8 = int(input('Amount contributed: '))

        employee = Member401k(name=answer1, number=answer2, shift=answer3, rate=answer5, hour=answer6, account_num=answer7, amount=answer8)
    elif position == 's':
        answer9 = int(input('Annual Salary: '))
        answer10 = int(input('Number of worker(s): '))
        answer11 = str(input('401K account number (10-digit): '))
        answer12 = int(input('Amount contributed: '))
        employee = Member401k(name=answer1, number=answer2, salary=answer9, shift=answer3, num_worker=answer10, account_num=answer11, amount=answer12)
    
    print(employee)

"""
    # Instantiate Workers object
    worker1 = Member401k(name='Marco Joseph', number=134, shift=Shift.DAY, rate=13,
                         hour=35, account_num='', amount=72)
    worker2 = Member401k(name='Angela Pittman', number=566, shift=Shift.SWING,
                         rate=11,
                         hour=21, account_num='', amount=172)
    # Instantiate Supervisors object
    supervisor1 = Member401k(name='Zach Mccall', number=456, salary=51680,
                             shift=Shift.NIGHT, num_worker=0, account_num='',
                             amount=550)
    supervisor2 = Member401k(name='Helena Navarro', number=987, salary=71690,
                             shift=Shift.DAY, num_worker=0, account_num='',
                             amount=250)

    print("----------Before All Max Out----------------")
    print("\n***Production Workers***")
    print(worker1)
    print(worker2)
    print("***Supervisor***")
    print(supervisor1)
    print(supervisor2)

    # Change contribute amount
    worker1.contributed_amount = 1000
    supervisor2.contributed_amount = 1000

    print("----------Now All Max Out----------------")
    print("\n***Production Workers***")
    print(worker1)
    print(worker2)
    print("***Supervisor***")
    print(supervisor1)
    print(supervisor2)
"""


# # ====================== End of Client (As a Function) ======================

if __name__ == "__main__":
    main()
