
import cv2
import os
import numpy as np

# subjects = ["", "Pushpraj", "Ishita", "Papa"]
subjects = os.listdir('/var/www/html/face-detection/ai-recognition/cv2/aligned_faces')
unRecognisedDataset = [];
unRecognisedTestDataset = [];
# print(subjects) #here the location is ‘/usr’
# # os.open(subjects[0])
# for i in range(len(subjects)):
#     print(i)
#     os.rename('./aligned_faces/'+subjects[i],'./aligned_faces/s'+str(i))


nameArrOfSubjects = ['katrina', 'kapil_dev', 'Abhishek Bachchan', 'Om Puri', 'amir-khan', 'sanjay-dutt', 'Adam Sandler', 'ranveer-singh', 'Papa', 'baav', 'Sidharth Malhotra', 'Arbaaz Khan', 'Kartik Aaryan', 'Jeremy Renner', 'krushang', 'Rishi Kapoor', 'alia', 'john-cena', 'paresh_raval', 'Bobby Deol', 'Varun Dhawan', 'Vivek Oberoi', 'jayveersinh', 'devang', 'mummy', 'Baa', 'sachin', 'gambhir', 'Tom Hanks', 'vin deisel', 'jonny_liver', 'Nawazuddin Siddiqui', 'Ishita', 'Samuel L. Jackson', 'Jackie Shroff', 'disha', 'Arshad Warsi', 'Chris Pratt', 'Amrish Puri', 'Emraan Hashmi', 'ben_afflek', 'robert downey jr', 'Anil Kapoor', 'dipika', 'Tom Cruise', 'Naseeruddin Shah', 'saif', 'Karan Johar', 'Ryan Gosling', 'jerry_seinfeld', 'Mark Ruffalo', 'ajay_devgan', 'Rajpal Yadav', 'dhoni', 'Himesh Reshammiya', 'Riteish Deshmukh', 'Dwayne "The Rock" Johnson', 'Aditya Roy Kapur', 'Pushpraj', 'Dharam Singh Deol', 'virat', 'Mark Wahlberg', 'tiku', 'amitab bachan', 'shahid-kapoor', 'Sunny Deol', 'buntybhai', 'anushka', 'Akkineni Nagarjuna', 'Nana Patekar', 'Prabhas', 'malhar', 'kareena', 'John Abraham', 'Akshaye Khanna', 'Sonu Sood', 'kuldip-shiddhpura', 'Prabhu Deva', 'Kay Kay Menon', 'Chris Evans', 'tiger_shroff', 'raam', 'Rajinikanth', 'Chris Hemsworth', 'Arjun Kapoor', 'elton_john', 'madonna', 'mindy_kaling', 'sunil', 'Jackie Chan', 'Alok Nath', 'savan', 'Dilip Joshi', 'Matt Damon', 'Anu Kapoor', 'priyanka', 'bharat', 'Anupam Kher', 'Ayushman Khurrana', 'Honey Singh', 'ranveer-kapoor', 'akshay-kumar', 'arijit singh', 'Sushant Singh Rajput', 'Ryan Reynolds']



# print(os.listdir('/var/www/html/face-detection/ai-recognition/cv2/aligned_faces/aligned_faces'))

def detect_face(img):
    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #load OpenCV face detector, I am using LBP which is fast
    #there is also a more accurate but slow Haar classifier
    face_cascade = cv2.CascadeClassifier('./lbpcascade_frontalface.xml')
    # face_cascade = cv2.CascadeClassifier('./lbpcascade_frontalface_alt.xml')

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
    
    if (len(faces) == 0):
        return None, None
    
    (x, y, w, h) = faces[0]
    
    #return only the face part of the image
    return gray[y:y+w, x:x+h], faces[0]
def prepare_training_data(data_folder_path):
    
    #------STEP-1--------
    #get the directories (one directory for each subject) in data folder
    dirs = os.listdir(data_folder_path)
    
    #list to hold all subject faces
    faces = []
    #list to hold labels for all subjects
    labels = []
    
    #let's go through each directory and read images within it
    for dir_name in dirs:
        print("dir_name =================+> ", dir_name)    
        #our subject directories start with letter 's' so
        #ignore any non-relevant directories if any
        if not dir_name.startswith("s"):
            continue;
            
        label = int(dir_name.replace("s", ""))
        print("label ============> ", label)
        subject_dir_path = data_folder_path + "/" + dir_name
        
        #get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            
            if image_name.startswith("."):
                continue;
            
            image_path = subject_dir_path + "/" + image_name

            #read image

            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            #display an image window to show the image 
            cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
            cv2.waitKey(100)
            
            #detect face
            face, rect = detect_face(image)
            # print("Face extracted =====?> ", image_path, "face =+> ", face, "LAbel ================> ", label)
            if face is not None:
                faces.append(face)
                labels.append(label)
            else: 
                unRecognisedDataset.append(dir_name)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    return faces, labels
print("Preparing data...")
faces, labels = prepare_training_data("./aligned_faces")
print("Data prepared")
# print("faces ==============> ", faces)

#print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))

face_recognizer = cv2.face.LBPHFaceRecognizer_create()

face_recognizer.train(faces, np.array(labels))



def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


def predict(test_img):
    if test_img is not None:
    #make a copy of the image as we don't want to chang original image
        # img = test_img.copy()
    #detect face from the image
        face, rect = detect_face(test_img)
        print("face, rect ========>", face, rect)
        if face is not None:
        #predict the image using our face recognizer 
            label, confidence = face_recognizer.predict(face)
            print("label, confidence ========>", label, confidence)
            #get name of respective label returned by face recognizer

            # label_text = subjects[label]
            label_text = nameArrOfSubjects[label]
            print("label of predicted image =======> ", label_text , confidence)    
            #draw a rectangle around face detected
            draw_rectangle(test_img, rect)
            #draw name of predicted person
            draw_text(test_img, label_text, rect[0], rect[1]-5)
            
            return test_img
        else:
            return None


print("Predicting images...")

testImages = os.listdir('/var/www/html/face-detection/ai-recognition/cv2/finalFolder')

for image in testImages:
    print("images ", "./finalFolder/"+image)
    #load test images
    test_img1 = cv2.imread("./finalFolder/"+image)
    test_img1 = cv2.cvtColor(test_img1, cv2.COLOR_BGR2RGB)

    # test_img1 = cv2.imread("./pT1.jpeg")
    # test_img2 = cv2.imread("./pr_ishita.jpeg")
    # test_img2 = cv2.imread("./ishita_test_2.jpeg")
    # # test_img2 = cv2.imread("./ishita1.jpeg")
    # test_img3 = cv2.imread("./papa_test_1.jpeg")
    # test_img3 = cv2.imread("./papa2.jpeg")
    # print("test image path ======>", test_img1)
    #perform a prediction
    predicted_img1 = predict(test_img1)
    # predicted_img2 = predict(test_img2)
    # predicted_img3 = predict(test_img3)
    # cv2.imshow("subjects[1]", cv2.resize(test_img1, (400, 500)))
    print("Prediction complete", predicted_img1)
    if predicted_img1 is not None:
    #display both images
        cv2.imshow(image, cv2.resize(predicted_img1, (400, 500)))
        cv2.waitKey(500)
    else:
        unRecognisedTestDataset.append("./finalFolder/"+image)
        # cv2.destroyAllWindows()
# cv2.imshow(subjects[2], cv2.resize(predicted_img2, (400, 500)))
# cv2.imshow(subjects[3], cv2.resize(predicted_img3, (400, 500)))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.waitKey(1)
# cv2.destroyAllWindows()

# mylist = 
print("unRecognisedDataset ====> ",list(dict.fromkeys(unRecognisedDataset)),  len(list(dict.fromkeys(unRecognisedDataset))))
print("unRecognisedTestDataset =====+> ", unRecognisedTestDataset, len(unRecognisedTestDataset))