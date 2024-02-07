\* Source Pyomo model name=Model *\

min 
objective:
+550.3538603446715 InvestmentFlowBlock_invest(backpressure_bus_el_0)
+226.09002140491177 InvestmentFlowBlock_invest(backpressure_bus_el_1)
+15.604198638169356 InvestmentFlowBlock_invest(backpressure_bus_el_2)
+0.6 flow(bus_fuel_backpressure_0_0)
+0.6 flow(bus_fuel_backpressure_0_1)
+0.6 flow(bus_fuel_backpressure_0_2)
+0.49220897992509305 flow(bus_fuel_backpressure_1_3)
+0.49220897992509305 flow(bus_fuel_backpressure_1_4)
+0.49220897992509305 flow(bus_fuel_backpressure_1_5)
+0.40378279986483445 flow(bus_fuel_backpressure_2_6)
+0.40378279986483445 flow(bus_fuel_backpressure_2_7)
+0.40378279986483445 flow(bus_fuel_backpressure_2_8)

s.t.

c_e_BusBlock_balance(bus_el_0_0)_:
+1 flow(backpressure_bus_el_0_0)
= 0

c_e_BusBlock_balance(bus_el_0_1)_:
+1 flow(backpressure_bus_el_0_1)
= 0

c_e_BusBlock_balance(bus_el_0_2)_:
+1 flow(backpressure_bus_el_0_2)
= 0

c_e_BusBlock_balance(bus_el_1_3)_:
+1 flow(backpressure_bus_el_1_3)
= 0

c_e_BusBlock_balance(bus_el_1_4)_:
+1 flow(backpressure_bus_el_1_4)
= 0

c_e_BusBlock_balance(bus_el_1_5)_:
+1 flow(backpressure_bus_el_1_5)
= 0

c_e_BusBlock_balance(bus_el_2_6)_:
+1 flow(backpressure_bus_el_2_6)
= 0

c_e_BusBlock_balance(bus_el_2_7)_:
+1 flow(backpressure_bus_el_2_7)
= 0

c_e_BusBlock_balance(bus_el_2_8)_:
+1 flow(backpressure_bus_el_2_8)
= 0

c_e_BusBlock_balance(bus_fuel_0_0)_:
+1 flow(bus_fuel_backpressure_0_0)
= 0

c_e_BusBlock_balance(bus_fuel_0_1)_:
+1 flow(bus_fuel_backpressure_0_1)
= 0

c_e_BusBlock_balance(bus_fuel_0_2)_:
+1 flow(bus_fuel_backpressure_0_2)
= 0

c_e_BusBlock_balance(bus_fuel_1_3)_:
+1 flow(bus_fuel_backpressure_1_3)
= 0

c_e_BusBlock_balance(bus_fuel_1_4)_:
+1 flow(bus_fuel_backpressure_1_4)
= 0

c_e_BusBlock_balance(bus_fuel_1_5)_:
+1 flow(bus_fuel_backpressure_1_5)
= 0

c_e_BusBlock_balance(bus_fuel_2_6)_:
+1 flow(bus_fuel_backpressure_2_6)
= 0

c_e_BusBlock_balance(bus_fuel_2_7)_:
+1 flow(bus_fuel_backpressure_2_7)
= 0

c_e_BusBlock_balance(bus_fuel_2_8)_:
+1 flow(bus_fuel_backpressure_2_8)
= 0

c_e_BusBlock_balance(bus_heat_0_0)_:
+1 flow(backpressure_bus_heat_0_0)
= 0

c_e_BusBlock_balance(bus_heat_0_1)_:
+1 flow(backpressure_bus_heat_0_1)
= 0

c_e_BusBlock_balance(bus_heat_0_2)_:
+1 flow(backpressure_bus_heat_0_2)
= 0

c_e_BusBlock_balance(bus_heat_1_3)_:
+1 flow(backpressure_bus_heat_1_3)
= 0

c_e_BusBlock_balance(bus_heat_1_4)_:
+1 flow(backpressure_bus_heat_1_4)
= 0

c_e_BusBlock_balance(bus_heat_1_5)_:
+1 flow(backpressure_bus_heat_1_5)
= 0

c_e_BusBlock_balance(bus_heat_2_6)_:
+1 flow(backpressure_bus_heat_2_6)
= 0

c_e_BusBlock_balance(bus_heat_2_7)_:
+1 flow(backpressure_bus_heat_2_7)
= 0

c_e_BusBlock_balance(bus_heat_2_8)_:
+1 flow(backpressure_bus_heat_2_8)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_el_0_0)_:
+0.4 flow(bus_fuel_backpressure_0_0)
-1 flow(backpressure_bus_el_0_0)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_heat_0_0)_:
+0.35 flow(bus_fuel_backpressure_0_0)
-1 flow(backpressure_bus_heat_0_0)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_el_0_1)_:
+0.4 flow(bus_fuel_backpressure_0_1)
-1 flow(backpressure_bus_el_0_1)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_heat_0_1)_:
+0.35 flow(bus_fuel_backpressure_0_1)
-1 flow(backpressure_bus_heat_0_1)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_el_0_2)_:
+0.4 flow(bus_fuel_backpressure_0_2)
-1 flow(backpressure_bus_el_0_2)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_heat_0_2)_:
+0.35 flow(bus_fuel_backpressure_0_2)
-1 flow(backpressure_bus_heat_0_2)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_el_1_3)_:
+0.4 flow(bus_fuel_backpressure_1_3)
-1 flow(backpressure_bus_el_1_3)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_heat_1_3)_:
+0.35 flow(bus_fuel_backpressure_1_3)
-1 flow(backpressure_bus_heat_1_3)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_el_1_4)_:
+0.4 flow(bus_fuel_backpressure_1_4)
-1 flow(backpressure_bus_el_1_4)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_heat_1_4)_:
+0.35 flow(bus_fuel_backpressure_1_4)
-1 flow(backpressure_bus_heat_1_4)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_el_1_5)_:
+0.4 flow(bus_fuel_backpressure_1_5)
-1 flow(backpressure_bus_el_1_5)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_heat_1_5)_:
+0.35 flow(bus_fuel_backpressure_1_5)
-1 flow(backpressure_bus_heat_1_5)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_el_2_6)_:
+0.4 flow(bus_fuel_backpressure_2_6)
-1 flow(backpressure_bus_el_2_6)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_heat_2_6)_:
+0.35 flow(bus_fuel_backpressure_2_6)
-1 flow(backpressure_bus_heat_2_6)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_el_2_7)_:
+0.4 flow(bus_fuel_backpressure_2_7)
-1 flow(backpressure_bus_el_2_7)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_heat_2_7)_:
+0.35 flow(bus_fuel_backpressure_2_7)
-1 flow(backpressure_bus_heat_2_7)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_el_2_8)_:
+0.4 flow(bus_fuel_backpressure_2_8)
-1 flow(backpressure_bus_el_2_8)
= 0

c_e_ConverterBlock_relation(backpressure_bus_fuel_bus_heat_2_8)_:
+0.35 flow(bus_fuel_backpressure_2_8)
-1 flow(backpressure_bus_heat_2_8)
= 0

c_e_InvestmentFlowBlock_total_rule(backpressure_bus_el_0)_:
-1 InvestmentFlowBlock_invest(backpressure_bus_el_0)
+1 InvestmentFlowBlock_total(backpressure_bus_el_0)
= 0

c_e_InvestmentFlowBlock_total_rule(backpressure_bus_el_1)_:
-1 InvestmentFlowBlock_invest(backpressure_bus_el_1)
-1 InvestmentFlowBlock_total(backpressure_bus_el_0)
+1 InvestmentFlowBlock_total(backpressure_bus_el_1)
+1 InvestmentFlowBlock_old(backpressure_bus_el_1)
= 0

c_e_InvestmentFlowBlock_total_rule(backpressure_bus_el_2)_:
-1 InvestmentFlowBlock_invest(backpressure_bus_el_2)
-1 InvestmentFlowBlock_total(backpressure_bus_el_1)
+1 InvestmentFlowBlock_total(backpressure_bus_el_2)
+1 InvestmentFlowBlock_old(backpressure_bus_el_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(backpressure_bus_el_0)_:
+1 InvestmentFlowBlock_old_end(backpressure_bus_el_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(backpressure_bus_el_1)_:
+1 InvestmentFlowBlock_old_end(backpressure_bus_el_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(backpressure_bus_el_2)_:
-1 InvestmentFlowBlock_invest(backpressure_bus_el_0)
+1 InvestmentFlowBlock_old_end(backpressure_bus_el_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(backpressure_bus_el_0)_:
+1 InvestmentFlowBlock_old_exo(backpressure_bus_el_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(backpressure_bus_el_1)_:
+1 InvestmentFlowBlock_old_exo(backpressure_bus_el_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(backpressure_bus_el_2)_:
+1 InvestmentFlowBlock_old_exo(backpressure_bus_el_2)
= 0

c_e_InvestmentFlowBlock_old_rule(backpressure_bus_el_0)_:
+1 InvestmentFlowBlock_old(backpressure_bus_el_0)
-1 InvestmentFlowBlock_old_end(backpressure_bus_el_0)
-1 InvestmentFlowBlock_old_exo(backpressure_bus_el_0)
= 0

c_e_InvestmentFlowBlock_old_rule(backpressure_bus_el_1)_:
+1 InvestmentFlowBlock_old(backpressure_bus_el_1)
-1 InvestmentFlowBlock_old_end(backpressure_bus_el_1)
-1 InvestmentFlowBlock_old_exo(backpressure_bus_el_1)
= 0

c_e_InvestmentFlowBlock_old_rule(backpressure_bus_el_2)_:
+1 InvestmentFlowBlock_old(backpressure_bus_el_2)
-1 InvestmentFlowBlock_old_end(backpressure_bus_el_2)
-1 InvestmentFlowBlock_old_exo(backpressure_bus_el_2)
= 0

c_u_InvestmentFlowBlock_max(backpressure_bus_el_0_0)_:
+1 flow(backpressure_bus_el_0_0)
-1 InvestmentFlowBlock_total(backpressure_bus_el_0)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_bus_el_0_1)_:
+1 flow(backpressure_bus_el_0_1)
-1 InvestmentFlowBlock_total(backpressure_bus_el_0)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_bus_el_0_2)_:
+1 flow(backpressure_bus_el_0_2)
-1 InvestmentFlowBlock_total(backpressure_bus_el_0)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_bus_el_1_3)_:
+1 flow(backpressure_bus_el_1_3)
-1 InvestmentFlowBlock_total(backpressure_bus_el_1)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_bus_el_1_4)_:
+1 flow(backpressure_bus_el_1_4)
-1 InvestmentFlowBlock_total(backpressure_bus_el_1)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_bus_el_1_5)_:
+1 flow(backpressure_bus_el_1_5)
-1 InvestmentFlowBlock_total(backpressure_bus_el_1)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_bus_el_2_6)_:
+1 flow(backpressure_bus_el_2_6)
-1 InvestmentFlowBlock_total(backpressure_bus_el_2)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_bus_el_2_7)_:
+1 flow(backpressure_bus_el_2_7)
-1 InvestmentFlowBlock_total(backpressure_bus_el_2)
<= 0

c_u_InvestmentFlowBlock_max(backpressure_bus_el_2_8)_:
+1 flow(backpressure_bus_el_2_8)
-1 InvestmentFlowBlock_total(backpressure_bus_el_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(backpressure_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_invest(backpressure_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_invest(backpressure_bus_el_2) <= +inf
   0 <= flow(bus_fuel_backpressure_0_0) <= +inf
   0 <= flow(bus_fuel_backpressure_0_1) <= +inf
   0 <= flow(bus_fuel_backpressure_0_2) <= +inf
   0 <= flow(bus_fuel_backpressure_1_3) <= +inf
   0 <= flow(bus_fuel_backpressure_1_4) <= +inf
   0 <= flow(bus_fuel_backpressure_1_5) <= +inf
   0 <= flow(bus_fuel_backpressure_2_6) <= +inf
   0 <= flow(bus_fuel_backpressure_2_7) <= +inf
   0 <= flow(bus_fuel_backpressure_2_8) <= +inf
   0 <= flow(backpressure_bus_el_0_0) <= +inf
   0 <= flow(backpressure_bus_el_0_1) <= +inf
   0 <= flow(backpressure_bus_el_0_2) <= +inf
   0 <= flow(backpressure_bus_el_1_3) <= +inf
   0 <= flow(backpressure_bus_el_1_4) <= +inf
   0 <= flow(backpressure_bus_el_1_5) <= +inf
   0 <= flow(backpressure_bus_el_2_6) <= +inf
   0 <= flow(backpressure_bus_el_2_7) <= +inf
   0 <= flow(backpressure_bus_el_2_8) <= +inf
   0 <= flow(backpressure_bus_heat_0_0) <= +inf
   0 <= flow(backpressure_bus_heat_0_1) <= +inf
   0 <= flow(backpressure_bus_heat_0_2) <= +inf
   0 <= flow(backpressure_bus_heat_1_3) <= +inf
   0 <= flow(backpressure_bus_heat_1_4) <= +inf
   0 <= flow(backpressure_bus_heat_1_5) <= +inf
   0 <= flow(backpressure_bus_heat_2_6) <= +inf
   0 <= flow(backpressure_bus_heat_2_7) <= +inf
   0 <= flow(backpressure_bus_heat_2_8) <= +inf
   0 <= InvestmentFlowBlock_total(backpressure_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_total(backpressure_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_total(backpressure_bus_el_2) <= +inf
   0 <= InvestmentFlowBlock_old(backpressure_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_old(backpressure_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_old(backpressure_bus_el_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(backpressure_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(backpressure_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(backpressure_bus_el_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(backpressure_bus_el_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(backpressure_bus_el_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(backpressure_bus_el_2) <= +inf
end
