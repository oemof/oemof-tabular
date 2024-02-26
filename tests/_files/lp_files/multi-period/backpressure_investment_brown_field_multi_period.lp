\* Source Pyomo model name=Model *\

min 
objective:
+393187.4631175658 ONE_VAR_CONSTANT
+550.3538603446715 InvestmentFlowBlock_invest(backpressure_electricity_0)
+226.09002140491177 InvestmentFlowBlock_invest(backpressure_electricity_1)
+15.604198638169356 InvestmentFlowBlock_invest(backpressure_electricity_2)
+0.6 flow(fuel_backpressure_0_0)
+0.6 flow(fuel_backpressure_0_1)
+0.6 flow(fuel_backpressure_0_2)
+0.49220897992509305 flow(fuel_backpressure_1_3)
+0.49220897992509305 flow(fuel_backpressure_1_4)
+0.49220897992509305 flow(fuel_backpressure_1_5)
+0.40378279986483445 flow(fuel_backpressure_2_6)
+0.40378279986483445 flow(fuel_backpressure_2_7)
+0.40378279986483445 flow(fuel_backpressure_2_8)

s.t.

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(backpressure_electricity_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(backpressure_electricity_0_1)
= 0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(backpressure_electricity_0_2)
= 0

c_e_BusBlock_balance(electricity_1_3)_:
+1 flow(backpressure_electricity_1_3)
= 0

c_e_BusBlock_balance(electricity_1_4)_:
+1 flow(backpressure_electricity_1_4)
= 0

c_e_BusBlock_balance(electricity_1_5)_:
+1 flow(backpressure_electricity_1_5)
= 0

c_e_BusBlock_balance(electricity_2_6)_:
+1 flow(backpressure_electricity_2_6)
= 0

c_e_BusBlock_balance(electricity_2_7)_:
+1 flow(backpressure_electricity_2_7)
= 0

c_e_BusBlock_balance(electricity_2_8)_:
+1 flow(backpressure_electricity_2_8)
= 0

c_e_BusBlock_balance(fuel_0_0)_:
+1 flow(fuel_backpressure_0_0)
= 0

c_e_BusBlock_balance(fuel_0_1)_:
+1 flow(fuel_backpressure_0_1)
= 0

c_e_BusBlock_balance(fuel_0_2)_:
+1 flow(fuel_backpressure_0_2)
= 0

c_e_BusBlock_balance(fuel_1_3)_:
+1 flow(fuel_backpressure_1_3)
= 0

c_e_BusBlock_balance(fuel_1_4)_:
+1 flow(fuel_backpressure_1_4)
= 0

c_e_BusBlock_balance(fuel_1_5)_:
+1 flow(fuel_backpressure_1_5)
= 0

c_e_BusBlock_balance(fuel_2_6)_:
+1 flow(fuel_backpressure_2_6)
= 0

c_e_BusBlock_balance(fuel_2_7)_:
+1 flow(fuel_backpressure_2_7)
= 0

c_e_BusBlock_balance(fuel_2_8)_:
+1 flow(fuel_backpressure_2_8)
= 0

c_e_BusBlock_balance(heat_0_0)_:
+1 flow(backpressure_heat_0_0)
= 0

c_e_BusBlock_balance(heat_0_1)_:
+1 flow(backpressure_heat_0_1)
= 0

c_e_BusBlock_balance(heat_0_2)_:
+1 flow(backpressure_heat_0_2)
= 0

c_e_BusBlock_balance(heat_1_3)_:
+1 flow(backpressure_heat_1_3)
= 0

c_e_BusBlock_balance(heat_1_4)_:
+1 flow(backpressure_heat_1_4)
= 0

c_e_BusBlock_balance(heat_1_5)_:
+1 flow(backpressure_heat_1_5)
= 0

c_e_BusBlock_balance(heat_2_6)_:
+1 flow(backpressure_heat_2_6)
= 0

c_e_BusBlock_balance(heat_2_7)_:
+1 flow(backpressure_heat_2_7)
= 0

c_e_BusBlock_balance(heat_2_8)_:
+1 flow(backpressure_heat_2_8)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_0_0)_:
+0.4 flow(fuel_backpressure_0_0)
-1 flow(backpressure_electricity_0_0)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_0_0)_:
+0.35 flow(fuel_backpressure_0_0)
-1 flow(backpressure_heat_0_0)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_0_1)_:
+0.4 flow(fuel_backpressure_0_1)
-1 flow(backpressure_electricity_0_1)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_0_1)_:
+0.35 flow(fuel_backpressure_0_1)
-1 flow(backpressure_heat_0_1)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_0_2)_:
+0.4 flow(fuel_backpressure_0_2)
-1 flow(backpressure_electricity_0_2)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_0_2)_:
+0.35 flow(fuel_backpressure_0_2)
-1 flow(backpressure_heat_0_2)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_1_3)_:
+0.4 flow(fuel_backpressure_1_3)
-1 flow(backpressure_electricity_1_3)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_1_3)_:
+0.35 flow(fuel_backpressure_1_3)
-1 flow(backpressure_heat_1_3)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_1_4)_:
+0.4 flow(fuel_backpressure_1_4)
-1 flow(backpressure_electricity_1_4)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_1_4)_:
+0.35 flow(fuel_backpressure_1_4)
-1 flow(backpressure_heat_1_4)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_1_5)_:
+0.4 flow(fuel_backpressure_1_5)
-1 flow(backpressure_electricity_1_5)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_1_5)_:
+0.35 flow(fuel_backpressure_1_5)
-1 flow(backpressure_heat_1_5)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_2_6)_:
+0.4 flow(fuel_backpressure_2_6)
-1 flow(backpressure_electricity_2_6)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_2_6)_:
+0.35 flow(fuel_backpressure_2_6)
-1 flow(backpressure_heat_2_6)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_2_7)_:
+0.4 flow(fuel_backpressure_2_7)
-1 flow(backpressure_electricity_2_7)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_2_7)_:
+0.35 flow(fuel_backpressure_2_7)
-1 flow(backpressure_heat_2_7)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_2_8)_:
+0.4 flow(fuel_backpressure_2_8)
-1 flow(backpressure_electricity_2_8)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_2_8)_:
+0.35 flow(fuel_backpressure_2_8)
-1 flow(backpressure_heat_2_8)
= 0

c_e_InvestmentFlowBlock_total_rule(backpressure_electricity_0)_:
-1 InvestmentFlowBlock_invest(backpressure_electricity_0)
+1 InvestmentFlowBlock_total(backpressure_electricity_0)
= 1000

c_e_InvestmentFlowBlock_total_rule(backpressure_electricity_1)_:
-1 InvestmentFlowBlock_invest(backpressure_electricity_1)
-1 InvestmentFlowBlock_total(backpressure_electricity_0)
+1 InvestmentFlowBlock_total(backpressure_electricity_1)
+1 InvestmentFlowBlock_old(backpressure_electricity_1)
= 0

c_e_InvestmentFlowBlock_total_rule(backpressure_electricity_2)_:
-1 InvestmentFlowBlock_invest(backpressure_electricity_2)
-1 InvestmentFlowBlock_total(backpressure_electricity_1)
+1 InvestmentFlowBlock_total(backpressure_electricity_2)
+1 InvestmentFlowBlock_old(backpressure_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(backpressure_electricity_0)_:
+1 InvestmentFlowBlock_old_end(backpressure_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(backpressure_electricity_1)_:
+1 InvestmentFlowBlock_old_end(backpressure_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(backpressure_electricity_2)_:
-1 InvestmentFlowBlock_invest(backpressure_electricity_0)
+1 InvestmentFlowBlock_old_end(backpressure_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(backpressure_electricity_0)_:
+1 InvestmentFlowBlock_old_exo(backpressure_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(backpressure_electricity_1)_:
+1 InvestmentFlowBlock_old_exo(backpressure_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(backpressure_electricity_2)_:
+1 InvestmentFlowBlock_old_exo(backpressure_electricity_2)
= 1000

c_e_InvestmentFlowBlock_old_rule(backpressure_electricity_0)_:
+1 InvestmentFlowBlock_old(backpressure_electricity_0)
-1 InvestmentFlowBlock_old_end(backpressure_electricity_0)
-1 InvestmentFlowBlock_old_exo(backpressure_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule(backpressure_electricity_1)_:
+1 InvestmentFlowBlock_old(backpressure_electricity_1)
-1 InvestmentFlowBlock_old_end(backpressure_electricity_1)
-1 InvestmentFlowBlock_old_exo(backpressure_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule(backpressure_electricity_2)_:
+1 InvestmentFlowBlock_old(backpressure_electricity_2)
-1 InvestmentFlowBlock_old_end(backpressure_electricity_2)
-1 InvestmentFlowBlock_old_exo(backpressure_electricity_2)
= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_0_0)_:
+1 flow(backpressure_electricity_0_0)
-1 InvestmentFlowBlock_total(backpressure_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_0_1)_:
+1 flow(backpressure_electricity_0_1)
-1 InvestmentFlowBlock_total(backpressure_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_0_2)_:
+1 flow(backpressure_electricity_0_2)
-1 InvestmentFlowBlock_total(backpressure_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_1_3)_:
+1 flow(backpressure_electricity_1_3)
-1 InvestmentFlowBlock_total(backpressure_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_1_4)_:
+1 flow(backpressure_electricity_1_4)
-1 InvestmentFlowBlock_total(backpressure_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_1_5)_:
+1 flow(backpressure_electricity_1_5)
-1 InvestmentFlowBlock_total(backpressure_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_2_6)_:
+1 flow(backpressure_electricity_2_6)
-1 InvestmentFlowBlock_total(backpressure_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_2_7)_:
+1 flow(backpressure_electricity_2_7)
-1 InvestmentFlowBlock_total(backpressure_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_2_8)_:
+1 flow(backpressure_electricity_2_8)
-1 InvestmentFlowBlock_total(backpressure_electricity_2)
<= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= InvestmentFlowBlock_invest(backpressure_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_invest(backpressure_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_invest(backpressure_electricity_2) <= +inf
   0 <= flow(fuel_backpressure_0_0) <= +inf
   0 <= flow(fuel_backpressure_0_1) <= +inf
   0 <= flow(fuel_backpressure_0_2) <= +inf
   0 <= flow(fuel_backpressure_1_3) <= +inf
   0 <= flow(fuel_backpressure_1_4) <= +inf
   0 <= flow(fuel_backpressure_1_5) <= +inf
   0 <= flow(fuel_backpressure_2_6) <= +inf
   0 <= flow(fuel_backpressure_2_7) <= +inf
   0 <= flow(fuel_backpressure_2_8) <= +inf
   0 <= flow(backpressure_electricity_0_0) <= +inf
   0 <= flow(backpressure_electricity_0_1) <= +inf
   0 <= flow(backpressure_electricity_0_2) <= +inf
   0 <= flow(backpressure_electricity_1_3) <= +inf
   0 <= flow(backpressure_electricity_1_4) <= +inf
   0 <= flow(backpressure_electricity_1_5) <= +inf
   0 <= flow(backpressure_electricity_2_6) <= +inf
   0 <= flow(backpressure_electricity_2_7) <= +inf
   0 <= flow(backpressure_electricity_2_8) <= +inf
   0 <= flow(backpressure_heat_0_0) <= +inf
   0 <= flow(backpressure_heat_0_1) <= +inf
   0 <= flow(backpressure_heat_0_2) <= +inf
   0 <= flow(backpressure_heat_1_3) <= +inf
   0 <= flow(backpressure_heat_1_4) <= +inf
   0 <= flow(backpressure_heat_1_5) <= +inf
   0 <= flow(backpressure_heat_2_6) <= +inf
   0 <= flow(backpressure_heat_2_7) <= +inf
   0 <= flow(backpressure_heat_2_8) <= +inf
   0 <= InvestmentFlowBlock_total(backpressure_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_total(backpressure_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_total(backpressure_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(backpressure_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old(backpressure_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old(backpressure_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(backpressure_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(backpressure_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(backpressure_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(backpressure_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(backpressure_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(backpressure_electricity_2) <= +inf
end
