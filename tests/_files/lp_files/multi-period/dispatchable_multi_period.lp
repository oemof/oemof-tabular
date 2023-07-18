\* Source Pyomo model name=Model *\

min 
objective:
+393187.4631175658 ONE_VAR_CONSTANT
+561.5105784699618 InvestmentFlowBlock_invest(gt_electricity_0)
+386.89361416194254 InvestmentFlowBlock_invest(gt_electricity_1)
+267.76218567632424 InvestmentFlowBlock_invest(gt_electricity_2)
+10 flow(gt_electricity_0_0)
+10 flow(gt_electricity_0_1)
+10 flow(gt_electricity_0_2)
+8.203482998751552 flow(gt_electricity_1_3)
+8.203482998751552 flow(gt_electricity_1_4)
+8.203482998751552 flow(gt_electricity_1_5)
+6.729713331080575 flow(gt_electricity_2_6)
+6.729713331080575 flow(gt_electricity_2_7)
+6.729713331080575 flow(gt_electricity_2_8)

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

c_e_BusBlock_balance(electricity_1_3)_:
+1 flow(gt_electricity_1_3)
= 0

c_e_BusBlock_balance(electricity_1_4)_:
+1 flow(gt_electricity_1_4)
= 0

c_e_BusBlock_balance(electricity_1_5)_:
+1 flow(gt_electricity_1_5)
= 0

c_e_BusBlock_balance(electricity_2_6)_:
+1 flow(gt_electricity_2_6)
= 0

c_e_BusBlock_balance(electricity_2_7)_:
+1 flow(gt_electricity_2_7)
= 0

c_e_BusBlock_balance(electricity_2_8)_:
+1 flow(gt_electricity_2_8)
= 0

c_e_InvestmentFlowBlock_total_rule(gt_electricity_0)_:
-1 InvestmentFlowBlock_invest(gt_electricity_0)
+1 InvestmentFlowBlock_total(gt_electricity_0)
= 1000

c_e_InvestmentFlowBlock_total_rule(gt_electricity_1)_:
-1 InvestmentFlowBlock_invest(gt_electricity_1)
-1 InvestmentFlowBlock_total(gt_electricity_0)
+1 InvestmentFlowBlock_total(gt_electricity_1)
+1 InvestmentFlowBlock_old(gt_electricity_1)
= 0

c_e_InvestmentFlowBlock_total_rule(gt_electricity_2)_:
-1 InvestmentFlowBlock_invest(gt_electricity_2)
-1 InvestmentFlowBlock_total(gt_electricity_1)
+1 InvestmentFlowBlock_total(gt_electricity_2)
+1 InvestmentFlowBlock_old(gt_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(gt_electricity_0)_:
+1 InvestmentFlowBlock_old_end(gt_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(gt_electricity_1)_:
+1 InvestmentFlowBlock_old_end(gt_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(gt_electricity_2)_:
-1 InvestmentFlowBlock_invest(gt_electricity_0)
+1 InvestmentFlowBlock_old_end(gt_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(gt_electricity_0)_:
+1 InvestmentFlowBlock_old_exo(gt_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(gt_electricity_1)_:
+1 InvestmentFlowBlock_old_exo(gt_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(gt_electricity_2)_:
+1 InvestmentFlowBlock_old_exo(gt_electricity_2)
= 1000

c_e_InvestmentFlowBlock_old_rule(gt_electricity_0)_:
-1 InvestmentFlowBlock_old_end(gt_electricity_0)
-1 InvestmentFlowBlock_old_exo(gt_electricity_0)
+1 InvestmentFlowBlock_old(gt_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule(gt_electricity_1)_:
+1 InvestmentFlowBlock_old(gt_electricity_1)
-1 InvestmentFlowBlock_old_end(gt_electricity_1)
-1 InvestmentFlowBlock_old_exo(gt_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule(gt_electricity_2)_:
+1 InvestmentFlowBlock_old(gt_electricity_2)
-1 InvestmentFlowBlock_old_end(gt_electricity_2)
-1 InvestmentFlowBlock_old_exo(gt_electricity_2)
= 0

c_u_InvestmentFlowBlock_max(gt_electricity_0_0)_:
+1 flow(gt_electricity_0_0)
-1 InvestmentFlowBlock_total(gt_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(gt_electricity_0_1)_:
+1 flow(gt_electricity_0_1)
-1 InvestmentFlowBlock_total(gt_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(gt_electricity_0_2)_:
+1 flow(gt_electricity_0_2)
-1 InvestmentFlowBlock_total(gt_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(gt_electricity_1_3)_:
+1 flow(gt_electricity_1_3)
-1 InvestmentFlowBlock_total(gt_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(gt_electricity_1_4)_:
+1 flow(gt_electricity_1_4)
-1 InvestmentFlowBlock_total(gt_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(gt_electricity_1_5)_:
+1 flow(gt_electricity_1_5)
-1 InvestmentFlowBlock_total(gt_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(gt_electricity_2_6)_:
+1 flow(gt_electricity_2_6)
-1 InvestmentFlowBlock_total(gt_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(gt_electricity_2_7)_:
+1 flow(gt_electricity_2_7)
-1 InvestmentFlowBlock_total(gt_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(gt_electricity_2_8)_:
+1 flow(gt_electricity_2_8)
-1 InvestmentFlowBlock_total(gt_electricity_2)
<= 0

c_u_InvestmentFlowBlock_min(gt_electricity_0_0)_:
-1 flow(gt_electricity_0_0)
+0.2 InvestmentFlowBlock_total(gt_electricity_0)
<= 0

c_u_InvestmentFlowBlock_min(gt_electricity_0_1)_:
-1 flow(gt_electricity_0_1)
+0.2 InvestmentFlowBlock_total(gt_electricity_0)
<= 0

c_u_InvestmentFlowBlock_min(gt_electricity_0_2)_:
-1 flow(gt_electricity_0_2)
+0.2 InvestmentFlowBlock_total(gt_electricity_0)
<= 0

c_u_InvestmentFlowBlock_min(gt_electricity_1_3)_:
-1 flow(gt_electricity_1_3)
+0.2 InvestmentFlowBlock_total(gt_electricity_1)
<= 0

c_u_InvestmentFlowBlock_min(gt_electricity_1_4)_:
-1 flow(gt_electricity_1_4)
+0.2 InvestmentFlowBlock_total(gt_electricity_1)
<= 0

c_u_InvestmentFlowBlock_min(gt_electricity_1_5)_:
-1 flow(gt_electricity_1_5)
+0.2 InvestmentFlowBlock_total(gt_electricity_1)
<= 0

c_u_InvestmentFlowBlock_min(gt_electricity_2_6)_:
-1 flow(gt_electricity_2_6)
+0.2 InvestmentFlowBlock_total(gt_electricity_2)
<= 0

c_u_InvestmentFlowBlock_min(gt_electricity_2_7)_:
-1 flow(gt_electricity_2_7)
+0.2 InvestmentFlowBlock_total(gt_electricity_2)
<= 0

c_u_InvestmentFlowBlock_min(gt_electricity_2_8)_:
-1 flow(gt_electricity_2_8)
+0.2 InvestmentFlowBlock_total(gt_electricity_2)
<= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= InvestmentFlowBlock_invest(gt_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_invest(gt_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_invest(gt_electricity_2) <= +inf
   0 <= flow(gt_electricity_0_0) <= +inf
   0 <= flow(gt_electricity_0_1) <= +inf
   0 <= flow(gt_electricity_0_2) <= +inf
   0 <= flow(gt_electricity_1_3) <= +inf
   0 <= flow(gt_electricity_1_4) <= +inf
   0 <= flow(gt_electricity_1_5) <= +inf
   0 <= flow(gt_electricity_2_6) <= +inf
   0 <= flow(gt_electricity_2_7) <= +inf
   0 <= flow(gt_electricity_2_8) <= +inf
   0 <= InvestmentFlowBlock_total(gt_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_total(gt_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old(gt_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_total(gt_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(gt_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(gt_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(gt_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(gt_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(gt_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(gt_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(gt_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(gt_electricity_0) <= +inf
end
