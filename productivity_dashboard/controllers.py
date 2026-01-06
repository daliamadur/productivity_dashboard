def t_time(self):
    return
    date.configure(text=format_date(datetime.now()))
    time.configure(text=format_time(datetime.now()))
    after(1, self.update_time)