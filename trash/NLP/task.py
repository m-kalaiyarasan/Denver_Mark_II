import schedule
import time

# Function to schedule a reminder
def schedule_reminder(event_time, event_name):
    schedule.every().day.at(event_time).do(lambda: print(f"Reminder: You have {event_name} Now"))

# Main function to interact with the user and schedule reminders
def main():
    print("Welcome to the reminder scheduler!")

    while True:
        user_input = input("Enter your event in the format 'event_name at HH:MM am/pm' (e.g., 'online class at 08:30 pm'), or 'quit' to exit: ")

        if user_input.lower() == 'quit':
            break
        
        try:
            parts = user_input.split(' at ')
            event_name = parts[0].strip()
            event_time = parts[1].strip()
            
            # Ensure time format is correct
            time_obj = time.strptime(event_time, "%I:%M %p")
            event_time = time.strftime("%H:%M", time_obj)
            
            # Schedule the reminder
            schedule_reminder(event_time, event_name)
            print(f"Reminder scheduled for {event_name} at {event_time}")
        
        except Exception as e:
            print(f"Error scheduling reminder: {e}")
    
    # Main loop to execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)  # Adjust sleep time as needed

if __name__ == "__main__":
    main()
