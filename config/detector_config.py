## Detector Setting
import models.detector as de


detectors = []

# input: size, position(x, y, z)

# ===== D1 ======

detectors.append(de.DetectorModule(25, (0, 0, 0)))
detectors += de.Set_Detector_Module(25, 12.5, 12.5, 15)
detectors += de.Set_Detector_Module(25, 37.5, 37.5, 25)    
detectors += de.Set_Detector_Module(25, 50, 50, 35)
detectors += de.Set_Detector_Module(25, 75, 75, 50)
detectors += de.Set_Detector_Module(50, 100, 100, 70)
detectors += de.Set_Detector_Module(50, 150, 150, 100)


# ===== D2 ===== For decay
#detectors.append(de.DetectorModule(25, (0, 0, 0)))
#detectors += de.Set_Detector_Module(100, 100, 100, 10)
#detectors += de.Set_Detector_Module(25, 50, 50, 15)
#detectors += de.Set_Detector_Module(25, 50, 50, 20)
#detectors += de.Set_Detector_Module(25, 50, 50, 25)    
#detectors += de.Set_Detector_Module(50, 50, 50, 35)
#detectors += de.Set_Detector_Module(25, 75, 75, 50)
#detectors += de.Set_Detector_Module(50, 100, 100, 70)
#detectors += de.Set_Detector_Module(100, 200, 200, 100)

