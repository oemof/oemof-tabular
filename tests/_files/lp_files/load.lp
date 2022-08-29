\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_Bus_balance(electricity_0)_:
+0 ONE_VAR_CONSTANT
= -30

c_e_Bus_balance(electricity_1)_:
+0 ONE_VAR_CONSTANT
= -20

c_e_Bus_balance(electricity_2)_:
+0 ONE_VAR_CONSTANT
= -50

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
end
