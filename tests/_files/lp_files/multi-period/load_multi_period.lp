\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(bus_el_0_0)_:
+0 ONE_VAR_CONSTANT
= -30.0

c_e_BusBlock_balance(bus_el_0_1)_:
+0 ONE_VAR_CONSTANT
= -20.0

c_e_BusBlock_balance(bus_el_0_2)_:
+0 ONE_VAR_CONSTANT
= -50.0

c_e_BusBlock_balance(bus_el_1_3)_:
+0 ONE_VAR_CONSTANT
= -30.0

c_e_BusBlock_balance(bus_el_1_4)_:
+0 ONE_VAR_CONSTANT
= -20.0

c_e_BusBlock_balance(bus_el_1_5)_:
+0 ONE_VAR_CONSTANT
= -50.0

c_e_BusBlock_balance(bus_el_2_6)_:
+0 ONE_VAR_CONSTANT
= -30.0

c_e_BusBlock_balance(bus_el_2_7)_:
+0 ONE_VAR_CONSTANT
= -20.0

c_e_BusBlock_balance(bus_el_2_8)_:
+0 ONE_VAR_CONSTANT
= -50.0

c_e_ONE_VAR_CONSTANT:
+1 ONE_VAR_CONSTANT
= 1

bounds
   1 <= ONE_VAR_CONSTANT <= 1
end
