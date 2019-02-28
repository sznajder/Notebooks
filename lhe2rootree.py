import sys
import ROOT as r
from array import array

def convert_lhe(fname_in, fname_out="events.root"):

    events = []
    event = ""
    in_event = False
    with open(fname_in, "r") as fhin:
        iline = 0
        for line in fhin:

            if in_event and line.startswith("<"):
                in_event = False
                events.append(event)
                event = ""

            if in_event:
                event += line

            if line.startswith("<event>"):
                in_event = True

        if event:
            events.append(event)

    f1 = r.TFile(fname_out, "recreate")
    t1 = r.TTree("events","events")

    bevent  = array( 'i', [ 0 ] )
    pdgid   = array( 'i', [ 0 ] )
    status  = array( 'i', [ 0 ] )
    parent1 = array( 'i', [ 0 ] )
    parent2 = array( 'i', [ 0 ] )
    color1  = array( 'i', [ 0 ] )
    color2  = array( 'i', [ 0 ] )
    mass    = array( 'd', [ 0 ] )
    spin    = array( 'd', [ 0 ] )
    p4      = r.TLorentzVector(0,0,0,0)

    t1.Branch("ievt",bevent, "ievt/I")
    t1.Branch("id",pdgid, "id/I")
    t1.Branch("status",status, "status/I")
    t1.Branch("parent1",parent1, "parent1/I")
    t1.Branch("parent2",parent2, "parent2/I")
    t1.Branch("color1",color1, "color1/I")
    t1.Branch("color2",color2, "color2/I")
    t1.Branch("mass",mass, "mass/F")
    t1.Branch("spin",spin, "spin/F")
    t1.Branch("p4","TLorentzVector",p4)

    for ievt,evt in enumerate(events):
        particle_lines = evt.splitlines()[1:]
        for particle_line in particle_lines:
            parts = particle_line.split()
            bevent[0] = ievt
            pdgid[0] = int(parts[0])
            status[0] = int(parts[1])
            parent1[0] = int(parts[2])
            parent2[0] = int(parts[3])
            color1[0] = int(parts[4])
            color2[0] = int(parts[5])
            px, py, pz, e = map(float,parts[6:10])
            p4.SetPxPyPzE(px,py,pz,e)
            mass[0] = float(parts[10])
            spin[0] = float(parts[11])

            t1.Fill()

    t1.Print()
    t1.Write()
    f1.Close()

if __name__ == "__main__":

    convert_lhe(sys.argv[1])
