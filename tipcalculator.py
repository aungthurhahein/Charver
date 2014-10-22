class tipCalculator:
    def __init__(self,people,totalbill,percentage):
        self.people = people
        self.totalbill = totalbill
        self.percentage= percentage    
                
    def tip_calculate(self):
        tip =(self.totalbill/self.percentage)/self.people
        total = self.totalbill + tip
        return "Tip: %f and total amount: %f" % (tip,total)
        
def usr_input():
    people = int(raw_input("Number of people: "))
    totalbill= float(raw_input("Total bill amount: "))
    percentage= float(raw_input("Tip percentage(1-100):"))
    tip = tipCalculator(people,totalbill,percentage)        
    print tip.tip_calculate()

usr_input()
