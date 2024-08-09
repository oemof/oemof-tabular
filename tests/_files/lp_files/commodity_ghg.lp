\* Source Pyomo model name=Model *\

min
objective:
+10 flow(gas_commodity_gas_0_0)
+10 flow(gas_commodity_gas_0_1)
+10 flow(gas_commodity_gas_0_2)

s.t.

c_e_BusBlock_balance(gas_0_0)_:
+1 flow(gas_commodity_gas_0_0)
= 0

c_e_BusBlock_balance(gas_0_1)_:
+1 flow(gas_commodity_gas_0_1)
= 0

c_e_BusBlock_balance(gas_0_2)_:
+1 flow(gas_commodity_gas_0_2)
= 0

c_u_SimpleFlowBlock_full_load_time_max_constr(gas_commodity_gas)_:
+1 flow(gas_commodity_gas_0_0)
+1 flow(gas_commodity_gas_0_1)
+1 flow(gas_commodity_gas_0_2)
<= 1000

c_e_CommodityGHGBlock_relation(gas_commodity_co2_0_0)_:
+56 flow(gas_commodity_gas_0_0)
-1 flow(gas_commodity_co2_0_0)
= 0

c_e_CommodityGHGBlock_relation(gas_commodity_co2_0_1)_:
+56 flow(gas_commodity_gas_0_1)
-1 flow(gas_commodity_co2_0_1)
= 0

c_e_CommodityGHGBlock_relation(gas_commodity_co2_0_2)_:
+56 flow(gas_commodity_gas_0_2)
-1 flow(gas_commodity_co2_0_2)
= 0

bounds
   0 <= flow(gas_commodity_gas_0_0) <= 900.0
   0 <= flow(gas_commodity_gas_0_1) <= 500.0
   0 <= flow(gas_commodity_gas_0_2) <= 400.0
   0 <= flow(gas_commodity_co2_0_0) <= +inf
   0 <= flow(gas_commodity_co2_0_1) <= +inf
   0 <= flow(gas_commodity_co2_0_2) <= +inf
end
