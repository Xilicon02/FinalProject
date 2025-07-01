## Detector Setting
from models.detector import DetectorModule
import models.detector as de


detectors = []

# input: size, position(x, y, z)

# ===== D1 ======

#detectors.append(de.DetectorModule(25, (0, 0, 0)))
detectors += de.Set_Detector_Module(25, 50, 50, 5)      # Layer 1, z=5
detectors += de.Set_Detector_Module(25, 100, 100, 10)   # Layer 2, z=10
detectors += de.Set_Detector_Module(50, 150, 150, 15)   # Layer 3, z=15
detectors += de.Set_Detector_Module(100, 200, 200, 20)  # Layer 4, z=20

#Mean RMSE: 15.201119388991058
#Median RMSE: 15.69443774401663
#Standard Deviation of RMSE: 6.190533917124837


# ===== D2 ======
#detectors += de.Set_Detector_Module(50, 50, 5, 25)
#detectors += de.Set_Detector_Module(75, 75, 10, 25)