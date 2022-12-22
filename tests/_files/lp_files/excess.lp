\* Source Pyomo model name=Model *\

min
objective:
+10 flow(electricity_excess_0)
+10 flow(electricity_excess_1)
+10 flow(electricity_excess_2)

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

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricity_excess_0) <= 1000
   0 <= flow(electricity_excess_1) <= 1000
   0 <= flow(electricity_excess_2) <= 1000
end
