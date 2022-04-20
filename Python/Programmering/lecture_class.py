
class lecture:
    """Klasse for hvert enkelt lektion, indeholder alt information relevant til booking"""
    def __init__(self, courseID, course, room, date, time_from, time_until, zoom: bool = False):
        self.__courseID = courseID
        self.__course = course
        self.__room = room
        self.__date = date
        self.__time_from = time_from
        self.__time_until = time_until
        self.__zoom = zoom

        assert course != "No Lecture imported"

    #Følgende metoder er getters og setters som kan ændre og kalde på objekter (lektioners) attributter

    def get_courseID(self): return self.__courseID

    def set_courseID(self, new_courseID): self.__courseID = new_courseID

    def get_course(self): return self.__course

    def get_room(self): return self.__room

    def set_room(self, new_room): self.__room = new_room

    def get_date(self): return self.__date

    def set_date(self, new_date): self.__date = new_date

    def get_time_from(self): return self.__time_from

    def set_time_from(self, new_time_from): self.__time_from = new_time_from

    def get_time_until(self): return self.__time_until

    def set_time_until(self, new_time_until): self.__time_until = new_time_until

    # Hvordan vores objekter bliver repræsenteret som string.
    def __str__(self):
        return f"Course: {self.__course}\nat {self.__room} on {self.__date}\nfrom {self.__time_from} until" \
               f" {self.__time_until}"
