
import boto3
import datetime
import sys
import re


def extract_text(photo,bucket):

    try:
        client = boto3.client('rekognition')

        response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

        textDetections = response['TextDetections']


    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)
        return (e,2)


    wordDetections=[]
    for detectedWordInfo in textDetections:
        if(detectedWordInfo[ "Type"]=="WORD"):
            wordDetections.append(detectedWordInfo)

    string=""
    for detectedWordInfo in wordDetections:
        detectedWord=detectedWordInfo["DetectedText"]
        if(detectedWordInfo["Confidence"]>97):
            string=string + detectedWord + " "

    return (string,1)


def compare_text(text_control, photo_test, bucket):

    text_test=extract_text(photo_test,bucket)
    print("Texto detectado:")
    print(text_test)

    if(text_test[1] !=1):
        return text_test[0]
    text_control = text_control[0]
    text_test = text_test[0]
    text_control=text_control.replace(" ","").lower()
    text_test=text_test.replace(" ","").lower()
    text_control = re.sub("[@/$%-_+\*#'\"]", "", text_control)
    text_test = re.sub("[@/$%-_+\*#'\"]", "", text_test)

    if(text_control in text_test):
        return True
    else:
        return False



def main():
    bucket = str(input("Nombre bucket:"))
    photo_control = str(input("Nombre imagen de control:"))
    text_control = extract_text(photo_control, bucket)
    log_file = open("log.txt", "a")
    if (text_control[1] != 1):
        print("imagen de control invalida")
        now = datetime.datetime.now()
        tiempo = now.strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(tiempo + "\t" + photo_control + "\t" + "Imagen de control invalida\n")
        log_file.close()

        return -1
    print("Texto detectado Imagen de control:")
    print(text_control[0])

    photo_test=str(input("ingrese ruta a imagen de prueba:"))

    while(photo_test !="0"):

        result = compare_text(text_control, photo_test, bucket)
        print(result)

        now = datetime.datetime.now()
        tiempo=now.strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(tiempo+"\t" + photo_control +"\t"+photo_test +"\t"+ str(result) +"\n")
        photo_test = str(input("ingrese ruta a imagen de prueba:"))

    log_file.close()
    return 0



if __name__ == "__main__":
    main()