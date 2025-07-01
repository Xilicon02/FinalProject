## Detector Setting
from models.detector import DetectorModule
import models.detector as de


detectors = []

detectors += de.Set_Detector_Module(50, 50, 10, 25)      # Layer 1, z=10
detectors += de.Set_Detector_Module(100, 100, 20, 25)   # Layer 2, z=20
detectors += de.Set_Detector_Module(150, 150, 30, 50)   # Layer 3, z=30
#detectors += de.Set_Detector_Module(200, 200, 20, 50)   # Layer 4, z=20
detectors += de.Set_Detector_Module(200, 200, 40, 100)  # Layer 5, z=40
#detectors += de.Set_Detector_Module(400, 400, 30, 100)  # Layer 6, z=40

#detectors += de.Set_Detector_Module(50, 50, 5, 25)      # Layer 1, z=5
#detectors += de.Set_Detector_Module(100, 100, 10, 25)   # Layer 2, z=10
#detectors += de.Set_Detector_Module(150, 150, 15, 50)   # Layer 3, z=15
##detectors += de.Set_Detector_Module(200, 200, 20, 50)   # Layer 4, z=20
#detectors += de.Set_Detector_Module(200, 200, 20, 100)  # Layer 5, z=30
##detectors += de.Set_Detector_Module(400, 400, 30, 100)  # Layer 6, z=40