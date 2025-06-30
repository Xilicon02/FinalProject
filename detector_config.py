## Detector Setting
from detector import DetectorModule
import detector as de


detectors = []

detectors += de.Set_Detector_Module(25, 25, 0, 25)
detectors += de.Set_Detector_Module(50, 50, 25, 25)
detectors += de.Set_Detector_Module(100, 100, 75, 50)
detectors += de.Set_Detector_Module(100, 100, 100, 100)