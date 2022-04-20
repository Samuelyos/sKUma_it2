from PyQt6 import QtWidgets, uic
from lecture_class import lecture
import mysql.connector

mydb = mysql.connector.connect(
    host="mysql-db.caprover.diplomportal.dk",
    user="s206026",
    password="oViFSGqnHflEFAA0ETNw1",
    database="s206026")
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM admincheck")
sqladmin = mycursor.fetchall()


class AdminRequestGUI(QtWidgets.QMainWindow):
    """Klasse for selve ændring af lektioner GUI"""

    def __init__(self):  #
        super(AdminRequestGUI, self).__init__()
        uic.loadUi('GUI/Admin_functionalGUI.ui', self)

        # Her defineres mange af de variable der bliver brugt senere i koden
        self.donePushButton.clicked.connect(self.done_push_button_pressed)
        self.acceptPush.clicked.connect(self.accept_button_pressed)
        self.denyPush.clicked.connect(self.deny_button_pressed)
        self.viewPush.clicked.connect(self.view_button_pressed)
        self.clearPush.clicked.connect(self.clear_button_pressed)
        self.show()
        self.chosenLecture = None
        self.reqlist = []
        self.newreqlist = []
        self.leclist = []
        self.newleclist = []
        self.lecIndex = 0

        # Loop der tager alle rækker i databasen over lektioner, og putter dem ind på en liste
        for lec in range(len(sqladmin)):
            self.leclist.append(
                lecture(sqladmin[lec][0], sqladmin[lec][1], sqladmin[lec][2], sqladmin[lec][3], sqladmin[lec][4],
                        sqladmin[lec][5]))
            self.reqlist.append(sqladmin[lec][7])

        # Giver de requestede lektioner en midlertidig attribut fra databasens reqID
        for lec in range(len(self.leclist)):
            self.leclist[lec].reqid = self.reqlist[lec]

        # Loop der laver en liste over alle requests fra admincheck databasen, og giver dem et midliertidigt requestID
        lecNum = 0
        for lect in self.leclist:
            self.comboLect.addItem(f'{lect.reqid}: {lect.get_course()}, {lect.get_courseID()}')
            lecNum += 1

    def view_button_pressed(self):
        """Viser den originale lektion på en måde der kan sammenlignes med den nye"""

        mycursor.execute("SELECT * FROM lectures")
        sqllec = mycursor.fetchall()
        originalList = []

        # Loop der skaber instances ud databasen over de originale lektioner
        for i in range(len(sqllec)):
            originalList.append(
                lecture(sqllec[i][0], sqllec[i][1], sqllec[i][2], sqllec[i][3], sqllec[i][4], sqllec[i][5]))

        # LecIndex is the index of the lecture request of the chosen lecture
        chosenRequest = self.comboLect.currentText()
        self.lecIndex = int(chosenRequest[0:3])

        # Loop der matcher reqID tekst fra GUI med  reqID fra databasen
        for i in range(len(self.leclist)):
            if self.lecIndex == self.leclist[i].reqid:
                self.chosenLecture = self.leclist[i]

        # Loop der sørger for at finde den originale lektion from, ud fra kursusID
        chosenOriginal = None
        for lecs in originalList:
            if lecs.get_courseID() == self.chosenLecture.get_courseID():
                chosenOriginal = lecs

        # Følgende kode opdatere labels i GUI
        self.labName_2.setText(f'{self.chosenLecture.get_course()}')
        self.labRoom_2.setText(f'{self.chosenLecture.get_room()}')
        self.labDate_2.setText(f'{self.chosenLecture.get_date()}')
        self.labFrom_2.setText(f'{self.chosenLecture.get_time_from()}')
        self.labUntil_2.setText(f'{self.chosenLecture.get_time_until()}')
        self.labName.setText(f'{self.chosenLecture.reqid}')
        self.labRoom.setText(f'{chosenOriginal.get_room()}')
        self.labDate.setText(f'{chosenOriginal.get_date()}')
        self.labFrom.setText(f'{chosenOriginal.get_time_from()}')
        self.labUntil.setText(f'{chosenOriginal.get_time_until()}')

    def clear_button_pressed(self):
        """Fjerner irrelevant info fra labels når man vil"""
        self.labName_2.clear()
        self.labRoom_2.clear()
        self.labDate_2.clear()
        self.labFrom_2.clear()
        self.labUntil_2.clear()
        self.labName.clear()
        self.labRoom.clear()
        self.labDate.clear()
        self.labFrom.clear()
        self.labUntil.clear()

    def clearlabels(self):
        """Fjerner irrelevant info fra labels efter SQL er opdateret"""
        # Tjekker om kryds-af boksen er fyldt eller ej
        if str(self.checkBox.checkState()) == 'CheckState.Checked':
            self.clear_button_pressed()
        else:
            pass

    def deny_button_pressed(self):
        """Deny knappen sletter den valgte lektion fra admincheck databasen, og opdaterer rullemenuen"""

        if self.labName_2.text() == '':
            print('Please choose a lecture to view')
        else:
            # Denne kode sletter lektionen fra admincheck databasen, ved at bruge reqID
            mycursor.execute(f"DELETE FROM admincheck WHERE reqID={self.chosenLecture.reqid};")
            mydb.commit()

            # Giver out-put i terminalen om det lykkedes eller ej med at slette
            if mycursor.rowcount != 0:
                print(mycursor.rowcount, "Request(s) Denied, entry is deleted from database")
            else:
                print("Invalid course chosen, something went wrong")

            # Opretter en fornyet liste over lektioner i admincheck efter den nylige sletning
            mycursor.execute("SELECT * FROM admincheck")
            newsqladmin = mycursor.fetchall()

            # Følgende kode og loop laver en opdateret udgave af lektionslisten og requestID listen fra __INIT__
            for nlec in range(len(newsqladmin)):
                self.newleclist.append(
                    lecture(newsqladmin[nlec][0], newsqladmin[nlec][1], newsqladmin[nlec][2], newsqladmin[nlec][3],
                            newsqladmin[nlec][4], newsqladmin[nlec][5]))
                self.newreqlist.append(newsqladmin[nlec][7])

            # Sletter alt indhold på rullelisten, og udskifter med den nye opdaterede liste
            self.comboLect.clear()
            for i in range(len(self.newleclist)):
                self.comboLect.addItem(
                    f'{self.newreqlist[i]}: {self.newleclist[i].get_course()}, {self.newleclist[i].get_courseID()}')

            # Tømmer den nye liste efter GUI integration, for irrelevant data ikke bliver lagret til næste brug af "Deny"
            # Printer i terminalen hvor mange requests der er tilbage i databasen, og sletter derefter listen over
            # info i databasen, ingen for at undgå lagring af irrelevant info.
            print(len(newsqladmin), "requests are left")
            self.newleclist.clear()
            self.newreqlist.clear()
            del newsqladmin
            self.clearlabels()

    def accept_button_pressed(self):
        """Når denne knap trykkes bliver den originale database opdateret med indholdet fra requesten"""

        if self.labName_2.text() == '':
            print('Please choose a lecture to view')
        else:
            # Først identificeres den valgte lektion, ved at tage den date som view viser
            # Info brydes ned til bider som kan sættes ind i databasen
            # Disse bidder gemmes som en midlertidig variabel
            update_courseID = str(self.comboLect.currentText())[-3:]
            update_room = self.labRoom_2.text()
            update_date = self.labDate_2.text()
            update_timeFrom = self.labFrom_2.text()
            update_timeUntil = self.labUntil_2.text()

            # SQL update statement where CourseID = midlertidigvariabel.get_courseID
            update_sql = f"UPDATE lectures SET room = '{update_room}', date = '{update_date}', timefrom = '{update_timeFrom}', timeuntil = '{update_timeUntil}' WHERE courseID = '{update_courseID}'"
            mycursor.execute(update_sql)
            mydb.commit()
            print(mycursor.rowcount, "Request accepted, database is updated")

            # Copy-Paste fra DENY for at slette og opdatere ting i GUI
            # Denne kode sletter lektionen fra admincheck databasen, ved at bruge reqID
            mycursor.execute(f"DELETE FROM admincheck WHERE reqID={self.chosenLecture.reqid};")
            mydb.commit()

            # Opretter en fornyet liste over lektioner i admincheck efter den nylige sletning
            mycursor.execute("SELECT * FROM admincheck")
            newsqladmin = mycursor.fetchall()

            # Følgende kode og loop laver en opdateret udgave af lektionslisten og requestID listen fra __INIT__
            for nlec in range(len(newsqladmin)):
                self.newleclist.append(
                    lecture(newsqladmin[nlec][0], newsqladmin[nlec][1], newsqladmin[nlec][2], newsqladmin[nlec][3],
                            newsqladmin[nlec][4], newsqladmin[nlec][5]))
                self.newreqlist.append(newsqladmin[nlec][7])

            # Sletter alt indhold på rullelisten, og udskifter med den nye opdaterede liste
            self.comboLect.clear()
            for i in range(len(self.newleclist)):
                self.comboLect.addItem(
                    f'{self.newreqlist[i]}: {self.newleclist[i].get_course()}, {self.newleclist[i].get_courseID()}')

            # Tømmer den nye liste efter GUI integration, for irrelevant data ikke bliver lagret til næste brug af "Deny"
            # Printer i terminalen hvor mange requests der er tilbage i databasen, og sletter derefter listen over
            # info i databasen, ingen for at undgå lagring af irrelevant info.
            print(len(newsqladmin), "requests are left")
            self.newleclist.clear()
            self.newreqlist.clear()
            del newsqladmin
            self.clearlabels()

    def done_push_button_pressed(self):
        """Lukker GUI efter brug"""
        self.close()
