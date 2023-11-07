# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Candidate:
    def __init__(self, first_name, last_name, DOB, cand_ID, party, SOC, position):
        self.first_name = first_name
        self.last_name = last_name
        self.DOB = DOB
        self.cand_ID = cand_ID
        self.party = party
        self.SOC = SOC
        self.position = position
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    user = Candidate("Jon","Snow",1/23/23,0,"Democrat","425-11-2222","Dog Catcher")
    print(user.first_name)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
