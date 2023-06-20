\* Source Pyomo model name=Model *\

min
objective:
+4 flow(link_bus1_0)
+4 flow(link_bus1_1)
+4 flow(link_bus1_2)
+4 flow(link_bus2_0)
+4 flow(link_bus2_1)
+4 flow(link_bus2_2)

s.t.

c_e_BusBlock_balance(bus1_0)_:
-1 flow(bus1_link_0)
+1 flow(link_bus1_0)
= 0

c_e_BusBlock_balance(bus1_1)_:
-1 flow(bus1_link_1)
+1 flow(link_bus1_1)
= 0

c_e_BusBlock_balance(bus1_2)_:
-1 flow(bus1_link_2)
+1 flow(link_bus1_2)
= 0

c_e_BusBlock_balance(bus2_0)_:
-1 flow(bus2_link_0)
+1 flow(link_bus2_0)
= 0

c_e_BusBlock_balance(bus2_1)_:
-1 flow(bus2_link_1)
+1 flow(link_bus2_1)
= 0

c_e_BusBlock_balance(bus2_2)_:
-1 flow(bus2_link_2)
+1 flow(link_bus2_2)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_0)_:
-0.75 flow(bus1_link_0)
+1 flow(link_bus2_0)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_1)_:
-0.75 flow(bus1_link_1)
+1 flow(link_bus2_1)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_2)_:
-0.75 flow(bus1_link_2)
+1 flow(link_bus2_2)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_0)_:
-0.75 flow(bus2_link_0)
+1 flow(link_bus1_0)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_1)_:
-0.75 flow(bus2_link_1)
+1 flow(link_bus1_1)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_2)_:
-0.75 flow(bus2_link_2)
+1 flow(link_bus1_2)
= 0

bounds
   0 <= flow(bus1_link_0) <= +inf
   0 <= flow(bus1_link_1) <= +inf
   0 <= flow(bus1_link_2) <= +inf
   0 <= flow(bus2_link_0) <= +inf
   0 <= flow(bus2_link_1) <= +inf
   0 <= flow(bus2_link_2) <= +inf
   0 <= flow(link_bus1_0) <= 80
   0 <= flow(link_bus1_1) <= 80
   0 <= flow(link_bus1_2) <= 80
   0 <= flow(link_bus2_0) <= 100
   0 <= flow(link_bus2_1) <= 100
   0 <= flow(link_bus2_2) <= 100
end
