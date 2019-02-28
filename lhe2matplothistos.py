import sys
from math import sqrt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

######################################################################

class Particle:
    """particle information"""

    def __init__( self, pdgid_, status_, mo1_, mo2_, px_, py_, pz_, e_, mass_ , spin_):
        """start a particle"""

        self.pdgid=pdgid_
        self.status=status_
        self.mo1=mo1_
        self.mo2=mo2_
        self.px=px_
        self.py=py_
        self.pz=pz_
        self.e=e_
        self.mass=mass_
        self.spin=spin_

    def pt(self):
        pt_ = sqrt(self.px**2+self.py**2)
        return  pt_

    def eta(self):
        if self.pz != 0 :
          theta_=atan2(self.pt(),self.pz)
          eta_=-log(tan(theta_/2.))
        else :
          eta_=0.0
        return eta_

    def phi(self):
        if self.px != 0 :
          phi_=atan2(self.py,self.px)
        else:
          phi_=math.pi
        return phi_

    def theta(self):
        if self.pz != 0 :
          theta_=atan2(self.pt(),self.pz)
        else :
          theta_=math.pi
        return theta_

    def theta2(self):
        return 2.*atan( exp( -self.eta() ) )

###############################################################################

def process_event(event_str):
        event = []
# Loop over event string to extract particles information
        particle_lines = event_str.splitlines()[1:]
        for particle_line in particle_lines:
            parts = particle_line.split()
            pdgid = int(parts[0])
            status = int(parts[1])
            parent1 = int(parts[2])
            parent2 = int(parts[3])
            color1 = int(parts[4])
            color2 = int(parts[5])
            px, py, pz, e = map(float,parts[6:10])
            mass = float(parts[10])
            spin = float(parts[11])

            particle = Particle(pdgid,
                        status,
                        parent1,
                        parent2,
                        px,
                        py,
                        pz,
                        e,
                        mass,
                        spin)

            event.append(particle)
        return event

###############################################################################

# Function LHE reader
def read_lhe(fname):
    events = []
    event_str = ""
    in_event = False
    with open(fname, "r") as file:
# Loop over LHE lines
        for line in file:
# If end of event process event anf fill histos
            if in_event and line.startswith("<"):
                in_event = False
                event = process_event(event_str)
                events.append(event)
                event_str = ""
# Add line to event string
            if in_event:
                event_str += line
# If begining of new event
            if line.startswith("<event>"):
                in_event = True
# Return events collection
    return events
##############################################################################

# Event analysis
def analysis(events):

# Loop over events
   mass=[]
   ptl =[]
   for event in events:

# Loop over event particles
       leps=[]
       jets=[]
       for particle in event:
           pid = particle.pdgid
           status = particle.status

# Select leptons
           if ( abs(pid)==13 or abs(pid)==11 ) and status==1 :
              leps.append(particle)
              ptl.append(particle.pt())
# Select jets
           if ( 0<abs(pid)<7 ) and status==1  :
              jets.append(particle)

# Four leptons mass
       if ( len(leps)!=2 ):
          print "Event with ",len(leps)," leptons ! Skipping ..."
          continue

       m = ( leps[0].e  + leps[1].e  )**2 \
          -( leps[0].px + leps[1].px )**2 \
          -( leps[0].py + leps[1].py )**2 \
          -( leps[0].pz + leps[1].pz )**2
       m = sqrt(m)
       mass.append(m)

# Plot and saves hitos 

   plt.hist(mass,bins=50,range=[20.,100.])
   plt.title('Dilepton Mass', fontsize=20)
   plt.xlabel(r'$mass [GeV]$', fontsize=20)
   plt.ylabel('events', fontsize=20)
   plt.savefig('dilepton_mass.png',format='png')
   plt.close()

   plt.hist(ptl,bins=50,range=[20.,100.])
   plt.title('Lepton Pt', fontsize=20)
   plt.xlabel(r'$Pt [GeV]$', fontsize=20)
   plt.ylabel('events', fontsize=20)
   plt.savefig('lepton_pt.png',format='png')
   plt.close()

   return
##################################################
#
#  Main
#
##################################################
if __name__ == "__main__":

    fname = sys.argv[1]
    print("Processing LHE file:",fname)
    events=read_lhe(fname)
    analysis(events)
