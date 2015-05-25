Finding the worst voltage drop during testing
------------------

Step 1: Extract points/coordinate information:

    Example: $ python extract_points.py b01.def

    Output: a "b01.points" file

Step 2: Create the power grid using coordinate information and toggle trace.

    Syntax: $ python create_spice_power_grid_BPM.py <.points file> <toggle_trace_file> <no_primary_input>
    
    Example: $ python create_spice_power_grid_BPM.py b04.points b04.toggle_trace_xfill_without_ordered.rfill.device.coord 77

    Output: "b04_power_grid_BPM_with_currents.cir"

    Note: The <toggle_trace_file> can be either the "rfill" of the "ofill" file.

Step 3: Simulate the circuit using ngspice.
    
    Example: $ ngspice b04_power_grid_BPM_with_currents.cir

    Output: a file called "minimums" (note: the ngspice simulation appends to this file. So remember
            to delete this file if re-running simulation.)

Step 4: Find the worst voltage drop.
    
    Syntax: $ python minofmins.py minimums

    Output: A number, which is the least voltage seen by the circuit during the testing. You
    can compare different orderings using different toggle_trace files in step 2.
