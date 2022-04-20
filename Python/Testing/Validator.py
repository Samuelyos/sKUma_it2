def validate_couseID(courseID:str):
    """validerer course ID er tal og ikke mere end 3 decimaler"""
    if not courseID.isdigit(): #tjekker om det er tal
        return False #retunerer false hvis det ikke er tal
    if len(courseID)>3: #tjekker at længden ikke er over 3
        return False
    return True # retunere true hvis den er guddi

def validate_course(course:str):
    """validerer længden på course"""
    if len(course)<5: #længen af navnet på kurset er over 5 tegn
        return False
    if len(course)>25: #længden af kurset må ikke være over 25 tegn
        return False
    return True


def validate_room(room:str):
    """validerer om det første er et bokstav og længden er passende"""
    if room[0].isdigit(): #hvis det er et tal, da det skal være et bokstav
        return False
    if len(room)<8: #længen skal være over 8
        return False
    if len(room)>35: #længen må ikke være over 25
        return False
    return True

def validate_date(date:str):
    """validerer dato"""
    if not date[0].isdigit(): #det første skal være et tal
        return False
    return True

def validate_timefrome(timefrome:str):
    """validerer start tidspunkt"""
    if not timefrome.isdigit(): #tjekker om det er et tal
        return False
    if len(timefrome)>4: #tjekker at længden ikke er over 4
        return False
    if not str.strip().split()[2]==":": #tjekker at ":" er på plads 3)
        return False
    return True

def validate_timeuntil(timeuntil:str):
    """validerer slut tidspunkt"""
    if not timeuntil.isdigit(): #tjekker om det er et tal
        return False
    if len(timeuntil)>4: #tjekker at længden ikke er over 4
        return False
    if not str.strip().split()[2]==":": #tjekker at ":" er på plads 3)
        return False
    return True

def validate_zoom(zoom:str):
    """validerer zoom"""
    if not zoom.isdigit =="0" or "1": #tjekker om det er et 0 eller 1 tal
        return False
    if len(zoom)>1: #tjekker at længden ikke er over 1
        return False
    return True








