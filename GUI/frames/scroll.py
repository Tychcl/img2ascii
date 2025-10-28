import customtkinter
class ScrollFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
        #self.frame = ScrollFrame(master=self, width=300, height=200)
        #self.frame.grid(row=0, column=0, padx=20, pady=20)
        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)