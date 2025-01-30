import numpy as np
import cv2
import pyautogui
import pytesseract
import keyboard
import time
from PIL import Image
import threading
import firebase_admin
from firebase_admin import credentials, firestore




# Ensure required packages are installed:
# pip install pynput imagehash opencv-python numpy pyautogui pillow pytesseract keyboard firebase_admin pyrebase4

# Note: Install the tesseract training dataset from https://github.com/UB-Mannheim/tesseract/wiki
# Add "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" to your PATH environment variable



# Load Firebase credentials
cred = credentials.Certificate("count-e929b-firebase-adminsdk-fbsvc-316f47b0f1.json")
firebase_admin.initialize_app(cred)
# Access Firestore database
db = firestore.client()
doc_ref = db.collection("Count").document("Data")
#doc_ref -> Path to data 
# Read a document
doc = doc_ref.get()
class AutoTextBot:
    
    
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
    
    @staticmethod
    def colorAmI():
        if doc.exists:
            print("Server Is Up \n----------------------------------")
        else:
            # Add a document
            doc_ref.set({"Stat":"Stop","User": "Red", "Count": "1"})
            print("help")
        
        intdata = doc.to_dict()
        
        uinput = input('Stat: '+ str(intdata) +' \n 1: Start \n 2: Join \n 3: If Stat: None\n')
        if uinput == "1":
            
            if intdata == None or intdata['Stat'] == "Live":
                print("Try Joing. Cant Start")
                return 'none'
            else:
                uinput = input('Entry currernt count \n')
                doc_ref.update({
                        'Stat': 'Live',
                        "Count": str(uinput),
                        "User": "Red"
                                })
                print("You Are Red")
                
                return 'red'
            
        elif uinput == "2":
            
            if intdata == None or intdata['Stat'] == "Stop":
                print("Try Start. Cant Join")
                return 'none'
            else:
                print("You Are Blue")
                return 'blue'
        
        elif uinput == "3":
            print("Start Up Again")
            return "none"
            
        else:
            print("wrong input")
            return "none"
        
    

    @staticmethod
    def locate_image(image_path, confidence=0.9):
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                print("Image found at:", location)
                return location
            else:
                print("Image not found")
                return None
        except Exception as e:
            print("Error locating image:", e)
            doc = doc_ref.get()
            intdata = doc.to_dict()
            print(intdata)
            return None

    @staticmethod
    def contains_image(template_path, screenshot_path, threshold=0.9):
        try:
            template = cv2.imread(template_path)
            screenshot = cv2.imread(screenshot_path)
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            return max_val > threshold
        except Exception as e:
            print("Error in image comparison:", e)
            
            return False
    '''
    @staticmethod
    def extract_text_from_image(image_path):
        try:
            #img = Image.open(image_path)
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
            text = pytesseract.image_to_string(thresh)
            #print(text)
            return text
        except Exception as e:
            print("Error extracting text from image:", e)
            return ""
    ''' 

    def run(self,inputlcation,userIcon, colorU ):
        event = threading.Event()

        def stop():
            event.set()
            doc_ref.update({
                        'Stat': 'Stop',
                                })
            print("Stopping bot...")

        keyboard.add_hotkey("esc", stop)

        while not event.is_set():
            image_path_match = inputlcation 

            location = self.locate_image(image_path_match)
            if not location:
                pass
                #break
            else:
                    
                x, y, width, height = int(location.left), int(location.top )- 150, 290, 80
                screenshot = pyautogui.screenshot(region=(x, y, width, height))
                screenshot_path = r'boxofCompare.png'
                screenshot.save(screenshot_path)

                user_icon_path = userIcon 
                has_image = self.contains_image(user_icon_path, screenshot_path)
                
                #This mean it is the user Turn
                if not has_image:
                    print("This is the line you thinking about -----------------")
                    doc = doc_ref.get()
                    intdata = doc.to_dict()
                    print(intdata)
                    try:
                        #colorU
                        # i want to check if it is my color aka my turn, and update the value by and increase by one
                        # location tag
                        pyautogui.click(x + width / 2, y + 50)
                        countvalue = int(intdata['Count'])+1
                        
                        keyboard.write(str(countvalue))
                        
                        keyboard.press_and_release('enter')
                        pyautogui.moveTo(0, 0)
                        
                        doc_ref.update({
                        'User': str(colorU),
                        'Count': str(countvalue)
                                })
                        
                        
                    except Exception as e:
                        print("Error typing or clicking:", e)
                        
                    ''' 
                    text = self.extract_text_from_image(screenshot_path)
                    print("Extracted text:", text)
                    try:
                        numbers = [int(item) for item in text.split() if item.isdigit()]
                        number_to_type = numbers[-1] + 1 if numbers else "1"
                        if isinstance(number_to_type, int):
                            pyautogui.click(x + width / 2, y + 50)
                            keyboard.write(str(number_to_type))
                            keyboard.press_and_release('enter')
                            pyautogui.moveTo(0, 0)
                        else:
                            pass
                    except Exception as e:
                        print("Error typing or clicking:", e)
                    '''

            time.sleep(5)

if __name__ == '__main__':
    
    bot = AutoTextBot()
    color= bot.colorAmI()
    if color == "none":
        print("what")
    else:
        print("You Color")
        print(color)
        bot.run(r'countLocation.png',r'userIcon.png', color)

    


