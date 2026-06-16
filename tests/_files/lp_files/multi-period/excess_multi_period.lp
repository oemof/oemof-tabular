\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(electricity_excess_0)
+10 flow(electricity_excess_1)
+10 flow(electricity_excess_2)
+8.203482998751552 flow(electricity_excess_3)
+8.203482998751552 flow(electricity_excess_4)
+8.203482998751552 flow(electricity_excess_5)
+6.729713331080575 flow(electricity_excess_6)
+6.729713331080575 flow(electricity_excess_7)
+6.729713331080575 flow(electricity_excess_8)

s.t.

c_e_BusBlock_balance(electricity_0)_:
+1 flow(electricity_excess_0)
= 0

c_e_BusBlock_balance(electricity_1)_:
+1 flow(electricity_excess_1)
= 0

c_e_BusBlock_balance(electricity_2)_:
+1 flow(electricity_excess_2)
= 0

c_e_BusBlock_balance(electricity_3)_:
+1 flow(electricity_excess_3)
= 0

c_e_BusBlock_balance(electricity_4)_:
+1 flow(electricity_excess_4)
= 0

c_e_BusBlock_balance(electricity_5)_:
+1 flow(electricity_excess_5)
= 0

c_e_BusBlock_balance(electricity_6)_:
+1 flow(electricity_excess_6)
= 0

c_e_BusBlock_balance(electricity_7)_:
+1 flow(electricity_excess_7)
= 0

c_e_BusBlock_balance(electricity_8)_:
+1 flow(electricity_excess_8)
= 0

bounds
   0 <= flow(electricity_excess_0) <= 1000
   0 <= flow(electricity_excess_1) <= 1000
   0 <= flow(electricity_excess_2) <= 1000
   0 <= flow(electricity_excess_3) <= 1000
   0 <= flow(electricity_excess_4) <= 1000
   0 <= flow(electricity_excess_5) <= 1000
   0 <= flow(electricity_excess_6) <= 1000
   0 <= flow(electricity_excess_7) <= 1000
   0 <= flow(electricity_excess_8) <= 1000
end
