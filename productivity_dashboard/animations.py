def ease(t):
    return 1 - (1-t)**3

def grow(widget, start, end, property, steps=15, delay=15):
    #change
    delta = (end-start) / steps
    current = start

    def step():
        #grab current from outside the function
        nonlocal current
        current += delta
        
        if property == "WIDTH":
            widget.configure(width=current)
        
        if property == "HEIGHT":
            widget.configure(height=current)

        #if not at beginning (for closing), not at end (for opening)
        if (delta > 0 and current < end) or (delta < 0 and current > end):
            widget.after(delay, step)
        else:
            #snap to end
            if property == "WIDTH":
                widget.configure(width=end)
            if property == "HEIGHT":
                widget.configure(height=end)
    
    step()