py_files = ["ChroMS_application.py", "Custom_tkinter_widget_classes.py", "HPLC_MS_data_classes.py",
            "HPLC_MS_diagram_classes.py", "Main_GUI_parameters.py", "Multifunctional_backbones.py",
            "Object_manager_backbones.py", "Text_outputs_functions.py", "Widget_manipulation_functions.py",
            "Path_manipulation_functions.py"]
spacing = len(max(py_files)) + 5
print("{0:{1}} {2}".format("File", spacing,"Length"))
line_sum = 0
for py_file in py_files:
    file = open(py_file, "r")
    line_number = 0
    for line in file:
        pass
        line_number += 1
        #print(line)
    file.close()
    print("{0:{1}} {2}".format(py_file, spacing, line_number))
    line_sum += line_number
    
print("{0:{1}} {2}".format("Total", spacing, line_sum))
