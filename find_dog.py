import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests
import json


def sendEmail(dogname):

    '''
    (str)->NoneType
    Send an email to inform myself that the dog that I am waiting for is now
    available on the website
    '''

    sender = '****@*****.com'
    receivers = ['****@*****.com', 'aaaa@****.com']
    password = '*********'
    subject = 'Found DOG!'

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (sender, ", ".join(receivers), subject, (
            dogname + ' is available!!!'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receivers, message)
        server.close()
        print "Email sent successfully !"
    except smtplib.SMTPException, e:
        print "Error: can't send it, below is the Exception: " + str(e)


def requestPage(url):

    '''
    Make request to endpoint to get repoonse
    returns a list of dictionaries of dog information
    '''

    response = requests.get(url)
    data = response.json()
    return data.get('AdoptableSearchResult').get('XmlNode')


def findDog(dogs, keys):

    '''
    check if any of the dog's name in keys shows up on the website
    '''

    for dog in dogs:
        if (dog is not None) and (getName(dog) in keys):
            print "found it"
            sendEmail(getName(dog))


def getName(dog):

    '''
    get a dog's name
    '''

    return dog.get('adoptableSearch').get('Name')


if __name__ == "__main__":

    while True:
        dogs = requestPage(
            'https://www.torontohumanesociety.com/'
            'api/api.php?action=getAnimalsForSpeciesId&id=1&stageId=2')
        findDog(dogs, ['Alfreda', 'Ashley', 'Twinkle'])
        time.sleep(300)
