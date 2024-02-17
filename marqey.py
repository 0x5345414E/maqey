import curses
import time

def marquee(win):
    text = "Fetch some headlines... "
    delay = 0.05
    curses.curs_set(0)  # Hide cursor

    # Get maximum dimensions of the window
    maxy, maxx = win.getmaxyx()

    # Calculate the position to start the text to have it centered
    text_length = len(text)
    if maxx < text_length:
        start_pos = 0
    else:
        # Center the text
        start_pos = (maxx - text_length) // 2

    pos = maxx  # Start position for the scrolling effect

    try:
        while True:
            win.clear()  # Clear the window to create the margin effect
            win.addstr(maxy - 2, 0, " " * maxx)
            text_pos = pos % maxx
            if text_pos + text_length > maxx:
                # If the text wraps, only show the part that fits
                win.addstr(maxy - 2, text_pos, text[max(0, maxx - text_pos):])
            else:
                win.addstr(maxy - 2, text_pos, text)

            win.refresh()  # Refresh the window to update the text display
            pos -= 1  # Move text left
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
    finally:
        curses.curs_set(1)  # Show cursor again

if __name__ == "__main__":
    curses.wrapper(marquee)
