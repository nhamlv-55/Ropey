FALLBACK_SERVER = 'localhost:50052'
DOPING_SERVER = 'localhost:50050'
FALLBACK_CONFIG = ['fp.spacer.dump_benchmarks=true',
                   'fp.spacer.dump_threshold=99999',
                   'fp.spacer.use_expansion=false',
                   'fp.spacer.arith.solver=6',
                   'fp.print_statistics=true',
                   'fp.spacer.use_h_inductive_generalizer=42',
                   'fp.spacer.use_inductive_generalizer=false',
                   'fp.spacer.grpc_host_port={}'.format(FALLBACK_SERVER),
                   'fp.validate=true',
                   '-tr:spacer.ind_gen',
                   '-T:$CPU',
                   '-memory:$MEM $1']

FALLBACK_CONFIG = ['fp.spacer.dump_benchmarks=true',
                   'fp.spacer.dump_threshold=99999',
                   'fp.spacer.use_expansion=false',
                   'fp.spacer.arith.solver=6',
                   'fp.print_statistics=true',
                   'fp.spacer.use_h_inductive_generalizer=42',
                   'fp.spacer.use_inductive_generalizer=false',
                   'fp.spacer.grpc_host_port={}'.format(DOPING_SERVER),
                   'fp.validate=true',
                   '-tr:spacer.ind_gen',
                   '-T:$CPU',
                   '-memory:$MEM $1']

