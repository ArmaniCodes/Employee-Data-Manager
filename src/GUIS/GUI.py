from src.Modules import *
from src.ManageEmployees.manageFile import getEmployeeList, createTable
from src.GUIS.newEmployeeGUI import newEmployeeWdw
from src.GUIS.editEmployeeGUI import employeeInfoWdw
from src.ManageEmployees.sortEmployees import searchForEmployee, sortByName,sortBySalary,sortByID
from src.GUIS.graphGUI import graphGUI

class EmployeeGui:
    def __init__(self):
        #Dark Theme
        self.root = tb.Window(themename="darkly")
        #Window Size
        self.root.geometry("1150x500")
        self.root.resizable(False, False)
        self.root.title("Employee Dashboard")
        self.employeeCount = 0
        self.buttonList = {}

        #Icon
        self.root.iconbitmap('windowIcon.ico')

        #Store instance of GUI for later Use
        self.instance = self
        self.createGui()

        #Transparent Button Style
        stylex = tb.Style()
        background_color = self.root.cget("background")
        stylex.configure("Custom.TButton", background=background_color, bordercolor=background_color,
                         lightcolor=background_color, darkcolor=background_color, highlightthickness=0, bd=0)


        #Store graphGUI instance
        self.graph_GUI = graphGUI(self.root)

        createTable()
        self.root.mainloop()

    def createGui(self):
        frame = tb.Frame(self.root)

        frame.pack(side="left",fill = "y")
        scrollbar = tb.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        #Setup buttons
        button = tb.Button(self.root, text="LOAD EMPLOYEES", command=self.LoadEmployees, bootstyle="light-outline",
                           width=17)
        button.pack(side="bottom", anchor="w")


        button = tb.Button(self.root, width=17, bootstyle="light-outline", text="NEW EMPLOYEE",
                           command=lambda: newEmployeeWdw(self.root, self.instance)         )
        button.pack(side="bottom", anchor="w")

        #Employee Count Label
        self.empCountLabel = tb.Label(self.root, text="Employees: 0", bootstyle="success", width=17)
        self.empCountLabel.pack(side="bottom", anchor="w")

        #Canvas for scroll bar
        self.canvas = tb.Canvas(frame, yscrollcommand=scrollbar.set, width=150, height=300)
        self.canvas.pack(side="left", fill="y")
        scrollbar.configure(command=self.canvas.yview)

        #Create employeeFrame then sortingFrame
        self.createEmployeeFrame()
        self.createSortingFrame()

    #Remove employee from frame
    def removeEmployeeFromFrame(self,buttonInstance):
        self.employeeCount -= 1
        del self.buttonList[buttonInstance.cget("text")]
        buttonInstance.destroy()
        self.updateEmployeeLabel(self.employeeCount)

    #Frame all about sorting Employee Data
    def createSortingFrame(self):
        #Style for the frame and label
        stylex = tb.Style()
        stylex.configure("My.TFrame", background="gray20", borderwidth=2, relief="solid")
        stylex.configure("Custom.TLabel", background="gray20", bordercolor="gray20",
                         lightcolor="gray20", darkcolor="gray20", bd=0)

        self.sortingFrame = tb.Frame(self.root, style="My.TFrame", width=150, height=250)
        self.sortingFrame.pack(side="left", anchor="n", padx=20, pady=20)

        #Sorting Buttons
        tb.Button(self.root, text="Sort Alphabetically", bootstyle="success", width=17,
                  command=lambda: sortByName(self.LoadSortedEmployees)).place(x=195, y=30)
        tb.Button(self.root, text="Sort By Employee ID", bootstyle="success", width=18,
                  command=lambda: sortByID(self.LoadSortedEmployees)).place(x=192, y=70)
        tb.Button(self.root, text="Sort By Salary", bootstyle="success", width=17,
                  command=lambda: sortBySalary(self.LoadSortedEmployees)).place(x=195, y=110)

        tb.Label(self.sortingFrame, text="Search By Full Name", width=18, style="Custom.TLabel").place(x=20, y=130)
        searchEntry = tb.Entry(self.sortingFrame, width=18)
        searchEntry.place(x=15, y=150)
        tb.Button(self.sortingFrame, width=10, text="Search", bootstyle="success",
                  command=lambda: searchForEmployee(self.root, self.instance, searchEntry.get())).place(x=34, y=185)


    def createEmployeeFrame(self):
        self.inner_frame = tk.Frame(self.canvas)
        #Creates window
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    #Adds new employee to Frame and updates scrollingFrame
    def addEmployeeToFrame(self,name):
        self.employeeCount += 1
        b = tb.Button(self.inner_frame, width=20, text=name, style="Custom.TButton")
        b.configure(command=lambda t=name, button=b: employeeInfoWdw(self.root, t, self.instance))
        b.pack(fill="x")
        self.buttonList[name] = b
        self.updateScrollingFrame()
        self.updateEmployeeLabel(self.employeeCount)

    def clearEmployees(self):
        self.employeeCount = 0
        #Destroying this clears all it's children AKA employees
        self.inner_frame.destroy()
        #Create new frame with no employees
        self.createEmployeeFrame()


    #Updates frame when new employees Loaded/Deleted
    def updateScrollingFrame(self):
        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def updateEmployeeLabel(self,employeeCount):
        self.empCountLabel.configure(text = "Employees: " + str(employeeCount))

    def LoadEmployees(self):
        employees = getEmployeeList()
        if employees:
            self.clearEmployees() #Clear Previous Employees
            self.buttonList.clear()

            #employees is stored as a list of tuples, i is a tuple, i[1] indexs the name, to see what the other indexs are stored as, check manageFile format
            for i in employees:
                b = tb.Button(self.inner_frame, width=20, text=i[1], style="Custom.TButton")
                b.configure(command=lambda t=i[1], button=b: employeeInfoWdw(self.root, t, self.instance))
                self.buttonList[i[1]] = b
                b.pack(fill="x")

            self.employeeCount = len(employees)
            self.updateScrollingFrame()
            self.updateEmployeeLabel(self.employeeCount)
            self.graph_GUI.createGraphs(employees)
        else:
            self.clearEmployees()

    def LoadSortedEmployees(self,employees):
        self.clearEmployees()
        self.buttonList.clear()

        # employees is a list of tuples, i is a tuple, i[1] is the name of the employee
        for i in employees:
            b = tb.Button(self.inner_frame, width=20, text=i[1], style="Custom.TButton")
            b.configure(command=lambda t=i[1], button=b: employeeInfoWdw(self.root, t, self.instance))
            self.buttonList[i[1]] = b
            b.pack(fill="x")
        self.employeeCount = len(employees)
        self.updateScrollingFrame()
