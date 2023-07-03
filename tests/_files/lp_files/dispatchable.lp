\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(gt_electricity_0_0)
+10 flow(gt_electricity_0_1)
+10 flow(gt_electricity_0_2)

s.t.

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(gt_electricity_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(gt_electricity_0_1)
= 0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(gt_electricity_0_2)
= 0

bounds
   200.0 <= flow(gt_electricity_0_0) <= 1000
   200.0 <= flow(gt_electricity_0_1) <= 1000
   200.0 <= flow(gt_electricity_0_2) <= 1000
end
