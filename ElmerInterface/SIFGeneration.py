
import sys
def getMaterial(name,number=1):
    m=''
    if name == 'steel':    
        m="""
Material %i
    Name = "Steel (carbon - generic)"
    Heat Conductivity = 44.8
    Youngs modulus = 200.0e9
    Mesh Poisson ratio = 0.285
    Heat Capacity = 1265.0
    Density = 7850.0
    Poisson ratio = 0.285
    Sound speed = 5100.0
    Heat expansion Coefficient = 13.8e-6
End
        """%number
    elif name == 'aluminium':
        m="""
Material %i
    Name = "Aluminium (generic)"
    Heat Conductivity = 237.0
    Youngs modulus = 70.0e9
    Mesh Poisson ratio = 0.35
    Heat Capacity = 897.0
    Density = 2700.0
    Poisson ratio = 0.35
    Sound speed = 5000.0
    Heat expansion Coefficient = 23.1e-6
End
          """%number
    elif name == 'polycarbonate':
        m='''
Material %i
    Name = "Polycarbonate (generic)"
    Heat Conductivity = 0.205
    Youngs modulus = 2.2e9
    Mesh Poisson ratio = 0.37
    Heat Capacity = 1250.0
    Density = 1220.0
    Poisson ratio = 0.37
    Heat expansion Coefficient = 67.0e-6
End
        '''%number
    elif name == 'pvc':
        m='''
Material %i
    Name = "Polyvinyl chloride (generic)"
    Heat Conductivity = 0.16
    Youngs modulus = 3100.0e6
    Mesh Poisson ratio = 0.41
    Heat Capacity = 900.0
    Density = 1380.0
    Poisson ratio = 0.41
    Heat expansion Coefficient = 80.0e-6
End
          '''%number
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