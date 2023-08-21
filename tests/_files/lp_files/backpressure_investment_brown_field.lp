\* Source Pyomo model name=Model *\

min
objective:
+50 InvestmentFlowBlock_invest(backpressure_electricity_0)
+0.6 flow(fuel_backpressure_0_0)
+0.6 flow(fuel_backpressure_0_1)
+0.6 flow(fuel_backpressure_0_2)

s.t.

c_e_BusBlock_balance(heat_0_0)_:
+1 flow(backpressure_heat_0_0)
= 0

c_e_BusBlock_balance(heat_0_1)_:
+1 flow(backpressure_heat_0_1)
= 0

c_e_BusBlock_balance(heat_0_2)_:
+1 flow(backpressure_heat_0_2)
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

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(backpressure_electricity_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(backpressure_electricity_0_1)
= 0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(backpressure_electricity_0_2)
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

c_e_InvestmentFlowBlock_total_rule(backpressure_electricity_0)_:
-1 InvestmentFlowBlock_invest(backpressure_electricity_0)
+1 InvestmentFlowBlock_total(backpressure_electricity_0)
= 1000

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

bounds
   0 <= InvestmentFlowBlock_invest(backpressure_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_total(backpressure_electricity_0) <= +inf
   0 <= flow(fuel_backpressure_0_0) <= +inf
   0 <= flow(fuel_backpressure_0_1) <= +inf
   0 <= flow(fuel_backpressure_0_2) <= +inf
   0 <= flow(backpressure_heat_0_0) <= +inf
   0 <= flow(backpressure_heat_0_1) <= +inf
   0 <= flow(backpressure_heat_0_2) <= +inf
   0 <= flow(backpressure_electricity_0_0) <= +inf
   0 <= flow(backpressure_electricity_0_1) <= +inf
   0 <= flow(backpressure_electricity_0_2) <= +inf
end
