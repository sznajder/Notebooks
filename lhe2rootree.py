import sys
import ROOT as r
from array import array
from tqdm import tqdm

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
    t1 = r.TTree("t","t")

    pdgid = array( 'i', [ 0 ] )
    bevent = array( 'i', [ 0 ] )
    status = array( 'i', [ 0 ] )
    parent1 = array( 'i', [ 0 ] )
    parent2 = array( 'i', [ 0 ] )
    color1 = array( 'i', [ 0 ] )
    color2 = array( 'i', [ 0 ] )
    mass = array( 'd', [ 0 ] )
    spin = array( 'd', [ 0 ] )
    p4 = r.TLorentzVector(1,1,0,5)

    t1.Branch("id",pdgid, "id/I")
    t1.Branch("event",bevent, "event/I")
    t1.Branch("status",status, "status/I")
    t1.Branch("parent1",parent1, "parent1/I")
    t1.Branch("parent2",parent2, "parent2/I")
    t1.Branch("color1",color1, "color1/I")
    t1.Branch("color2",color2, "color2/I")
    t1.Branch("mass",mass, "mass/F")
    t1.Branch("spin",spin, "spin/F")
    t1.Branch("p4.","TLorentzVector",p4)

    for ievt,evt in enumerate(events):
        particle_lines = evt.splitlines()[1:]
        for particle_line in particle_lines:
            parts = particle_line.split()
            evt_pdgid = int(parts[0])
            evt_status = int(parts[1])
            evt_parent1 = int(parts[2])
            evt_parent2 = int(parts[3])
            evt_color1 = int(parts[4])
            evt_color2 = int(parts[5])
            evt_px, evt_py, evt_pz, evt_e = map(float,parts[6:10])
            evt_mass = float(parts[10])
            evt_spin = float(parts[11])

            p4.SetPxPyPzE(evt_px, evt_py, evt_pz, evt_e)

            bevent[0] = ievt
            pdgid[0] = evt_pdgid
            status[0] = evt_status
            parent1[0] = evt_parent1
            parent2[0] = evt_parent2
            color1[0] = evt_color1
            color2[0] = evt_color2
            mass[0] = evt_mass
            spin[0] = evt_spin

            t1.Fill()

    t1.Print()
    t1.Write()
    f1.Close()

if __name__ == "__main__":

    convert_lhe(sys.argv[1])

