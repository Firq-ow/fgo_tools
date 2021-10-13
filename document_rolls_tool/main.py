import tkinter as tk


def ce_5():
    print("5* CE")




top = tk.Tk()
top.columnconfigure(0, weight=1, minsize=75)
top.rowconfigure(0, weight=1, minsize=50)

# Create buttons for CEs

frm_ce = tk.Frame(borderwidth=1)

lbl_ce = tk.Label(master=frm_ce, text="CEs", fg="#000000")
btn_ce_5 = tk.Button(master=frm_ce, text="5 Star CE", command=ce_5)
btn_ce_4 = tk.Button(master=frm_ce, text="4 Star CE")
btn_ce_3 = tk.Button(master=frm_ce, text="3 Star CE")
lbl_ce.pack()
btn_ce_5.pack()
btn_ce_4.pack()
btn_ce_3.pack()


frm_ce.grid(row=0, column=0, padx=5, pady=5, sticky="n")

# Create buttons for Servants

frm_svnt = tk.Frame(borderwidth=1)

lbl_svnt = tk.Label(master=frm_svnt, text="Servants", fg="#000000")
btn_svnt_5 = tk.Button(master=frm_svnt, text="5 Star Servant")
brn_svnt_4 = tk.Button(master=frm_svnt, text="4 Star Servant")
btn_svnt_3 = tk.Button(master=frm_svnt, text="3 Star Servant")
lbl_svnt.pack()
btn_svnt_5.pack()
brn_svnt_4.pack()
btn_svnt_3.pack()

frm_svnt.grid(row=0, column=1, padx=5, pady=5, sticky="n")

# Create result display window

frm_result = tk.Frame(width=200, height=500, bg="#101010")
frm_result.grid(row=0, column=2)


# Create Window and listen for events

top.mainloop()
