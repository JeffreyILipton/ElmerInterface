import xml.etree.ElementTree as ET

import sys


def getMaterial(name,number=1):
    tree = ET.parse('MaterialDB.xml')
    root = tree.getroot()
    matEl = root.find(".//material[@name='%s']"%name)
    if matEl is None or len(matEl)<0 : return ''
    props = ["Heat_Conductivity","Heat_Capacity","Head_Expansion_Coefficent","Youngs_modulus","Poisson_ratio","Density","Sound_Speed" ]
    vals = []
    for prop in props:
        propEl = matEl.find(prop)
        if propEl is None:
            vals.append('')
        else:
            vals.append(propEl.text)
            if (prop == "Poisson_ratio"): vals.append(propEl.text)
    #vals.insert(0,name)
    #vals.insert(0,number)
    m='''
Material %i
    Name = "%s"
    Heat Conductivity = %s
    Heat Capacity = %s
    Heat expansion Coefficient = %s
    Youngs modulus = %s
    Mesh Poisson ratio = %s
    Poisson ratio = %s
    Density = %s
    Sound speed = %s
End
       '''%(number,name,vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7])
    return m   
    
    

def BoundaryCondition_Static(n,b=2):
    s="""
Boundary Condition %i
    Target Boundaries(1) = %i 
    Name = "fixed"
    Displacement 3 = 0
    Displacement 2 = 0
    Displacement 1 = 0
End
    """%(n,b)
    return s

def BoundaryCondition_Load(force,n,b=3):
    s="""
Boundary Condition %i
    Target Boundaries(1) = %i 
    Name = "pressure(called_force)"
    Force 2 = %0.0f
End
    """%(n,b,force)
    return s

def Solver_Linear_Elastic(n):
    s="""
Solver %i
    Equation = Linear elasticity
    Procedure = "StressSolve" "StressSolver"
    Variable = -dofs 3 Displacement
    Exec Solver = Always
    Stabilize = True
    Bubbles = False
    Lumped Mass Matrix = False
    Optimize Bandwidth = True
    Steady State Convergence Tolerance = 1.0e-5
    Nonlinear System Convergence Tolerance = 1.0e-7
    Nonlinear System Max Iterations = 20
    Nonlinear System Newton After Iterations = 3
    Nonlinear System Newton After Tolerance = 1.0e-3
    Nonlinear System Relaxation Factor = 1
    Linear System Solver = Iterative
    Linear System Iterative Method = BiCGStab
    Linear System Max Iterations = 500
    Linear System Convergence Tolerance = 1.0e-10
    BiCGstabl polynomial degree = 2
    Linear System Preconditioning = Diagonal
    Linear System ILUT Tolerance = 1.0e-3
    Linear System Abort Not Converged = False
    Linear System Residual Output = 1
    Linear System Precondition Recompute = 1
End
    """%n
    return s

def Solver_save_scalars(n,m):
    s="""
Solver %i
    Exec Solver = after timestep
    Equation = String SaveScalars
    Procedure = File "SaveData" "SaveScalars"
    Filename = File "f.dat"
    Variable 1 = String Displacement
    Operator 1 = String max
    Variable 2 = String Stress_xx
    Operator 2 = String max
    Variable 3 = String Stress_yy
    Operator 3 = String max
    Variable 4 = String Stress_zz
    Operator 4 = String max
    Variable 5 = String Stress_xy
    Operator 5 = String max
    Variable 6 = String Stress_yz
    Operator 6 = String max
    Variable 7 = String Stress_xz
    Operator 7 = String max
End

Boundary Condition %i
    Save Scalars = Logical True
End  
    """%(n,m)
    return s


def makeSIFfile(material,force):
    header = """ 
Header
    CHECK KEYWORDS Warn
    Mesh DB "." "out.mesh"
    Include Path "."
    Results Directory "."
End
    """

    simulation="""
Simulation
    Max Output Level = 5
    Coordinate System = Cartesian
    Coordinate Mapping(3) = 1 2 3
    Simulation Type = Steady state
    Steady State Max Iterations = 1
    Output Intervals = 1
    Timestepping Method = BDF
    BDF Order = 1
    Solver Input File = case.sif
    Post File = case.ep
End
    """

    constants="""
Constants
    Gravity(4) = 0 -1 0 9.82
    Stefan Boltzmann = 5.67e-08
    Permittivity of Vacuum = 8.8542e-12
    Boltzmann Constant = 1.3807e-23
    Unit Charge = 1.602e-19
End
    """

    body1="""
Body 1
    Target Bodies(1) = 1
    Name = "Body 1"
    Equation = 1
    Material = 1
End
    """

    
    
    
    equation="""
Equation 1
    Name = "Equation 1"
    Calculate Stresses = True
    Active Solvers(1) = 1
End
    """
    material1 = getMaterial(material,1)
    solver1 = Solver_Linear_Elastic(1)
    force_condition   = BoundaryCondition_Load(force,1,2)
    static_condition  = BoundaryCondition_Static(2,3)
    output  = Solver_save_scalars(2,3)

    filestring = header+simulation+constants+body1+material1+equation+solver1+force_condition+static_condition+output
    with open('case.sif', 'w') as f:
        f.write(filestring)
    f.close()

def main():
    makeSIFfile('steel',50000)

if __name__ == "__main__":
    sys.exit(int(main() or 0))