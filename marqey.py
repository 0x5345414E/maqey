import requests
from bs4 import BeautifulSoup
import curses
import time

"""Global variables for fetching headlines"""
last_fetch_time = 0
fetch_interval = 300  # 5 minutes


def fetch_ap_headlines(url="https://apnews.com/"):
    """Fetch the latest headlines from the AP News website."""
    global last_fetch_time
    current_time = time.time()
    if current_time - last_fetch_time < fetch_interval:
        print("Fetching headlines skipped due to rate limiting.")
        return None

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        headlines = [
            headline.get_text().strip()
            for headline in soup.select("bsp-custom-headline h3")
        ]
        last_fetch_time = current_time
        return headlines
    except Exception as e:
        print(f"Error fetching headlines: {e}")
        return ["Error fetching headlines"]

def display_marquee(stdscr, delay=0.13): # Increase to delay speed in marquee
    """Display a marquee of the latest AP News headlines."""
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Make getch non-blocking
    maxy, maxx = stdscr.getmaxyx()

    headlines = fetch_ap_headlines() or ["No new headlines."]
    text = "   |   ".join(headlines) + " " * maxx  # Add trailing spaces equal to screen width
    pos = maxx  # Start from the right side of the screen

    while True:
        stdscr.erase()  # Clear the screen to avoid flickering
        
        # Calculate the width of the text to be displayed
        text_width = len(text)
        
        # Calculate the position to start displaying text from
        start_pos = pos % (text_width + maxx)
        
        # Display the text
        # If the starting position of the text is greater than the screen width, it means the
        # text has scrolled off the screen, and we need to start from the beginning
        if start_pos > maxx:
            to_display = text[:maxx]  # Display the beginning of the text
            stdscr.addstr(maxy - 2, 0, to_display)
        else:
            to_display = text[start_pos:start_pos + maxx]
            stdscr.addstr(maxy - 2, 0, to_display)

        stdscr.refresh()
        pos -= 1  # Move text to the left

        # Check if the entire text has scrolled off the left; if so, reset position
        if pos < -text_width:
            pos = maxx  # Reset position to start from the right again

        time.sleep(delay)  # Control the scroll speed

        # Exit on 'q' key press
        if stdscr.getch() == ord('q'):
            break
        
if __name__ == "__main__":
    """Run the marquee in the terminal."""
    curses.wrapper(display_marquee)
