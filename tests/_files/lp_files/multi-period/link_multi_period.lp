\* Source Pyomo model name=Model *\

min 
objective:
+4 flow(link_bus1_0_0)
+4 flow(link_bus1_0_1)
+4 flow(link_bus1_0_2)
+3.2813931995006205 flow(link_bus1_1_3)
+3.2813931995006205 flow(link_bus1_1_4)
+3.2813931995006205 flow(link_bus1_1_5)
+2.69188533243223 flow(link_bus1_2_6)
+2.69188533243223 flow(link_bus1_2_7)
+2.69188533243223 flow(link_bus1_2_8)
+4 flow(link_bus2_0_0)
+4 flow(link_bus2_0_1)
+4 flow(link_bus2_0_2)
+3.2813931995006205 flow(link_bus2_1_3)
+3.2813931995006205 flow(link_bus2_1_4)
+3.2813931995006205 flow(link_bus2_1_5)
+2.69188533243223 flow(link_bus2_2_6)
+2.69188533243223 flow(link_bus2_2_7)
+2.69188533243223 flow(link_bus2_2_8)

s.t.

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

c_e_BusBlock_balance(bus2_1_3)_:
+1 flow(link_bus2_1_3)
-1 flow(bus2_link_1_3)
= 0

c_e_BusBlock_balance(bus2_1_4)_:
+1 flow(link_bus2_1_4)
-1 flow(bus2_link_1_4)
= 0

c_e_BusBlock_balance(bus2_1_5)_:
+1 flow(link_bus2_1_5)
-1 flow(bus2_link_1_5)
= 0

c_e_BusBlock_balance(bus2_2_6)_:
+1 flow(link_bus2_2_6)
-1 flow(bus2_link_2_6)
= 0

c_e_BusBlock_balance(bus2_2_7)_:
+1 flow(link_bus2_2_7)
-1 flow(bus2_link_2_7)
= 0

c_e_BusBlock_balance(bus2_2_8)_:
+1 flow(link_bus2_2_8)
-1 flow(bus2_link_2_8)
= 0

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

c_e_BusBlock_balance(bus1_1_3)_:
+1 flow(link_bus1_1_3)
-1 flow(bus1_link_1_3)
= 0

c_e_BusBlock_balance(bus1_1_4)_:
+1 flow(link_bus1_1_4)
-1 flow(bus1_link_1_4)
= 0

c_e_BusBlock_balance(bus1_1_5)_:
+1 flow(link_bus1_1_5)
-1 flow(bus1_link_1_5)
= 0

c_e_BusBlock_balance(bus1_2_6)_:
+1 flow(link_bus1_2_6)
-1 flow(bus1_link_2_6)
= 0

c_e_BusBlock_balance(bus1_2_7)_:
+1 flow(link_bus1_2_7)
-1 flow(bus1_link_2_7)
= 0

c_e_BusBlock_balance(bus1_2_8)_:
+1 flow(link_bus1_2_8)
-1 flow(bus1_link_2_8)
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

c_e_LinkBlock_relation(link_bus1_bus2_1_3)_:
+1 flow(link_bus2_1_3)
-0.75 flow(bus1_link_1_3)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_1_3)_:
+1 flow(link_bus1_1_3)
-0.75 flow(bus2_link_1_3)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_1_4)_:
+1 flow(link_bus2_1_4)
-0.75 flow(bus1_link_1_4)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_1_4)_:
+1 flow(link_bus1_1_4)
-0.75 flow(bus2_link_1_4)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_1_5)_:
+1 flow(link_bus2_1_5)
-0.75 flow(bus1_link_1_5)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_1_5)_:
+1 flow(link_bus1_1_5)
-0.75 flow(bus2_link_1_5)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_2_6)_:
+1 flow(link_bus2_2_6)
-0.75 flow(bus1_link_2_6)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_2_6)_:
+1 flow(link_bus1_2_6)
-0.75 flow(bus2_link_2_6)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_2_7)_:
+1 flow(link_bus2_2_7)
-0.75 flow(bus1_link_2_7)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_2_7)_:
+1 flow(link_bus1_2_7)
-0.75 flow(bus2_link_2_7)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_2_8)_:
+1 flow(link_bus2_2_8)
-0.75 flow(bus1_link_2_8)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_2_8)_:
+1 flow(link_bus1_2_8)
-0.75 flow(bus2_link_2_8)
= 0

bounds
   0 <= flow(link_bus1_0_0) <= 80
   0 <= flow(link_bus1_0_1) <= 80
   0 <= flow(link_bus1_0_2) <= 80
   0 <= flow(link_bus1_1_3) <= 80
   0 <= flow(link_bus1_1_4) <= 80
   0 <= flow(link_bus1_1_5) <= 80
   0 <= flow(link_bus1_2_6) <= 80
   0 <= flow(link_bus1_2_7) <= 80
   0 <= flow(link_bus1_2_8) <= 80
   0 <= flow(link_bus2_0_0) <= 100
   0 <= flow(link_bus2_0_1) <= 100
   0 <= flow(link_bus2_0_2) <= 100
   0 <= flow(link_bus2_1_3) <= 100
   0 <= flow(link_bus2_1_4) <= 100
   0 <= flow(link_bus2_1_5) <= 100
   0 <= flow(link_bus2_2_6) <= 100
   0 <= flow(link_bus2_2_7) <= 100
   0 <= flow(link_bus2_2_8) <= 100
   0 <= flow(bus2_link_0_0) <= +inf
   0 <= flow(bus2_link_0_1) <= +inf
   0 <= flow(bus2_link_0_2) <= +inf
   0 <= flow(bus2_link_1_3) <= +inf
   0 <= flow(bus2_link_1_4) <= +inf
   0 <= flow(bus2_link_1_5) <= +inf
   0 <= flow(bus2_link_2_6) <= +inf
   0 <= flow(bus2_link_2_7) <= +inf
   0 <= flow(bus2_link_2_8) <= +inf
   0 <= flow(bus1_link_0_0) <= +inf
   0 <= flow(bus1_link_0_1) <= +inf
   0 <= flow(bus1_link_0_2) <= +inf
   0 <= flow(bus1_link_1_3) <= +inf
   0 <= flow(bus1_link_1_4) <= +inf
   0 <= flow(bus1_link_1_5) <= +inf
   0 <= flow(bus1_link_2_6) <= +inf
   0 <= flow(bus1_link_2_7) <= +inf
   0 <= flow(bus1_link_2_8) <= +inf
end
