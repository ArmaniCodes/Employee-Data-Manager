from src.Modules import *
from src.ManageEmployees.manageFile import get_employee_data, update_employee_data,delete_employee_by_id
from src.InputValidate.inputValidation import calculate_age, checkBirthDate, checkSalary

def save(new_window,entryList):
    #Validate DOB and Salary since user can change and put incorrect format
    if not checkBirthDate(entryList) or not checkSalary(entryList):
        return False

    #Since these are just text and not instances of entries we must remove them before the below for loop runs
    name = entryList["Name"]
    emID = entryList["Employee ID"]
    del entryList["Name"]
    del entryList["Employee ID"]
    for k, v in entryList.items():
        entryList[k] = v.get()

    newList = {name : entryList}
    #Recalculate Age incase DOB was ammended
    newList[name]["Age"] = calculate_age(newList[name]["Date Of Birth"])
    newList[name]["Employee ID"] = emID
    newList[name]["Salary"] = int(newList[name]["Salary"])

    #Store info and destroy window
    update_employee_data(name,newList)
    new_window.destroy()

    # We delete users by their employee ID not their name, this is to ensure we don't delete the wrong person
def delEmployeeHelper(empID,rootwindow,guiInstance,buttonInstance):
    delete_employee_by_id(empID)
    guiInstance.removeEmployeeFromFrame(buttonInstance)
    rootwindow.destroy()

def employeeInfoWdw(root,name,guiInstance):
    #Get the button that stores this individual employee's name
    buttonInstance = guiInstance.buttonList[name]

    #Window specs
    new_window = tb.Toplevel(root)
    new_window.title(name + "'s info")
    new_window.geometry("600x500")
    new_window.resizable(False, False)
    new_window.iconbitmap('windowIcon.ico')

    #Title
    label = tb.Label(new_window, text=name + "'s info, override if necessary ", font=("Helvetica", 13)).pack(pady=5)

    #Employee Data is stored as a tuple which is why we index to retrieve data
    entryList = {}
    employee_data = get_employee_data(name)

    #Save Button
    close_button = tb.Button(new_window, text="Save/Close", command=lambda: save(new_window, entryList),
                             bootstyle="success,outline")
    close_button.pack(side="bottom")

    #Delete Button employee_data[8] is the employee ID to see other indexs check managefile key order
    delete_button = tb.Button(new_window, text="DELETE",
                              command=lambda: delEmployeeHelper(employee_data[8], new_window, guiInstance, buttonInstance),
                              bootstyle="danger,outline")
    delete_button.place(relx=0, rely=1, anchor="sw")





    #Frames to hold widgets
    details_frame = tb.Frame(new_window, width=0)
    details_frame.pack(side="left", anchor="n", pady=15, padx=10)

    details_frame2 = tb.Frame(new_window, width=200)
    details_frame2.pack(side="right", anchor="n", pady=15, padx=10, expand=True, fill="x")

    #Personal information Label
    tb.Label(details_frame, text="Personal Information", bootstyle="success", font=("Helvetica", 11)).grid(row=0,
                                                                                                           column=0,
                                                                                                           pady=10)
    #Store full employee name, employee_data[1] is the name
    entryList["Name"] = employee_data[1]


    # We don't store first and last name since we won't be modifying it anyway
    # Create labels and entry widgets for employee first Name
    tb.Label(details_frame, text="Employee First Name:").grid(row=1, column=0, sticky="e", pady=(0, 5))
    name_entry = tb.Label(details_frame, width=15, text=name.split()[0])
    name_entry.grid(row=1, column=1, sticky="w", pady=(0, 5))
    # Create labels and entry widgets for employee last Name
    tb.Label(details_frame, text="Employee Last Name:").grid(row=2, column=0, sticky="e", pady=(0, 5))
    last_name_entry = tb.Label(details_frame, width=15, text=name.split()[1])
    last_name_entry.grid(row=2, column=1, sticky="w", pady=(0, 5))


    # Create labels and entry widgets for employee DOB
    tb.Label(details_frame, text="Employee Date of Birth:").grid(row=3, column=0, sticky="e", pady=(0, 5))
    dob_entry = tb.Entry(details_frame, width=15)
    dob_entry.insert(0, employee_data[2])   # employee_data[2] stores the DOB
    dob_entry.grid(row=3, column=1, sticky="w", pady=(0, 5))
    entryList["Date Of Birth"] = dob_entry

    # Create labels and combo widgets for employee Sex
    # We use combobox instead of entry to ensure input cannot be invalid
    tb.Label(details_frame, text="Employee Sex:").grid(row=4, column=0, sticky="e", pady=(0, 5))
    sex_combo = tb.Combobox(details_frame, values=["M", "F"], width=13, state="readonly")
    sex_combo.set(employee_data[3])  # Set the initial text displayed in the dropdown to employee sex
    sex_combo.grid(row=4, column=1, sticky="w", pady=(0, 5))
    entryList["Sex"] = sex_combo

    # Create labels and entry widgets for employee Race
    tb.Label(details_frame, text="Employee Race:").grid(row=5, column=0, sticky="e", pady=(0, 5))
    race_entry = tb.Entry(details_frame, width=15)
    race_entry.insert(0, employee_data[4])   #employee_data[4] is the race
    race_entry.grid(row=5, column=1, sticky="w", pady=(0, 5))
    entryList["Race"] = race_entry

    #Contact Information Label
    tb.Label(details_frame, text="Contact Information", bootstyle="success", font=("Helvetica", 11)).grid(row=6,
                                                                                                          column=0,
                                                                                                          sticky="e",
                                                                                                          pady=22)
    # Create labels and entry widgets for employee Email
    tb.Label(details_frame, text="Employee Email:").grid(row=7, column=0, sticky="e", pady=(0, 5))
    email_entry = tb.Entry(details_frame, width=17)
    email_entry.insert(0,employee_data[5])
    email_entry.grid(row=7, column=1, sticky="w", pady=(0, 5))
    entryList["Email"] = email_entry

    # Create labels and entry widgets for employee Phone
    tb.Label(details_frame, text="Employee Phone:").grid(row=8, column=0, sticky="e", pady=(0, 5))
    phone_entry = tb.Entry(details_frame, width=17)
    phone_entry.insert(0, employee_data[6])
    phone_entry.grid(row=8, column=1, sticky="w", pady=(0, 5))
    entryList["Phone"] = phone_entry

    # Create labels and entry widgets for employee Address
    tb.Label(details_frame, text="Employee Address:").grid(row=9, column=0, sticky="e", pady=(0, 5))
    address_entry = tb.Entry(details_frame, width=17)
    address_entry.insert(0, employee_data[7])
    address_entry.grid(row=9, column=1, sticky="w", pady=(0, 5))
    entryList["Address"] = address_entry

    # Create label widgets for employee ID
    # Since employee ID cannot be changed we will not be using an entry!
    tb.Label(details_frame, text="Employee ID:").grid(row=10, column=0, sticky="e", pady=(0, 5))
    ID_entry = tb.Label(details_frame, width=17, text=employee_data[8])
    ID_entry.grid(row=10, column=1, sticky="w", pady=(0, 5))
    entryList["Employee ID"] = employee_data[8]

    #Employment Details Label
    tb.Label(details_frame2, text="Employment Details", bootstyle="success", font=("Helvetica", 11)).grid(row=0,
                                                                                                          column=3,
                                                                                                          pady=10)
    # Create labels and entry widgets for employee Job Title
    tb.Label(details_frame2, text="Job Title:").grid(row=1, column=3, pady=(0, 5), sticky="e")
    job_entry = tb.Entry(details_frame2, width=15)
    job_entry.insert(0,  employee_data[9])
    job_entry.grid(row=1, column=4, sticky="w", pady=(0, 5))
    entryList["Job Title"] = job_entry

    # Create labels and entry widgets for employee Job Department
    tb.Label(details_frame2, text="Department:").grid(row=2, column=3, pady=(0, 5), sticky="e")
    department_entry = tb.Entry(details_frame2, width=15)
    department_entry.insert(0, employee_data[10])
    department_entry.grid(row=2, column=4, sticky="w", pady=(0, 5))
    entryList["Department"] = department_entry

    # Create labels and entry widgets for employee Superior
    tb.Label(details_frame2, text="Manager/Leader:").grid(row=3, column=3, pady=(0, 5), sticky="e")
    manager_entry = tb.Entry(details_frame2, width=15)
    manager_entry.insert(0, employee_data[11])
    manager_entry.grid(row=3, column=4, sticky="w", pady=(0, 5))
    entryList["Manager/Leader"] = manager_entry

    # Create labels and entry widgets for employee Job Status
    # We use combobox instead of entry because it's easier to inputvalidate since we will be needing it for stats for graphing
    tb.Label(details_frame2, text="Employment Status:").grid(row=4, column=3, pady=(0, 5), sticky="e")
    status_combo = tb.Combobox(details_frame2, values=["Full Time", "Part Time", "Internship", "Contract"], width=13,
                               state="readonly")
    status_combo.set(employee_data[12])  # Set the initial text displayed in the dropdown
    status_combo.grid(row=4, column=4, sticky="w", pady=(0, 5))
    entryList["Status"] = status_combo

    # Create labels and entry widgets for employee Salary
    tb.Label(details_frame2, text="Salary:").grid(row=5, column=3, pady=(0, 5), sticky="e")
    salary_entry = tb.Entry(details_frame2, width=15)
    salary_entry.insert(0,employee_data[13])
    salary_entry.grid(row=5, column=4, sticky="w", pady=(0, 5))
    entryList["Salary"] = salary_entry

    #Performance & Development Label
    tb.Label(details_frame2, text="Performance & Development", bootstyle="success", font=("Helvetica", 11)).grid(row=6,
                                                                                                                 column=3,
                                                                                                                 columnspan=2,
                                                                                                                 pady=10)
    # Create labels and entry widgets for employee Attendance
    tb.Label(details_frame2, text="Time and Attendance:").grid(row=7, column=3, pady=(0, 5), sticky="e")
    time_entry = tb.Entry(details_frame2, width=15)
    time_entry.insert(0, employee_data[14])
    time_entry.grid(row=7, column=4, sticky="w", pady=(0, 5))
    entryList["Time and Attendance"] = time_entry

    # Create labels and entry widgets for employee Skills
    tb.Label(details_frame2, text="Certifications and Skills:").grid(row=8, column=3, pady=(0, 5), sticky="e")
    certs_entry = tb.Entry(details_frame2, width=15)
    certs_entry.insert(0, employee_data[15])
    certs_entry.grid(row=8, column=4, sticky="w", pady=(0, 5))
    entryList["Certifications and Skills"] = certs_entry

    # Create labels and entry widgets for employee Programs
    tb.Label(details_frame2, text="Training/Programs:").grid(row=9, column=3, pady=(0, 5), sticky="e")
    training = tb.Entry(details_frame2, width=15)
    training.insert(0, employee_data[16])
    training.grid(row=9, column=4, sticky="w", pady=(0, 5))
    entryList["Training/Programs"] = training

    # Create labels and entry widgets for employee extra Info
    tb.Label(details_frame2, text="Any Extra Information:").grid(row=10, column=3, pady=(0, 5), sticky="e")
    extra_entry = tb.Entry(details_frame2, width=15)
    extra_entry.insert(0, employee_data[17])
    extra_entry.grid(row=10, column=4, sticky="w", pady=(0, 5))
    entryList["Extra Information"] = extra_entry