
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    from tkinter import *
    #from tkinter.ttk import *
    from tkinter.filedialog import askdirectory
    from glob import glob
    from dbpf.dbpf_converter import DBPFConverter
    import os.path


    def helloCallBack():
        E1.delete(0, END)
        directory = askdirectory()
        E1.insert(0, directory)


    def initiate_decompression():
        global progress

        files = glob("{}{}*.package".format(E1.get(), os.sep))
        files.extend(glob("{}{}*.objectCache".format(E1.get(), os.sep)))
        files.extend(glob("{}{}*.world".format(E1.get(), os.sep)))

        file_count = len(files)
        current_file = 0
        for file in files:
            if file.endswith(".objectCache"):
                dbpf_converter = DBPFConverter(file.split(".objectCache")[0], "objectCache", w.get())
            elif file.endswith(".package"):
                dbpf_converter = DBPFConverter(file.split(".package")[0], "package", w.get())
            elif file.endswith(".world"):
                dbpf_converter = DBPFConverter(file.split(".world")[0], "world", w.get())
            else:
                raise Exception("File not recognized")
            current_file += 1
            top.update_idletasks()
        E1.delete(0, END)
        E1.insert(0, "Done converting!")


    top = Tk()
    top.title("TurboTravel Converter - Alpha Software - Will probably explode if you look at it wrong")

    scalevar = IntVar()
    scalevar.set(1)

    w = Scale(top, from_=1, to=multiprocessing.cpu_count(),variable=scalevar, resolution = 1, orient=HORIZONTAL)
    label = Label(top,text= "CPU Threads")

    L1 = Label(top, text="Folder To Convert")
    E1 = Entry(top, width = 70)

    B = Button(top, text ="Select Directory", command = helloCallBack)
    b1 = Button(top,text="Convert", command = initiate_decompression)

    w.grid(row=3, column=2)
    label.grid(row=3, column=3)
    L1.grid(row=0, column=1)
    E1.grid(row=1, column=1)

    B.grid(row=1, column=2)
    E1.grid(row=1, column=1)
    b1.grid(row=1, column=3)


    top.mainloop()