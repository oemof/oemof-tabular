\* Source Pyomo model name=Model *\

min 
objective:
+4 flow(link_bus1_0_0)
+4 flow(link_bus1_0_1)
+4 flow(link_bus1_0_2)
+4 flow(link_bus2_0_0)
+4 flow(link_bus2_0_1)
+4 flow(link_bus2_0_2)

s.t.

c_e_BusBlock_balance(bus1_0_0)_:
+1 flow(link_bus1_0_0)
-1 flow(bus1_link_0_0)
= 0

c_e_BusBlock_balance(bus1_0_1)_:
+1 flow(link_bus1_0_1)
-1 flow(bus1_link_0_1)
= 0

c_e_BusBlock_balance(bus1_0_2)_:
+1 flow(link_bus1_0_2)
-1 flow(bus1_link_0_2)
= 0

c_e_BusBlock_balance(bus2_0_0)_:
+1 flow(link_bus2_0_0)
-1 flow(bus2_link_0_0)
= 0

c_e_BusBlock_balance(bus2_0_1)_:
+1 flow(link_bus2_0_1)
-1 flow(bus2_link_0_1)
= 0

c_e_BusBlock_balance(bus2_0_2)_:
+1 flow(link_bus2_0_2)
-1 flow(bus2_link_0_2)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_0_0)_:
+1 flow(link_bus2_0_0)
-0.75 flow(bus1_link_0_0)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_0_0)_:
+1 flow(link_bus1_0_0)
-0.75 flow(bus2_link_0_0)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_0_1)_:
+1 flow(link_bus2_0_1)
-0.75 flow(bus1_link_0_1)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_0_1)_:
+1 flow(link_bus1_0_1)
-0.75 flow(bus2_link_0_1)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_0_2)_:
+1 flow(link_bus2_0_2)
-0.75 flow(bus1_link_0_2)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_0_2)_:
+1 flow(link_bus1_0_2)
-0.75 flow(bus2_link_0_2)
= 0

bounds
   0 <= flow(link_bus1_0_0) <= 80
   0 <= flow(link_bus1_0_1) <= 80
   0 <= flow(link_bus1_0_2) <= 80
   0 <= flow(link_bus2_0_0) <= 100
   0 <= flow(link_bus2_0_1) <= 100
   0 <= flow(link_bus2_0_2) <= 100
   0 <= flow(bus1_link_0_0) <= +inf
   0 <= flow(bus1_link_0_1) <= +inf
   0 <= flow(bus1_link_0_2) <= +inf
   0 <= flow(bus2_link_0_0) <= +inf
   0 <= flow(bus2_link_0_1) <= +inf
   0 <= flow(bus2_link_0_2) <= +inf
end
