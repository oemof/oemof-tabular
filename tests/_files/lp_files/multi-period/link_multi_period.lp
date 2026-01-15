\* Source Pyomo model name=Model *\

min 
objective:
+4 flow(link_bus1_0)
+4 flow(link_bus1_1)
+4 flow(link_bus1_2)
+3.2813931995006205 flow(link_bus1_3)
+3.2813931995006205 flow(link_bus1_4)
+3.2813931995006205 flow(link_bus1_5)
+2.69188533243223 flow(link_bus1_6)
+2.69188533243223 flow(link_bus1_7)
+2.69188533243223 flow(link_bus1_8)
+4 flow(link_bus2_0)
+4 flow(link_bus2_1)
+4 flow(link_bus2_2)
+3.2813931995006205 flow(link_bus2_3)
+3.2813931995006205 flow(link_bus2_4)
+3.2813931995006205 flow(link_bus2_5)
+2.69188533243223 flow(link_bus2_6)
+2.69188533243223 flow(link_bus2_7)
+2.69188533243223 flow(link_bus2_8)

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

c_e_BusBlock_balance(bus1_3)_:
-1 flow(bus1_link_3)
+1 flow(link_bus1_3)
= 0

c_e_BusBlock_balance(bus1_4)_:
-1 flow(bus1_link_4)
+1 flow(link_bus1_4)
= 0

c_e_BusBlock_balance(bus1_5)_:
-1 flow(bus1_link_5)
+1 flow(link_bus1_5)
= 0

c_e_BusBlock_balance(bus1_6)_:
-1 flow(bus1_link_6)
+1 flow(link_bus1_6)
= 0

c_e_BusBlock_balance(bus1_7)_:
-1 flow(bus1_link_7)
+1 flow(link_bus1_7)
= 0

c_e_BusBlock_balance(bus1_8)_:
-1 flow(bus1_link_8)
+1 flow(link_bus1_8)
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

c_e_BusBlock_balance(bus2_3)_:
-1 flow(bus2_link_3)
+1 flow(link_bus2_3)
= 0

c_e_BusBlock_balance(bus2_4)_:
-1 flow(bus2_link_4)
+1 flow(link_bus2_4)
= 0

c_e_BusBlock_balance(bus2_5)_:
-1 flow(bus2_link_5)
+1 flow(link_bus2_5)
= 0

c_e_BusBlock_balance(bus2_6)_:
-1 flow(bus2_link_6)
+1 flow(link_bus2_6)
= 0

c_e_BusBlock_balance(bus2_7)_:
-1 flow(bus2_link_7)
+1 flow(link_bus2_7)
= 0

c_e_BusBlock_balance(bus2_8)_:
-1 flow(bus2_link_8)
+1 flow(link_bus2_8)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_0)_:
-0.75 flow(bus1_link_0)
+1 flow(link_bus2_0)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_0)_:
-0.75 flow(bus2_link_0)
+1 flow(link_bus1_0)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_1)_:
-0.75 flow(bus1_link_1)
+1 flow(link_bus2_1)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_1)_:
-0.75 flow(bus2_link_1)
+1 flow(link_bus1_1)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_2)_:
-0.75 flow(bus1_link_2)
+1 flow(link_bus2_2)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_2)_:
-0.75 flow(bus2_link_2)
+1 flow(link_bus1_2)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_3)_:
-0.75 flow(bus1_link_3)
+1 flow(link_bus2_3)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_3)_:
-0.75 flow(bus2_link_3)
+1 flow(link_bus1_3)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_4)_:
-0.75 flow(bus1_link_4)
+1 flow(link_bus2_4)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_4)_:
-0.75 flow(bus2_link_4)
+1 flow(link_bus1_4)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_5)_:
-0.75 flow(bus1_link_5)
+1 flow(link_bus2_5)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_5)_:
-0.75 flow(bus2_link_5)
+1 flow(link_bus1_5)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_6)_:
-0.75 flow(bus1_link_6)
+1 flow(link_bus2_6)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_6)_:
-0.75 flow(bus2_link_6)
+1 flow(link_bus1_6)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_7)_:
-0.75 flow(bus1_link_7)
+1 flow(link_bus2_7)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_7)_:
-0.75 flow(bus2_link_7)
+1 flow(link_bus1_7)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_8)_:
-0.75 flow(bus1_link_8)
+1 flow(link_bus2_8)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_8)_:
-0.75 flow(bus2_link_8)
+1 flow(link_bus1_8)
= 0

bounds
   0 <= flow(bus1_link_0) <= +inf
   0 <= flow(bus1_link_1) <= +inf
   0 <= flow(bus1_link_2) <= +inf
   0 <= flow(bus1_link_3) <= +inf
   0 <= flow(bus1_link_4) <= +inf
   0 <= flow(bus1_link_5) <= +inf
   0 <= flow(bus1_link_6) <= +inf
   0 <= flow(bus1_link_7) <= +inf
   0 <= flow(bus1_link_8) <= +inf
   0 <= flow(bus2_link_0) <= +inf
   0 <= flow(bus2_link_1) <= +inf
   0 <= flow(bus2_link_2) <= +inf
   0 <= flow(bus2_link_3) <= +inf
   0 <= flow(bus2_link_4) <= +inf
   0 <= flow(bus2_link_5) <= +inf
   0 <= flow(bus2_link_6) <= +inf
   0 <= flow(bus2_link_7) <= +inf
   0 <= flow(bus2_link_8) <= +inf
   0 <= flow(link_bus1_0) <= 80
   0 <= flow(link_bus1_1) <= 80
   0 <= flow(link_bus1_2) <= 80
   0 <= flow(link_bus1_3) <= 80
   0 <= flow(link_bus1_4) <= 80
   0 <= flow(link_bus1_5) <= 80
   0 <= flow(link_bus1_6) <= 80
   0 <= flow(link_bus1_7) <= 80
   0 <= flow(link_bus1_8) <= 80
   0 <= flow(link_bus2_0) <= 100
   0 <= flow(link_bus2_1) <= 100
   0 <= flow(link_bus2_2) <= 100
   0 <= flow(link_bus2_3) <= 100
   0 <= flow(link_bus2_4) <= 100
   0 <= flow(link_bus2_5) <= 100
   0 <= flow(link_bus2_6) <= 100
   0 <= flow(link_bus2_7) <= 100
   0 <= flow(link_bus2_8) <= 100
end
