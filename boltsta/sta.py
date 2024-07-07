from .readers import sdc_parser,parse_liberty_file
from .network import graph_path_handler
from .model import Model

def run_sta(library_path,design_path,sdc_path,dir):

    # first step is to read liberty file
    pdk_path = parse_liberty_file(library_path)

    # seconcd step is to read the constraints
    sdc_constraints = sdc_parser(sdc_path)

    # constraints variables needed
    clock_transition = sdc_constraints['clock_transition']
    clock_hold_uncertainty = sdc_constraints['clock_hold_uncertainty']
    clock_setup_uncertainty = sdc_constraints['clock_setup_uncertainty']
    timing_derates = sdc_constraints['timing_derates']

    # third step is to generate the grapth 
    rr, rr_atr_list, ir, ir_atr_list, ro, ro_atr_list, fanout_dict = graph_path_handler(design_path)

    # fourh step is to generate the timing reports
    Model(pdk_path,rr,rr_atr_list,clock_transition,0.14,dir,0,clock_setup_uncertainty,10)
    
    pass