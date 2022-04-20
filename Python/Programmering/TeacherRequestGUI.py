from PyQt6 import QtWidgets, uic
from lecture_class import lecture
import mysql.connector

mydb = mysql.connector.connect(
    host="mysql-db.caprover.diplomportal.dk",
    user="s206026",
    password="oViFSGqnHflEFAA0ETNw1",
    database="s206026")
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM lectures")
sqllec = mycursor.fetchall()

# Loop der tager alle rækker i databasen over lektioner, og putter dem ind på en liste
leclist = []
for lec in range(len(sqllec)):
    leclist.append(lecture(sqllec[lec][0], sqllec[lec][1], sqllec[lec][2], sqllec[lec][3], sqllec[lec][4], sqllec[lec][5]))


class TeacherRequestGUI(QtWidgets.QDialog):
    """Klasse for selve ændring af lektioner GUI"""

    def __init__(self):  #
        super(TeacherRequestGUI, self).__init__()
        uic.loadUi('GUI/Underviser_functionalGUI.ui', self)

# Forbinder knapperne med funktioner i python
        self.buttonBox.clicked.connect(self.ok_button_pressed)
        self.pushButton.clicked.connect(self.push_button_pressed)
        self.addPush.clicked.connect(self.addPush_pressed)

# Kort loop der tilføjer et item i dropdown menuen, for hvert item i listen over lektioner
        for i in range(len(leclist)):
            self.comboBox.addItem(leclist[i].get_course())
        self.show()

    def push_button_pressed(self):

        # Når knappen "import" bliver trykket på, kaldes følgende linjer. Teksten i felterne bliver udskiftet med en lektion
        chosenLect = self.comboBox.currentText()

        # chosenLect er en midlertidig variabel, der statisk opdaterer variablen oldLecture, afhængigt af hvad du vælger i
        # dropdown-menuen ved siden af import
        oldLecture = None
        for i in range(len(leclist)):
            if chosenLect == leclist[i].get_course():
                oldLecture = leclist[i]

        # Når man trykker på import bliver diverse labels udfyldt automatisk
        self.roomLabelOld.setText(f'{oldLecture.get_room()}')
        self.label.setText(f'{oldLecture.get_course()}')
        self.courseID_label.setText(f'{oldLecture.get_courseID()}')
        self.timeLabelS.setText(f'{oldLecture.get_time_from()}, {oldLecture.get_date()}')
        self.timeLabelE.setText(f'{oldLecture.get_time_until()}')
        self.roomLineEdit.setText(f'{oldLecture.get_room()}')

    def ok_button_pressed(self):
        """Ok knappen som lukker selve GUI"""
        self.close()

    def addPush_pressed(self):
        """ Læser ændringerne fortaget i GUI, og opdatere admincheck i databasen med ændringerne efter OK"""

        # Læser indhold på labels og gemmer dem som variable
        course = self.label.text()
        courseID = self.courseID_label.text()
        dateGUI = self.calender.selectedDate().toString('yyyy-MM-dd')
        GUItimeStart = self.S2TimeEdit.dateTime().toString('hh:mm')
        GUItimeEnd = self.E2TimeEdit.time().toString('hh:mm')
        room = self.roomLineEdit.text()

        # Hvis der ikke er nogle lektion, returneres dette i terminalen
        if course == "No Lecture imported":
            print('No Lecture was imported, please import and try again')

        # Hvis der er en lektion importeret, bliver denne tilføjet til admincheck tabellen i databasen
        else:
            ins_sql = f"INSERT INTO admincheck (courseID, course, room, `date`, timefrom, timeuntil) VALUES ('{courseID}','{course}', '{room}', '{dateGUI}',\
                    '{GUItimeStart}', '{GUItimeEnd}')"
            mycursor.execute(ins_sql)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
