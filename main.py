from ttkthemes import ThemedTk
from dashboard import Dashboard

win = ThemedTk(theme="equilux")
dashboard = Dashboard(win)
win.mainloop()
