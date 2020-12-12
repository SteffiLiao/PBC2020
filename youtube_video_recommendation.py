import tkinter as tk
import tkinter.font as tkFont

class YoutubeSearch(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.create_widgets()
        self.master.title("Special YouTube Recommendation")
        self.master.geometry("800x600")
        
    def create_widgets(self):
        f1 = tkFont.Font(size=20, family="王漢宗細黑體繁")  # slant="italic"斜體
        f2 = tkFont.Font(size=14, family="王漢宗細黑體繁")
        f3 = tkFont.Font(size=16, family="王漢宗細黑體繁")

        self.scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scrollbar.grid(row=1, column=1, sticky='we')
        
        self.search = tk.Label(self, text="搜尋", font=f1, height=2, width=7)  # 搜索詞
        self.search_content = tk.Entry(self, bd=3,font=f2,width=40,
                                       xscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.search_content.xview)
        
        self.selection = tk.Label(self, text="篩選器",
                                  font=f1, height=1, width=10, bg="#FFA07A")
        self.not_search = tk.Label(self, text="不要出現", font=f3, height=2, width=10)  # 不想看到的關鍵字
        self.not_search_content = tk.Entry(self, bd=3, font=f2, width=30)
        
        self.order = tk.Label(self, text="排序依據", font=f3, height=1, width=10)
        
        self.relevance = tk.Checkbutton(self, text="關聯性", font=f2)
        self.date = tk.Checkbutton(self, text="上傳日期", font=f2)
        self.like_ratio = tk.Checkbutton(self, text="讚踩比", font=f2)
        self.view = tk.Checkbutton(self, text="觀看次數", font=f2)
        
        self.go = tk.Button(self, command=self.click_go,
                            font=f3, text="GO", bg='#FFFACD',fg='#FF8C00')  # bg背景色；fg字體色
        
        
        # 設定每個功能的位置
        self.search.grid(row=0, column=0)
        self.search_content.grid(row=0, column=1, ipady=8)
        
        self.selection.grid(row=2, column=0)
        self.not_search.grid(row=3, column=0)
        self.not_search_content.grid(row=3, column=1, ipady=6)
        self.order.grid(row=4, column=0)
        
        self.relevance.grid(row=5, column=0)
        self.date.grid(row=5, column=1)
        self.view.grid(row=6, column=1)
        self.like_ratio.grid(row=6, column=0)
        self.go.grid(row=10, column=0, columnspan=2)
    
    def click_go(self):
        # 讀取搜索欄資訊
        pass
 
    
    
        
yt_recom = YoutubeSearch()
yt_recom.mainloop()


















'''
待新增其他功能：
不想見到的關鍵字以逗號隔開

'''