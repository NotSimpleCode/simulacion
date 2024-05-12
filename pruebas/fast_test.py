
import pruebas.management.average_manage as AM
import pruebas.management.variance_manage as VM
import pruebas.management.chi_manage as CM
import pruebas.management.ks_manage as KM
import pruebas.management.poker_manage as PM


passed_data = []


def doTests(ri):

    global passed_data

    passed_data.clear()

    AM.fastTest(ri)
    
    VM.fastTest(AM.getPassedData())
    
    CM.fastTest(VM.getPassedData())
    
    KM.fastTest(CM.getPassedData())

    PM.fastTest(KM.getPassedData())

    passed_data = PM.getPassedData()


def getPassedData():
    return passed_data