# run with 
## chimera --nogui olfr1392_1u19_noH.pdb writedms.py
## chimera --nogui pdb:3D7F_withoutLigand writedms.py 
# chimera --nogui Q9I8C1_27_noH.pdb writedms.py 
# where this py file is named writedms.py
# it would run chimera without gui on the file 3D7F_withoutLigand.pdb  
# and it would output to a file called 3D7F_without_ligand.dms

from chimera import runCommand, openModels, MSMSModel
# generate surface using 'surf' command
runCommand("surf")
# get the surf object
surf = openModels.list(modelTypes=[MSMSModel])[0]
# write DMS
from WriteDMS import writeDMS
#writeDMS(surf, "3D7F_rec_noH.dms")
#writeDMS(surf, "olfr1392_1u19_noH.dms")
#writeDMS(surf, "Q9I8C1_27_aligned_noH.dms")
writeDMS(surf, "rec.dms")

