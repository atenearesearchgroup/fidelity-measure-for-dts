# utils.sh

# Function to ask a yes or no question and proceed based on the response
ask_question() {
    local question="$1"
    local response

    while true; do
        read -p "$question (y/n): " response
        case "$response" in
            [Yy]*)
                # echo "Continuing with execution..."
                return 0
                ;;
            [Nn]*)
                # echo "Execution stopped."
                return 1
                ;;
            *)
                echo "Invalid response. Please answer with 'y' or 'n'."
                ;;
        esac
    done
}
