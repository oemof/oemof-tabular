\* Source Pyomo model name=Model *\

min 
objective:
+740.3538603446715 InvestmentFlowBlock_invest(bus_el_storage_0)
+319.3808392388273 InvestmentFlowBlock_invest(bus_el_storage_1)
+23.270646132095994 InvestmentFlowBlock_invest(bus_el_storage_2)
+1800.3538603446716 GenericInvestmentStorageBlock_invest(storage_0)
+839.8454018911981 GenericInvestmentStorageBlock_invest(storage_1)
+66.04135320347618 GenericInvestmentStorageBlock_invest(storage_2)

s.t.

c_e_BusBlock_balance(bus_el_0_0)_:
-1 flow(bus_el_storage_0_0)
+1 flow(storage_bus_el_0_0)
= 0

c_e_BusBlock_balance(bus_el_0_1)_:
-1 flow(bus_el_storage_0_1)
+1 flow(storage_bus_el_0_1)
= 0

c_e_BusBlock_balance(bus_el_0_2)_:
-1 flow(bus_el_storage_0_2)
+1 flow(storage_bus_el_0_2)
= 0

c_e_BusBlock_balance(bus_el_1_3)_:
-1 flow(bus_el_storage_1_3)
+1 flow(storage_bus_el_1_3)
= 0

c_e_BusBlock_balance(bus_el_1_4)_:
-1 flow(bus_el_storage_1_4)
+1 flow(storage_bus_el_1_4)
= 0

c_e_BusBlock_balance(bus_el_1_5)_:
-1 flow(bus_el_storage_1_5)
+1 flow(storage_bus_el_1_5)
= 0

c_e_BusBlock_balance(bus_el_2_6)_:
-1 flow(bus_el_storage_2_6)
+1 flow(storage_bus_el_2_6)
= 0

c_e_BusBlock_balance(bus_el_2_7)_:
-1 flow(bus_el_storage_2_7)
+1 flow(storage_bus_el_2_7)
= 0

c_e_BusBlock_balance(bus_el_2_8)_:
-1 flow(bus_el_storage_2_8)
+1 flow(storage_bus_el_2_8)
= 0

c_e_InvestmentFlowBlock_total_rule(bus_el_storage_0)_:
-1 InvestmentFlowBlock_invest(bus_el_storage_0)
+1 InvestmentFlowBlock_total(bus_el_storage_0)
= 0

c_e_InvestmentFlowBlock_total_rule(bus_el_storage_1)_:
-1 InvestmentFlowBlock_invest(bus_el_storage_1)
-1 InvestmentFlowBlock_total(bus_el_storage_0)
+1 InvestmentFlowBlock_total(bus_el_storage_1)
+1 InvestmentFlowBlock_old(bus_el_storage_1)
= 0

c_e_InvestmentFlowBlock_total_rule(bus_el_storage_2)_:
-1 InvestmentFlowBlock_invest(bus_el_storage_2)
-1 InvestmentFlowBlock_total(bus_el_storage_1)
+1 InvestmentFlowBlock_total(bus_el_storage_2)
+1 InvestmentFlowBlock_old(bus_el_storage_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_bus_el_0)_:
-1 InvestmentFlowBlock_invest(storage_bus_el_0)
+1 InvestmentFlowBlock_total(storage_bus_el_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_bus_el_1)_:
-1 InvestmentFlowBlock_invest(storage_bus_el_1)
-1 InvestmentFlowBlock_total(storage_bus_el_0)
+1 InvestmentFlowBlock_total(storage_bus_el_1)
+1 InvestmentFlowBlock_old(storage_bus_el_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_bus_el_2)_:
-1 InvestmentFlowBlock_invest(storage_bus_el_2)
-1 InvestmentFlowBlock_total(storage_bus_el_1)
+1 InvestmentFlowBlock_total(storage_bus_el_2)
+1 InvestmentFlowBlock_old(storage_bus_el_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(bus_el_storage_0)_:
+1 InvestmentFlowBlock_old_end(bus_el_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(bus_el_storage_1)_:
+1 InvestmentFlowBlock_old_end(bus_el_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(bus_el_storage_2)_:
-1 InvestmentFlowBlock_invest(bus_el_storage_0)
+1 InvestmentFlowBlock_old_end(bus_el_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_bus_el_0)_:
+1 InvestmentFlowBlock_old_end(storage_bus_el_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_bus_el_1)_:
+1 InvestmentFlowBlock_old_end(storage_bus_el_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_bus_el_2)_:
-1 InvestmentFlowBlock_invest(storage_bus_el_0)
+1 InvestmentFlowBlock_old_end(storage_bus_el_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(bus_el_storage_0)_:
+1 InvestmentFlowBlock_old_exo(bus_el_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(bus_el_storage_1)_:
+1 InvestmentFlowBlock_old_exo(bus_el_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(bus_el_storage_2)_:
+1 InvestmentFlowBlock_old_exo(bus_el_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_bus_el_0)_:
+1 InvestmentFlowBlock_old_exo(storage_bus_el_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_bus_el_1)_:
+1 InvestmentFlowBlock_old_exo(storage_bus_el_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_bus_el_2)_:
+1 InvestmentFlowBlock_old_exo(storage_bus_el_2)
= 0

c_e_InvestmentFlowBlock_old_rule(bus_el_storage_0)_:
+1 InvestmentFlowBlock_old(bus_el_storage_0)
-1 InvestmentFlowBlock_old_end(bus_el_storage_0)
-1 InvestmentFlowBlock_old_exo(bus_el_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule(bus_el_storage_1)_:
+1 InvestmentFlowBlock_old(bus_el_storage_1)
-1 InvestmentFlowBlock_old_end(bus_el_storage_1)
-1 InvestmentFlowBlock_old_exo(bus_el_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule(bus_el_storage_2)_:
+1 InvestmentFlowBlock_old(bus_el_storage_2)
-1 InvestmentFlowBlock_old_end(bus_el_storage_2)
-1 InvestmentFlowBlock_old_exo(bus_el_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_bus_el_0)_:
+1 InvestmentFlowBlock_old(storage_bus_el_0)
-1 InvestmentFlowBlock_old_end(storage_bus_el_0)
-1 InvestmentFlowBlock_old_exo(storage_bus_el_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_bus_el_1)_:
+1 InvestmentFlowBlock_old(storage_bus_el_1)
-1 InvestmentFlowBlock_old_end(storage_bus_el_1)
-1 InvestmentFlowBlock_old_exo(storage_bus_el_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_bus_el_2)_:
+1 InvestmentFlowBlock_old(storage_bus_el_2)
-1 InvestmentFlowBlock_old_end(storage_bus_el_2)
-1 InvestmentFlowBlock_old_exo(storage_bus_el_2)
= 0

c_u_InvestmentFlowBlock_max(bus_el_storage_0_0)_:
+1 flow(bus_el_storage_0_0)
-1 InvestmentFlowBlock_total(bus_el_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(bus_el_storage_0_1)_:
+1 flow(bus_el_storage_0_1)
-1 InvestmentFlowBlock_total(bus_el_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(bus_el_storage_0_2)_:
+1 flow(bus_el_storage_0_2)
-1 InvestmentFlowBlock_total(bus_el_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(bus_el_storage_1_3)_:
+1 flow(bus_el_storage_1_3)
-1 InvestmentFlowBlock_total(bus_el_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(bus_el_storage_1_4)_:
+1 flow(bus_el_storage_1_4)
-1 InvestmentFlowBlock_total(bus_el_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(bus_el_storage_1_5)_:
+1 flow(bus_el_storage_1_5)
-1 InvestmentFlowBlock_total(bus_el_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(bus_el_storage_2_6)_:
+1 flow(bus_el_storage_2_6)
-1 InvestmentFlowBlock_total(bus_el_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(bus_el_storage_2_7)_:
+1 flow(bus_el_storage_2_7)
-1 InvestmentFlowBlock_total(bus_el_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(bus_el_storage_2_8)_:
+1 flow(bus_el_storage_2_8)
-1 InvestmentFlowBlock_total(bus_el_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_bus_el_0_0)_:
+1 flow(storage_bus_el_0_0)
-1 InvestmentFlowBlock_total(storage_bus_el_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_bus_el_0_1)_:
+1 flow(storage_bus_el_0_1)
-1 InvestmentFlowBlock_total(storage_bus_el_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_bus_el_0_2)_:
+1 flow(storage_bus_el_0_2)
-1 InvestmentFlowBlock_total(storage_bus_el_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_bus_el_1_3)_:
+1 flow(storage_bus_el_1_3)
-1 InvestmentFlowBlock_total(storage_bus_el_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_bus_el_1_4)_:
+1 flow(storage_bus_el_1_4)
-1 InvestmentFlowBlock_total(storage_bus_el_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_bus_el_1_5)_:
+1 flow(storage_bus_el_1_5)
-1 InvestmentFlowBlock_total(storage_bus_el_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_bus_el_2_6)_:
+1 flow(storage_bus_el_2_6)
-1 InvestmentFlowBlock_total(storage_bus_el_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_bus_el_2_7)_:
+1 flow(storage_bus_el_2_7)
-1 InvestmentFlowBlock_total(storage_bus_el_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_bus_el_2_8)_:
+1 flow(storage_bus_el_2_8)
-1 InvestmentFlowBlock_total(storage_bus_el_2)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_0)
+1 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_1)
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_old(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_2)
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_old(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_0)_:
+1 GenericInvestmentStorageBlock_old_end(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_1)_:
+1 GenericInvestmentStorageBlock_old_end(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_0)
+1 GenericInvestmentStorageBlock_old_end(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_0)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_1)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_0)_:
+1 GenericInvestmentStorageBlock_old(storage_0)
-1 GenericInvestmentStorageBlock_old_end(storage_0)
-1 GenericInvestmentStorageBlock_old_exo(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_1)_:
+1 GenericInvestmentStorageBlock_old(storage_1)
-1 GenericInvestmentStorageBlock_old_end(storage_1)
-1 GenericInvestmentStorageBlock_old_exo(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_2)_:
+1 GenericInvestmentStorageBlock_old(storage_2)
-1 GenericInvestmentStorageBlock_old_end(storage_2)
-1 GenericInvestmentStorageBlock_old_exo(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_initially_empty(storage_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_1)_:
-0.9 flow(bus_el_storage_0_1)
+1.1111111111111112 flow(storage_bus_el_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_2)_:
-0.9 flow(bus_el_storage_0_2)
+1.1111111111111112 flow(storage_bus_el_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_3)_:
-0.9 flow(bus_el_storage_1_3)
+1.1111111111111112 flow(storage_bus_el_1_3)
-1 GenericInvestmentStorageBlock_storage_content(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_4)_:
-0.9 flow(bus_el_storage_1_4)
+1.1111111111111112 flow(storage_bus_el_1_4)
-1 GenericInvestmentStorageBlock_storage_content(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_5)_:
-0.9 flow(bus_el_storage_1_5)
+1.1111111111111112 flow(storage_bus_el_1_5)
-1 GenericInvestmentStorageBlock_storage_content(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_5)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_6)_:
-0.9 flow(bus_el_storage_2_6)
+1.1111111111111112 flow(storage_bus_el_2_6)
-1 GenericInvestmentStorageBlock_storage_content(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_6)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_7)_:
-0.9 flow(bus_el_storage_2_7)
+1.1111111111111112 flow(storage_bus_el_2_7)
-1 GenericInvestmentStorageBlock_storage_content(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_7)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_8)_:
-0.9 flow(bus_el_storage_2_8)
+1.1111111111111112 flow(storage_bus_el_2_8)
-1 GenericInvestmentStorageBlock_storage_content(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_8)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_0)_:
-1 InvestmentFlowBlock_total(bus_el_storage_0)
+1 InvestmentFlowBlock_total(storage_bus_el_0)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_1)_:
-1 InvestmentFlowBlock_total(bus_el_storage_1)
+1 InvestmentFlowBlock_total(storage_bus_el_1)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_2)_:
-1 InvestmentFlowBlock_total(bus_el_storage_2)
+1 InvestmentFlowBlock_total(storage_bus_el_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_2)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_3)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_4)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_5)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_5)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_6)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_6)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_7)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_7)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_8)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_8)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(bus_el_storage_0) <= 3
   0 <= InvestmentFlowBlock_invest(bus_el_storage_1) <= 3
   0 <= InvestmentFlowBlock_invest(bus_el_storage_2) <= 3
   0 <= InvestmentFlowBlock_invest(storage_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_bus_el_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_0) <= 10
   0 <= GenericInvestmentStorageBlock_invest(storage_1) <= 10
   0 <= GenericInvestmentStorageBlock_invest(storage_2) <= 10
   0 <= flow(bus_el_storage_0_0) <= +inf
   0 <= flow(bus_el_storage_0_1) <= +inf
   0 <= flow(bus_el_storage_0_2) <= +inf
   0 <= flow(bus_el_storage_1_3) <= +inf
   0 <= flow(bus_el_storage_1_4) <= +inf
   0 <= flow(bus_el_storage_1_5) <= +inf
   0 <= flow(bus_el_storage_2_6) <= +inf
   0 <= flow(bus_el_storage_2_7) <= +inf
   0 <= flow(bus_el_storage_2_8) <= +inf
   0 <= flow(storage_bus_el_0_0) <= +inf
   0 <= flow(storage_bus_el_0_1) <= +inf
   0 <= flow(storage_bus_el_0_2) <= +inf
   0 <= flow(storage_bus_el_1_3) <= +inf
   0 <= flow(storage_bus_el_1_4) <= +inf
   0 <= flow(storage_bus_el_1_5) <= +inf
   0 <= flow(storage_bus_el_2_6) <= +inf
   0 <= flow(storage_bus_el_2_7) <= +inf
   0 <= flow(storage_bus_el_2_8) <= +inf
   0 <= InvestmentFlowBlock_total(bus_el_storage_0) <= +inf
   0 <= InvestmentFlowBlock_total(bus_el_storage_1) <= +inf
   0 <= InvestmentFlowBlock_total(bus_el_storage_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage_bus_el_2) <= +inf
   0 <= InvestmentFlowBlock_old(bus_el_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old(bus_el_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old(bus_el_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_old(storage_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage_bus_el_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(bus_el_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(bus_el_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(bus_el_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_bus_el_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(bus_el_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(bus_el_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(bus_el_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_bus_el_2) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_5) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_6) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_7) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_8) <= +inf
end
