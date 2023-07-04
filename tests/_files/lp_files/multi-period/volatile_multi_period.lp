\* Source Pyomo model name=Model *\

min 
objective:
+159.11879557824162 InvestmentFlowBlock_invest(wind_bus_el_0)
+130.53283343079286 InvestmentFlowBlock_invest(wind_bus_el_1)
+107.08238798283774 InvestmentFlowBlock_invest(wind_bus_el_2)

s.t.

c_e_BusBlock_balance(bus_el_0_0)_:
+1 flow(wind_bus_el_0_0)
= 0

c_e_BusBlock_balance(bus_el_0_1)_:
+1 flow(wind_bus_el_0_1)
= 0

c_e_BusBlock_balance(bus_el_0_2)_:
+1 flow(wind_bus_el_0_2)
= 0

c_e_BusBlock_balance(bus_el_1_3)_:
+1 flow(wind_bus_el_1_3)
= 0

c_e_BusBlock_balance(bus_el_1_4)_:
+1 flow(wind_bus_el_1_4)
= 0

c_e_BusBlock_balance(bus_el_1_5)_:
+1 flow(wind_bus_el_1_5)
= 0

c_e_BusBlock_balance(bus_el_2_6)_:
+1 flow(wind_bus_el_2_6)
= 0

c_e_BusBlock_balance(bus_el_2_7)_:
+1 flow(wind_bus_el_2_7)
= 0

c_e_BusBlock_balance(bus_el_2_8)_:
+1 flow(wind_bus_el_2_8)
= 0

c_e_InvestmentFlowBlock_total_rule(wind_bus_el_0)_:
-1 InvestmentFlowBlock_invest(wind_bus_el_0)
+1 InvestmentFlowBlock_total(wind_bus_el_0)
= 10

c_e_InvestmentFlowBlock_total_rule(wind_bus_el_1)_:
-1 InvestmentFlowBlock_invest(wind_bus_el_1)
-1 InvestmentFlowBlock_total(wind_bus_el_0)
+1 InvestmentFlowBlock_total(wind_bus_el_1)
+1 InvestmentFlowBlock_old(wind_bus_el_1)
= 0

c_e_InvestmentFlowBlock_total_rule(wind_bus_el_2)_:
-1 InvestmentFlowBlock_invest(wind_bus_el_2)
-1 InvestmentFlowBlock_total(wind_bus_el_1)
+1 InvestmentFlowBlock_total(wind_bus_el_2)
+1 InvestmentFlowBlock_old(wind_bus_el_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_bus_el_0)_:
+1 InvestmentFlowBlock_old_end(wind_bus_el_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_bus_el_1)_:
-1 InvestmentFlowBlock_invest(wind_bus_el_0)
+1 InvestmentFlowBlock_old_end(wind_bus_el_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_bus_el_2)_:
-1 InvestmentFlowBlock_invest(wind_bus_el_1)
+1 InvestmentFlowBlock_old_end(wind_bus_el_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_bus_el_0)_:
+1 InvestmentFlowBlock_old_exo(wind_bus_el_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_bus_el_1)_:
+1 InvestmentFlowBlock_old_exo(wind_bus_el_1)
= 10

c_e_InvestmentFlowBlock_old_rule_exo(wind_bus_el_2)_:
+1 InvestmentFlowBlock_old_exo(wind_bus_el_2)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_bus_el_0)_:
-1 InvestmentFlowBlock_old_end(wind_bus_el_0)
-1 InvestmentFlowBlock_old_exo(wind_bus_el_0)
+1 InvestmentFlowBlock_old(wind_bus_el_0)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_bus_el_1)_:
+1 InvestmentFlowBlock_old(wind_bus_el_1)
-1 InvestmentFlowBlock_old_end(wind_bus_el_1)
-1 InvestmentFlowBlock_old_exo(wind_bus_el_1)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_bus_el_2)_:
+1 InvestmentFlowBlock_old(wind_bus_el_2)
-1 InvestmentFlowBlock_old_end(wind_bus_el_2)
-1 InvestmentFlowBlock_old_exo(wind_bus_el_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_bus_el_0_0)_:
+1 flow(wind_bus_el_0_0)
-0.25 InvestmentFlowBlock_total(wind_bus_el_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_bus_el_0_1)_:
+1 flow(wind_bus_el_0_1)
-0.1 InvestmentFlowBlock_total(wind_bus_el_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_bus_el_0_2)_:
+1 flow(wind_bus_el_0_2)
-0.3 InvestmentFlowBlock_total(wind_bus_el_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_bus_el_1_3)_:
+1 flow(wind_bus_el_1_3)
-0.25 InvestmentFlowBlock_total(wind_bus_el_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_bus_el_1_4)_:
+1 flow(wind_bus_el_1_4)
-0.1 InvestmentFlowBlock_total(wind_bus_el_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_bus_el_1_5)_:
+1 flow(wind_bus_el_1_5)
-0.3 InvestmentFlowBlock_total(wind_bus_el_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_bus_el_2_6)_:
+1 flow(wind_bus_el_2_6)
-0.25 InvestmentFlowBlock_total(wind_bus_el_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_bus_el_2_7)_:
+1 flow(wind_bus_el_2_7)
-0.1 InvestmentFlowBlock_total(wind_bus_el_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_bus_el_2_8)_:
+1 flow(wind_bus_el_2_8)
-0.3 InvestmentFlowBlock_total(wind_bus_el_2)
= 0

bounds
   0 <= InvestmentFlowBlock_invest(wind_bus_el_0) <= 90
   0 <= InvestmentFlowBlock_invest(wind_bus_el_1) <= 90
   0 <= InvestmentFlowBlock_invest(wind_bus_el_2) <= 90
   0 <= flow(wind_bus_el_0_0) <= +inf
   0 <= flow(wind_bus_el_0_1) <= +inf
   0 <= flow(wind_bus_el_0_2) <= +inf
   0 <= flow(wind_bus_el_1_3) <= +inf
   0 <= flow(wind_bus_el_1_4) <= +inf
   0 <= flow(wind_bus_el_1_5) <= +inf
   0 <= flow(wind_bus_el_2_6) <= +inf
   0 <= flow(wind_bus_el_2_7) <= +inf
   0 <= flow(wind_bus_el_2_8) <= +inf
   0 <= InvestmentFlowBlock_total(wind_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_total(wind_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_old(wind_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_total(wind_bus_el_2) <= +inf
   0 <= InvestmentFlowBlock_old(wind_bus_el_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_bus_el_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_bus_el_2) <= +inf
   0 <= InvestmentFlowBlock_old(wind_bus_el_0) <= +inf
end
