import pywhatkit as kit
import datetime

kalai="7339614080"
kishore="8610846045"

def nam(var_name):
    try:
        return globals()[var_name]
    except KeyError:
        return "Variable not found"
    
def send_whatsapp_message(phone_number, message):
    now = datetime.datetime.now()
    # Schedule the message to be sent 1 minute from now
    hour = now.hour
    minute = now.minute + 2
    try:
        kit.sendwhatmsg(phone_number, message, hour, minute)
        print("Message sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
def data(name,message):
    varname=name
    phone_number="+91"+nam(varname)
    print(phone_number)
    # message = f"Dear {varname.capitalize()}, Kalaiyarasan is on work like busy."
    # txt = input("Enter the message: ")
    if "bot" in  message:
        message = f"Dear {varname.capitalize()}, iam DENVER👾 Kalaiyarasan,s Vritual Assistant, and he is busy right now, he will ping you later, Thankyou."
    else:
        message=message
    send_whatsapp_message(phone_number, message)
    

# if __name__ == "__main__":
#     varname = input("whome you want to text :  ")
    
#     # phone_number="+91"+nam(varname)
#     # print(phone_number)
#     # print(nam)
#     # # message = f"Dear {varname.capitalize()}, Kalaiyarasan is on work like busy."
#     # txt = input("Enter the message: ")
#     # if "bot" in  txt:
#     #     message = f"Dear {varname.capitalize()}, iam DENVER👾 Kalaiyarasan,s Vritual Assistant, and he is busy right now, he will ping you later, Thankyou."
#     # else:
#     #     message=txt
#     # hour = int(input("Enter the hour (24-hour format): "))
#     # minute = int(input("Enter the minute: "))
#
# data("kalai","hello")     