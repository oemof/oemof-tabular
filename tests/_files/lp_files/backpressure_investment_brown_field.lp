\* Source Pyomo model name=Model *\

min 
objective:
+50 InvestmentFlow_invest(backpressure_electricity)
+0.59999999999999998 flow(fuel_backpressure_0)
+0.59999999999999998 flow(fuel_backpressure_1)
+0.59999999999999998 flow(fuel_backpressure_2)

s.t.

c_e_Bus_balance(electricity_0)_:
+1 flow(backpressure_electricity_0)
= 0

c_e_Bus_balance(electricity_1)_:
+1 flow(backpressure_electricity_1)
= 0

c_e_Bus_balance(electricity_2)_:
+1 flow(backpressure_electricity_2)
= 0

c_e_Bus_balance(fuel_0)_:
+1 flow(fuel_backpressure_0)
= 0

c_e_Bus_balance(fuel_1)_:
+1 flow(fuel_backpressure_1)
= 0

c_e_Bus_balance(fuel_2)_:
+1 flow(fuel_backpressure_2)
= 0

c_e_Bus_balance(heat_0)_:
+1 flow(backpressure_heat_0)
= 0

c_e_Bus_balance(heat_1)_:
+1 flow(backpressure_heat_1)
= 0

c_e_Bus_balance(heat_2)_:
+1 flow(backpressure_heat_2)
= 0

c_e_Transformer_relation(backpressure_fuel_electricity_0)_:
-1 flow(backpressure_electricity_0)
+0.40000000000000002 flow(fuel_backpressure_0)
= 0

c_e_Transformer_relation(backpressure_fuel_electricity_1)_:
-1 flow(backpressure_electricity_1)
+0.40000000000000002 flow(fuel_backpressure_1)
= 0

c_e_Transformer_relation(backpressure_fuel_electricity_2)_:
-1 flow(backpressure_electricity_2)
+0.40000000000000002 flow(fuel_backpressure_2)
= 0

c_e_Transformer_relation(backpressure_fuel_heat_0)_:
-1 flow(backpressure_heat_0)
+0.34999999999999998 flow(fuel_backpressure_0)
= 0

c_e_Transformer_relation(backpressure_fuel_heat_1)_:
-1 flow(backpressure_heat_1)
+0.34999999999999998 flow(fuel_backpressure_1)
= 0

c_e_Transformer_relation(backpressure_fuel_heat_2)_:
-1 flow(backpressure_heat_2)
+0.34999999999999998 flow(fuel_backpressure_2)
= 0

c_u_InvestmentFlow_max(backpressure_electricity_0)_:
-1 InvestmentFlow_invest(backpressure_electricity)
+1 flow(backpressure_electricity_0)
<= 1000

c_u_InvestmentFlow_max(backpressure_electricity_1)_:
-1 InvestmentFlow_invest(backpressure_electricity)
+1 flow(backpressure_electricity_1)
<= 1000

c_u_InvestmentFlow_max(backpressure_electricity_2)_:
-1 InvestmentFlow_invest(backpressure_electricity)
+1 flow(backpressure_electricity_2)
<= 1000

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(backpressure_electricity_0) <= +inf
   0 <= flow(backpressure_electricity_1) <= +inf
   0 <= flow(backpressure_electricity_2) <= +inf
   0 <= flow(backpressure_heat_0) <= +inf
   0 <= flow(backpressure_heat_1) <= +inf
   0 <= flow(backpressure_heat_2) <= +inf
   0 <= flow(fuel_backpressure_0) <= +inf
   0 <= flow(fuel_backpressure_1) <= +inf
   0 <= flow(fuel_backpressure_2) <= +inf
   0 <= InvestmentFlow_invest(backpressure_electricity) <= +inf
end
