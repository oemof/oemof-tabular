\* Source Pyomo model name=Model *\

min 
objective:
+450000 ONE_VAR_CONSTANT
+650.0 InvestmentFlowBlock_invest(backpressure_electricity_0)
+359.92657536218167 InvestmentFlowBlock_invest(backpressure_electricity_1)
+32.99787833947502 InvestmentFlowBlock_invest(backpressure_electricity_2)
+0.6 flow(fuel_backpressure_0)
+0.6 flow(fuel_backpressure_1)
+0.6 flow(fuel_backpressure_2)
+0.49220897992509305 flow(fuel_backpressure_3)
+0.49220897992509305 flow(fuel_backpressure_4)
+0.49220897992509305 flow(fuel_backpressure_5)
+0.40378279986483445 flow(fuel_backpressure_6)
+0.40378279986483445 flow(fuel_backpressure_7)
+0.40378279986483445 flow(fuel_backpressure_8)

s.t.

c_e_BusBlock_balance(electricity_0)_:
+1 flow(backpressure_electricity_0)
= 0

c_e_BusBlock_balance(electricity_1)_:
+1 flow(backpressure_electricity_1)
= 0

c_e_BusBlock_balance(electricity_2)_:
+1 flow(backpressure_electricity_2)
= 0

c_e_BusBlock_balance(electricity_3)_:
+1 flow(backpressure_electricity_3)
= 0

c_e_BusBlock_balance(electricity_4)_:
+1 flow(backpressure_electricity_4)
= 0

c_e_BusBlock_balance(electricity_5)_:
+1 flow(backpressure_electricity_5)
= 0

c_e_BusBlock_balance(electricity_6)_:
+1 flow(backpressure_electricity_6)
= 0

c_e_BusBlock_balance(electricity_7)_:
+1 flow(backpressure_electricity_7)
= 0

c_e_BusBlock_balance(electricity_8)_:
+1 flow(backpressure_electricity_8)
= 0

c_e_BusBlock_balance(fuel_0)_:
+1 flow(fuel_backpressure_0)
= 0

c_e_BusBlock_balance(fuel_1)_:
+1 flow(fuel_backpressure_1)
= 0

c_e_BusBlock_balance(fuel_2)_:
+1 flow(fuel_backpressure_2)
= 0

c_e_BusBlock_balance(fuel_3)_:
+1 flow(fuel_backpressure_3)
= 0

c_e_BusBlock_balance(fuel_4)_:
+1 flow(fuel_backpressure_4)
= 0

c_e_BusBlock_balance(fuel_5)_:
+1 flow(fuel_backpressure_5)
= 0

c_e_BusBlock_balance(fuel_6)_:
+1 flow(fuel_backpressure_6)
= 0

c_e_BusBlock_balance(fuel_7)_:
+1 flow(fuel_backpressure_7)
= 0

c_e_BusBlock_balance(fuel_8)_:
+1 flow(fuel_backpressure_8)
= 0

c_e_BusBlock_balance(heat_0)_:
+1 flow(backpressure_heat_0)
= 0

c_e_BusBlock_balance(heat_1)_:
+1 flow(backpressure_heat_1)
= 0

c_e_BusBlock_balance(heat_2)_:
+1 flow(backpressure_heat_2)
= 0

c_e_BusBlock_balance(heat_3)_:
+1 flow(backpressure_heat_3)
= 0

c_e_BusBlock_balance(heat_4)_:
+1 flow(backpressure_heat_4)
= 0

c_e_BusBlock_balance(heat_5)_:
+1 flow(backpressure_heat_5)
= 0

c_e_BusBlock_balance(heat_6)_:
+1 flow(backpressure_heat_6)
= 0

c_e_BusBlock_balance(heat_7)_:
+1 flow(backpressure_heat_7)
= 0

c_e_BusBlock_balance(heat_8)_:
+1 flow(backpressure_heat_8)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_0)_:
+0.4 flow(fuel_backpressure_0)
-1 flow(backpressure_electricity_0)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_0)_:
+0.35 flow(fuel_backpressure_0)
-1 flow(backpressure_heat_0)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_1)_:
+0.4 flow(fuel_backpressure_1)
-1 flow(backpressure_electricity_1)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_1)_:
+0.35 flow(fuel_backpressure_1)
-1 flow(backpressure_heat_1)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_2)_:
+0.4 flow(fuel_backpressure_2)
-1 flow(backpressure_electricity_2)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_2)_:
+0.35 flow(fuel_backpressure_2)
-1 flow(backpressure_heat_2)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_3)_:
+0.4 flow(fuel_backpressure_3)
-1 flow(backpressure_electricity_3)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_3)_:
+0.35 flow(fuel_backpressure_3)
-1 flow(backpressure_heat_3)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_4)_:
+0.4 flow(fuel_backpressure_4)
-1 flow(backpressure_electricity_4)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_4)_:
+0.35 flow(fuel_backpressure_4)
-1 flow(backpressure_heat_4)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_5)_:
+0.4 flow(fuel_backpressure_5)
-1 flow(backpressure_electricity_5)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_5)_:
+0.35 flow(fuel_backpressure_5)
-1 flow(backpressure_heat_5)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_6)_:
+0.4 flow(fuel_backpressure_6)
-1 flow(backpressure_electricity_6)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_6)_:
+0.35 flow(fuel_backpressure_6)
-1 flow(backpressure_heat_6)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_7)_:
+0.4 flow(fuel_backpressure_7)
-1 flow(backpressure_electricity_7)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_7)_:
+0.35 flow(fuel_backpressure_7)
-1 flow(backpressure_heat_7)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_electricity_8)_:
+0.4 flow(fuel_backpressure_8)
-1 flow(backpressure_electricity_8)
= 0

c_e_ConverterBlock_relation(backpressure_fuel_heat_8)_:
+0.35 flow(fuel_backpressure_8)
-1 flow(backpressure_heat_8)
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
+1 flow(backpressure_electricity_0)
-1 InvestmentFlowBlock_total(backpressure_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_0_1)_:
+1 flow(backpressure_electricity_1)
-1 InvestmentFlowBlock_total(backpressure_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_0_2)_:
+1 flow(backpressure_electricity_2)
-1 InvestmentFlowBlock_total(backpressure_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_1_3)_:
+1 flow(backpressure_electricity_3)
-1 InvestmentFlowBlock_total(backpressure_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_1_4)_:
+1 flow(backpressure_electricity_4)
-1 InvestmentFlowBlock_total(backpressure_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_1_5)_:
+1 flow(backpressure_electricity_5)
-1 InvestmentFlowBlock_total(backpressure_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_2_6)_:
+1 flow(backpressure_electricity_6)
-1 InvestmentFlowBlock_total(backpressure_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_2_7)_:
+1 flow(backpressure_electricity_7)
-1 InvestmentFlowBlock_total(backpressure_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_electricity_2_8)_:
+1 flow(backpressure_electricity_8)
-1 InvestmentFlowBlock_total(backpressure_electricity_2)
<= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= InvestmentFlowBlock_invest(backpressure_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_invest(backpressure_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_invest(backpressure_electricity_2) <= +inf
   0 <= flow(fuel_backpressure_0) <= +inf
   0 <= flow(fuel_backpressure_1) <= +inf
   0 <= flow(fuel_backpressure_2) <= +inf
   0 <= flow(fuel_backpressure_3) <= +inf
   0 <= flow(fuel_backpressure_4) <= +inf
   0 <= flow(fuel_backpressure_5) <= +inf
   0 <= flow(fuel_backpressure_6) <= +inf
   0 <= flow(fuel_backpressure_7) <= +inf
   0 <= flow(fuel_backpressure_8) <= +inf
   0 <= flow(backpressure_electricity_0) <= +inf
   0 <= flow(backpressure_electricity_1) <= +inf
   0 <= flow(backpressure_electricity_2) <= +inf
   0 <= flow(backpressure_electricity_3) <= +inf
   0 <= flow(backpressure_electricity_4) <= +inf
   0 <= flow(backpressure_electricity_5) <= +inf
   0 <= flow(backpressure_electricity_6) <= +inf
   0 <= flow(backpressure_electricity_7) <= +inf
   0 <= flow(backpressure_electricity_8) <= +inf
   0 <= flow(backpressure_heat_0) <= +inf
   0 <= flow(backpressure_heat_1) <= +inf
   0 <= flow(backpressure_heat_2) <= +inf
   0 <= flow(backpressure_heat_3) <= +inf
   0 <= flow(backpressure_heat_4) <= +inf
   0 <= flow(backpressure_heat_5) <= +inf
   0 <= flow(backpressure_heat_6) <= +inf
   0 <= flow(backpressure_heat_7) <= +inf
   0 <= flow(backpressure_heat_8) <= +inf
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
