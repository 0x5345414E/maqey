# Define a new function to start the Python marquee script
function start_marquee() {
  # Path to your Python script
  local script_path="~/path/to/marquee.py"
  
  # Execute the Python script in the background
  python3 "$script_path" &
  
  # Save the background job's PID so you can stop it later if needed
  MARQUEE_PID=$!
}

# Optionally, define a function to stop the marquee
function stop_marquee() {
  if [[ -n $MARQUEE_PID ]]; then
    kill $MARQUEE_PID
    unset MARQUEE_PID
  fi
}

# Automatically start the marquee when a new shell session is started
start_marquee

# Ensure the marquee is stopped when the shell session ends
trap stop_marquee EXIT
