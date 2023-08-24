\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(electricity_excess_0_0)
+10 flow(electricity_excess_0_1)
+10 flow(electricity_excess_0_2)
+8.203482998751552 flow(electricity_excess_1_3)
+8.203482998751552 flow(electricity_excess_1_4)
+8.203482998751552 flow(electricity_excess_1_5)
+6.729713331080575 flow(electricity_excess_2_6)
+6.729713331080575 flow(electricity_excess_2_7)
+6.729713331080575 flow(electricity_excess_2_8)

s.t.

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(electricity_excess_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(electricity_excess_0_1)
= 0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(electricity_excess_0_2)
= 0

c_e_BusBlock_balance(electricity_1_3)_:
+1 flow(electricity_excess_1_3)
= 0

c_e_BusBlock_balance(electricity_1_4)_:
+1 flow(electricity_excess_1_4)
= 0

c_e_BusBlock_balance(electricity_1_5)_:
+1 flow(electricity_excess_1_5)
= 0

c_e_BusBlock_balance(electricity_2_6)_:
+1 flow(electricity_excess_2_6)
= 0

c_e_BusBlock_balance(electricity_2_7)_:
+1 flow(electricity_excess_2_7)
= 0

c_e_BusBlock_balance(electricity_2_8)_:
+1 flow(electricity_excess_2_8)
= 0

bounds
   0 <= flow(electricity_excess_0_0) <= 1000
   0 <= flow(electricity_excess_0_1) <= 1000
   0 <= flow(electricity_excess_0_2) <= 1000
   0 <= flow(electricity_excess_1_3) <= 1000
   0 <= flow(electricity_excess_1_4) <= 1000
   0 <= flow(electricity_excess_1_5) <= 1000
   0 <= flow(electricity_excess_2_6) <= 1000
   0 <= flow(electricity_excess_2_7) <= 1000
   0 <= flow(electricity_excess_2_8) <= 1000
end
