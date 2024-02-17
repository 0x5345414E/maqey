# ~/.oh-my-zsh/custom/plugins/marquee/marquee.plugin.zsh

# Function to start the Python marquee script
start_marquee() {
    # path to the marqey.py script
    python3 /Users/dev/Development/marqey/marqey.py &
    MARQUEE_PID=$!
}

# Function to stop the marquee
stop_marquee() {
    if [[ -n $MARQUEE_PID ]]; then
        kill $MARQUEE_PID
        unset MARQUEE_PID
    fi
}

# Automatically start the marquee when a new shell session is started
start_marquee

# Optionally, stop the marquee when the shell session ends
trap stop_marquee EXIT