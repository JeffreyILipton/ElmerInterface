import subprocess
from SIFGeneration import *
import os
import sys


def setupEnviroment():
    my_env = os.environ
    my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]

def processSTLToMesh(stlfile):
    parts = stlfile.split(".")
    parts[-1].lower()
    filename = ".".join(parts)
    cmd = 'netgen.exe -geofile=%s -fine -batchmode -meshfiletype="Elmer Format"'%filename

    output = subprocess.check_output(cmd)
    if "DONE!" in output:
        return True
    return False

def makeStartInfo():
    filename ="ELMERSOLVER_STARTINFO"
    contents = "case.sif\n1"
    with open(filename,'w') as f:
        f.write(contents)
    f.close()

def RunSolver():
    cmd = "ElmerSolver"
    output = subprocess.check_output([cmd])
    if "ELMER SOLVER FINISHED" in output:
        return True
    return False

def readDataFile():
    fileContent=""
    with open("f.dat") as f:
        fileContent=f.read()
    f.close()
    content = fileContent.rstrip()
    parts = content.split('   ')
    parts.pop(0)
    print parts
    return parts
    

def processGeometrey(stlfile,material,force):
    makeSIFfile(material,force)
    makeStartInfo()
    good = True
    good = good and processSTLToMesh(stlfile)
    if good:
        good = RunSolver()
    if good:
        readDataFile()
        return True
    else:
        return False

def main():
    os.chdir('C:\Users\jil26\Documents\GitHub\MIT\ElmerInterface\Media\TestPython')
    processGeometrey("Part2.stl",'steel',50000)

if __name__ == "__main__":
    sys.exit(int(main() or 0))