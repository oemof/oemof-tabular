\* Source Pyomo model name=Model *\

min
objective:
+10 flow(gt_electricity_0)
+10 flow(gt_electricity_1)
+10 flow(gt_electricity_2)

s.t.

c_e_BusBlock_balance(electricity_0)_:
+1 flow(gt_electricity_0)
= 0

c_e_BusBlock_balance(electricity_1)_:
+1 flow(gt_electricity_1)
= 0

c_e_BusBlock_balance(electricity_2)_:
+1 flow(gt_electricity_2)
= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   200 <= flow(gt_electricity_0) <= 1000
   200 <= flow(gt_electricity_1) <= 1000
   200 <= flow(gt_electricity_2) <= 1000
end
