\* Source Pyomo model name=Model *\

min 
objective:
+5 flow(storage_electricity_0_0)
+5 flow(storage_electricity_0_1)
+5 flow(storage_electricity_0_2)
+4.101741499375776 flow(storage_electricity_1_3)
+4.101741499375776 flow(storage_electricity_1_4)
+4.101741499375776 flow(storage_electricity_1_5)
+3.3648566655402874 flow(storage_electricity_2_6)
+3.3648566655402874 flow(storage_electricity_2_7)
+3.3648566655402874 flow(storage_electricity_2_8)
+12.231343625058066 GenericInvestmentStorageBlock_invest(storage_0)
+10.033961948005201 GenericInvestmentStorageBlock_invest(storage_1)
+8.231343625058066 GenericInvestmentStorageBlock_invest(storage_2)

s.t.

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(storage_electricity_0_0)
-1 flow(electricity_storage_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(storage_electricity_0_1)
-1 flow(electricity_storage_0_1)
= 0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(storage_electricity_0_2)
-1 flow(electricity_storage_0_2)
= 0

c_e_BusBlock_balance(electricity_1_3)_:
+1 flow(storage_electricity_1_3)
-1 flow(electricity_storage_1_3)
= 0

c_e_BusBlock_balance(electricity_1_4)_:
+1 flow(storage_electricity_1_4)
-1 flow(electricity_storage_1_4)
= 0

c_e_BusBlock_balance(electricity_1_5)_:
+1 flow(storage_electricity_1_5)
-1 flow(electricity_storage_1_5)
= 0

c_e_BusBlock_balance(electricity_2_6)_:
+1 flow(storage_electricity_2_6)
-1 flow(electricity_storage_2_6)
= 0

c_e_BusBlock_balance(electricity_2_7)_:
+1 flow(storage_electricity_2_7)
-1 flow(electricity_storage_2_7)
= 0

c_e_BusBlock_balance(electricity_2_8)_:
+1 flow(storage_electricity_2_8)
-1 flow(electricity_storage_2_8)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_0)_:
+1 InvestmentFlowBlock_total(electricity_storage_0)
-1 InvestmentFlowBlock_invest(electricity_storage_0)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_1)_:
-1 InvestmentFlowBlock_total(electricity_storage_0)
+1 InvestmentFlowBlock_total(electricity_storage_1)
-1 InvestmentFlowBlock_invest(electricity_storage_1)
+1 InvestmentFlowBlock_old(electricity_storage_1)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_2)_:
-1 InvestmentFlowBlock_total(electricity_storage_1)
+1 InvestmentFlowBlock_total(electricity_storage_2)
-1 InvestmentFlowBlock_invest(electricity_storage_2)
+1 InvestmentFlowBlock_old(electricity_storage_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_0)_:
+1 InvestmentFlowBlock_total(storage_electricity_0)
-1 InvestmentFlowBlock_invest(storage_electricity_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_1)_:
-1 InvestmentFlowBlock_total(storage_electricity_0)
+1 InvestmentFlowBlock_total(storage_electricity_1)
-1 InvestmentFlowBlock_invest(storage_electricity_1)
+1 InvestmentFlowBlock_old(storage_electricity_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_2)_:
-1 InvestmentFlowBlock_total(storage_electricity_1)
+1 InvestmentFlowBlock_total(storage_electricity_2)
-1 InvestmentFlowBlock_invest(storage_electricity_2)
+1 InvestmentFlowBlock_old(storage_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_0)_:
+1 InvestmentFlowBlock_old_end(electricity_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_1)_:
+1 InvestmentFlowBlock_old_end(electricity_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_2)_:
-1 InvestmentFlowBlock_invest(electricity_storage_0)
+1 InvestmentFlowBlock_old_end(electricity_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_0)_:
+1 InvestmentFlowBlock_old_end(storage_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_1)_:
+1 InvestmentFlowBlock_old_end(storage_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_2)_:
-1 InvestmentFlowBlock_invest(storage_electricity_0)
+1 InvestmentFlowBlock_old_end(storage_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_0)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_1)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_2)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_0)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_1)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_2)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_0)_:
-1 InvestmentFlowBlock_old_end(electricity_storage_0)
-1 InvestmentFlowBlock_old_exo(electricity_storage_0)
+1 InvestmentFlowBlock_old(electricity_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_1)_:
+1 InvestmentFlowBlock_old(electricity_storage_1)
-1 InvestmentFlowBlock_old_end(electricity_storage_1)
-1 InvestmentFlowBlock_old_exo(electricity_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_2)_:
+1 InvestmentFlowBlock_old(electricity_storage_2)
-1 InvestmentFlowBlock_old_end(electricity_storage_2)
-1 InvestmentFlowBlock_old_exo(electricity_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_0)_:
-1 InvestmentFlowBlock_old_end(storage_electricity_0)
-1 InvestmentFlowBlock_old_exo(storage_electricity_0)
+1 InvestmentFlowBlock_old(storage_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_1)_:
+1 InvestmentFlowBlock_old(storage_electricity_1)
-1 InvestmentFlowBlock_old_end(storage_electricity_1)
-1 InvestmentFlowBlock_old_exo(storage_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_2)_:
+1 InvestmentFlowBlock_old(storage_electricity_2)
-1 InvestmentFlowBlock_old_end(storage_electricity_2)
-1 InvestmentFlowBlock_old_exo(storage_electricity_2)
= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_0)_:
+1 flow(electricity_storage_0_0)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_1)_:
+1 flow(electricity_storage_0_1)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_2)_:
+1 flow(electricity_storage_0_2)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_3)_:
+1 flow(electricity_storage_1_3)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_4)_:
+1 flow(electricity_storage_1_4)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_5)_:
+1 flow(electricity_storage_1_5)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_6)_:
+1 flow(electricity_storage_2_6)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_7)_:
+1 flow(electricity_storage_2_7)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_8)_:
+1 flow(electricity_storage_2_8)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_0)_:
+1 flow(storage_electricity_0_0)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_1)_:
+1 flow(storage_electricity_0_1)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_2)_:
+1 flow(storage_electricity_0_2)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_3)_:
+1 flow(storage_electricity_1_3)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_4)_:
+1 flow(storage_electricity_1_4)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_5)_:
+1 flow(storage_electricity_1_5)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_6)_:
+1 flow(storage_electricity_2_6)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_7)_:
+1 flow(storage_electricity_2_7)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_8)_:
+1 flow(storage_electricity_2_8)
-1 InvestmentFlowBlock_total(storage_electricity_2)
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
-1 GenericInvestmentStorageBlock_old_end(storage_0)
-1 GenericInvestmentStorageBlock_old_exo(storage_0)
+1 GenericInvestmentStorageBlock_old(storage_0)
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

c_e_GenericInvestmentStorageBlock_balance(storage_0_1)_:
+1 flow(storage_electricity_0_1)
-1 flow(electricity_storage_0_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_2)_:
+1 flow(storage_electricity_0_2)
-1 flow(electricity_storage_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_3)_:
+1 flow(storage_electricity_1_3)
-1 flow(electricity_storage_1_3)
-1 GenericInvestmentStorageBlock_storage_content(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_4)_:
+1 flow(storage_electricity_1_4)
-1 flow(electricity_storage_1_4)
-1 GenericInvestmentStorageBlock_storage_content(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_5)_:
+1 flow(storage_electricity_1_5)
-1 flow(electricity_storage_1_5)
-1 GenericInvestmentStorageBlock_storage_content(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_5)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_6)_:
+1 flow(storage_electricity_2_6)
-1 flow(electricity_storage_2_6)
-1 GenericInvestmentStorageBlock_storage_content(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_6)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_7)_:
+1 flow(storage_electricity_2_7)
-1 flow(electricity_storage_2_7)
-1 GenericInvestmentStorageBlock_storage_content(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_7)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_8)_:
+1 flow(storage_electricity_2_8)
-1 flow(electricity_storage_2_8)
-1 GenericInvestmentStorageBlock_storage_content(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_8)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_0)_:
-1 InvestmentFlowBlock_total(electricity_storage_0)
+1 InvestmentFlowBlock_total(storage_electricity_0)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_1)_:
-1 InvestmentFlowBlock_total(electricity_storage_1)
+1 InvestmentFlowBlock_total(storage_electricity_1)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_2)_:
-1 InvestmentFlowBlock_total(electricity_storage_2)
+1 InvestmentFlowBlock_total(storage_electricity_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_0)_:
+1 InvestmentFlowBlock_total(storage_electricity_0)
-0.125 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_1)_:
+1 InvestmentFlowBlock_total(storage_electricity_1)
-0.125 GenericInvestmentStorageBlock_total(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_2)_:
+1 InvestmentFlowBlock_total(storage_electricity_2)
-0.125 GenericInvestmentStorageBlock_total(storage_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_0)_:
-0.75 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_1)_:
-0.5 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_2)_:
-0.25 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_3)_:
-0.75 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_4)_:
-0.5 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_5)_:
-0.25 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_5)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_6)_:
-0.75 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_6)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_7)_:
-0.5 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_7)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_8)_:
-0.25 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_8)
<= 0

bounds
   0 <= flow(storage_electricity_0_0) <= +inf
   0 <= flow(storage_electricity_0_1) <= +inf
   0 <= flow(storage_electricity_0_2) <= +inf
   0 <= flow(storage_electricity_1_3) <= +inf
   0 <= flow(storage_electricity_1_4) <= +inf
   0 <= flow(storage_electricity_1_5) <= +inf
   0 <= flow(storage_electricity_2_6) <= +inf
   0 <= flow(storage_electricity_2_7) <= +inf
   0 <= flow(storage_electricity_2_8) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_2) <= +inf
   0 <= flow(electricity_storage_0_0) <= +inf
   0 <= flow(electricity_storage_0_1) <= +inf
   0 <= flow(electricity_storage_0_2) <= +inf
   0 <= flow(electricity_storage_1_3) <= +inf
   0 <= flow(electricity_storage_1_4) <= +inf
   0 <= flow(electricity_storage_1_5) <= +inf
   0 <= flow(electricity_storage_2_6) <= +inf
   0 <= flow(electricity_storage_2_7) <= +inf
   0 <= flow(electricity_storage_2_8) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_0) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_1) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_1) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_2) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_5) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_6) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_7) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_8) <= +inf
end
