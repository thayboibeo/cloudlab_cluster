# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
import geni.rspec.igext as IG

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()
link = request.LAN("lan")

for i in range(6):
  node = request.XenVM("node" + str(i))
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"
  
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address("192.168.1." + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)
  
  if i == 0:
    node.routable_control_ip = "true"
  
  # Install and execute a script that is contained in the repository.
  #node.addService(pg.Execute(shell="sh", command="/local/repository/silly.sh"))

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
