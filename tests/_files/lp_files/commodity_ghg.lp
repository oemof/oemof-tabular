\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(gas_commodity_gas_0)
+10 flow(gas_commodity_gas_1)
+10 flow(gas_commodity_gas_2)

s.t.

c_e_BusBlock_balance(co2_0)_:
+1 flow(gas_commodity_co2_0)
= 0

c_e_BusBlock_balance(co2_1)_:
+1 flow(gas_commodity_co2_1)
= 0

c_e_BusBlock_balance(co2_2)_:
+1 flow(gas_commodity_co2_2)
= 0

c_e_BusBlock_balance(gas_0)_:
+1 flow(gas_commodity_gas_0)
= 0

c_e_BusBlock_balance(gas_1)_:
+1 flow(gas_commodity_gas_1)
= 0

c_e_BusBlock_balance(gas_2)_:
+1 flow(gas_commodity_gas_2)
= 0

c_u_SimpleFlowBlock_full_load_time_max_constr(gas_commodity_gas)_:
+1 flow(gas_commodity_gas_0)
+1 flow(gas_commodity_gas_1)
+1 flow(gas_commodity_gas_2)
<= 1000

c_e_CommodityGHGBlock_relation(gas_commodity_co2_0)_:
-2 flow(gas_commodity_gas_0)
-1 flow(gas_commodity_co2_0)
= 0

c_e_CommodityGHGBlock_relation(gas_commodity_co2_1)_:
-2 flow(gas_commodity_gas_1)
-1 flow(gas_commodity_co2_1)
= 0

c_e_CommodityGHGBlock_relation(gas_commodity_co2_2)_:
-2 flow(gas_commodity_gas_2)
-1 flow(gas_commodity_co2_2)
= 0

bounds
   0 <= flow(gas_commodity_gas_0) <= 900.0
   0 <= flow(gas_commodity_gas_1) <= 500.0
   0 <= flow(gas_commodity_gas_2) <= 400.0
   -inf <= flow(gas_commodity_co2_0) <= +inf
   -inf <= flow(gas_commodity_co2_1) <= +inf
   -inf <= flow(gas_commodity_co2_2) <= +inf
end
