# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
import geni.rspec.igext as IG

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


tourDescription = \
"""
This profile provides a full research cluster with head node, scheduler, compute nodes, and shared file systems.

First node (head): 
- Shared home directory
- Shared software directory (/software)
- Management server for BeeGFS
- Management server for SLURM

Second node (metadata):
- Metadata server for BeeGFS
- Metadata server for SLURM

Third node (storage):
- Storage server

Remaining three nodes (computing):
- Compute nodes  
"""

#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)


link = request.LAN("lan")

for i in range(6):
  if i == 0:
    node = request.XenVM("head")
    node.routable_control_ip = "true"
  elif i == 1:
    node = request.XenVM("metadata")
  elif i == 2:
    node = request.XenVM("storage")
  else:
    node = request.XenVM("compute-" + str(i))
    node.cores = 2
    node.ram = 4096
    
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"
  
  iface = node.addInterface("if" + str(i-3))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address("192.168.1." + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)
  
  node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/passwordless.sh"))

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
