\* Source Pyomo model name=Model *\

min
objective:
+540 InvestmentFlow_invest(link_bus1)
+540 InvestmentFlow_invest(link_bus2)
+22 flow(link_bus1_0)
+22 flow(link_bus1_1)
+22 flow(link_bus1_2)
+22 flow(link_bus2_0)
+22 flow(link_bus2_1)
+22 flow(link_bus2_2)

s.t.

c_e_Bus_balance(bus1_0)_:
-1 flow(bus1_link_0)
+1 flow(link_bus1_0)
= 0

c_e_Bus_balance(bus1_1)_:
-1 flow(bus1_link_1)
+1 flow(link_bus1_1)
= 0

c_e_Bus_balance(bus1_2)_:
-1 flow(bus1_link_2)
+1 flow(link_bus1_2)
= 0

c_e_Bus_balance(bus2_0)_:
-1 flow(bus2_link_0)
+1 flow(link_bus2_0)
= 0

c_e_Bus_balance(bus2_1)_:
-1 flow(bus2_link_1)
+1 flow(link_bus2_1)
= 0

c_e_Bus_balance(bus2_2)_:
-1 flow(bus2_link_2)
+1 flow(link_bus2_2)
= 0

c_u_InvestmentFlow_max(link_bus1_0)_:
-1 InvestmentFlow_invest(link_bus1)
+1 flow(link_bus1_0)
<= 0

c_u_InvestmentFlow_max(link_bus1_1)_:
-1 InvestmentFlow_invest(link_bus1)
+1 flow(link_bus1_1)
<= 0

c_u_InvestmentFlow_max(link_bus1_2)_:
-1 InvestmentFlow_invest(link_bus1)
+1 flow(link_bus1_2)
<= 0

c_u_InvestmentFlow_max(link_bus2_0)_:
-1 InvestmentFlow_invest(link_bus2)
+1 flow(link_bus2_0)
<= 0

c_u_InvestmentFlow_max(link_bus2_1)_:
-1 InvestmentFlow_invest(link_bus2)
+1 flow(link_bus2_1)
<= 0

c_u_InvestmentFlow_max(link_bus2_2)_:
-1 InvestmentFlow_invest(link_bus2)
+1 flow(link_bus2_2)
<= 0

c_e_LinkBlock_relation(link_bus1_bus2_0)_:
-0.95999999999999996 flow(bus1_link_0)
+1 flow(link_bus2_0)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_1)_:
-0.95999999999999996 flow(bus1_link_1)
+1 flow(link_bus2_1)
= 0

c_e_LinkBlock_relation(link_bus1_bus2_2)_:
-0.95999999999999996 flow(bus1_link_2)
+1 flow(link_bus2_2)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_0)_:
-0.95999999999999996 flow(bus2_link_0)
+1 flow(link_bus1_0)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_1)_:
-0.95999999999999996 flow(bus2_link_1)
+1 flow(link_bus1_1)
= 0

c_e_LinkBlock_relation(link_bus2_bus1_2)_:
-0.95999999999999996 flow(bus2_link_2)
+1 flow(link_bus1_2)
= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus1_link_0) <= +inf
   0 <= flow(bus1_link_1) <= +inf
   0 <= flow(bus1_link_2) <= +inf
   0 <= flow(bus2_link_0) <= +inf
   0 <= flow(bus2_link_1) <= +inf
   0 <= flow(bus2_link_2) <= +inf
   0 <= flow(link_bus1_0) <= +inf
   0 <= flow(link_bus1_1) <= +inf
   0 <= flow(link_bus1_2) <= +inf
   0 <= flow(link_bus2_0) <= +inf
   0 <= flow(link_bus2_1) <= +inf
   0 <= flow(link_bus2_2) <= +inf
   0 <= InvestmentFlow_invest(link_bus1) <= +inf
   0 <= InvestmentFlow_invest(link_bus2) <= +inf
end
