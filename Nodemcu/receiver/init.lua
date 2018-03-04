print(wifi.setmode(wifi.SOFTAP, true))
print(wifi.setphymode(wifi.PHYMODE_B))
cfg = {ssid="Lock signal", pwd="bechtel has mice", auth=wifi.WPA2_PSK, save=true}
print(wifi.ap.config(cfg))
cfg = {ip = "192.168.0.1", netmask = "255.255.255.0", gateway = "192.168.0.1"}
print(wifi.ap.setip(cfg))
print(wifi.ap.dhcp.start())
cfg = nil

srv = net.createServer(net.TCP)
srv:listen(80,function(conn) 
	conn:on("receive",function(cn,request)
		cn:send("Hello world")
		cn:close()
		collectgarbage()
	end) 
end)

collectgarbage()