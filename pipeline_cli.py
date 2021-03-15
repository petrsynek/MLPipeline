import argparse

from MLPipeline.pipeline_builder import Builder

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-i",
                    "--inputs",
                    required=True,
                    nargs='*',
                    help="list of input values in format a=1 b=2")
    ap.add_argument("-f",
                    "--file",
                    required=True,
                    help="relative path to the pipeline.yaml file")
    ap.add_argument("-b",
                    "--bad_yaml",
                    action='store_true',
                    help="If you plan to use yaml where everything is dict, use this tag.")
    args = vars(ap.parse_args())

    cline_inputs = {cline_input.split('=')[0]: cline_input.split('=')[1]
                    for cline_input in args['inputs']}

    site = Builder()
    site.load_yaml(args['file'])
    site.pass_command_line_inputs(cline_inputs)
    pipe = site.build_pipeline(args['bad_yaml'])
    fake_result = pipe.fake_run()
    if fake_result:
        pipe = site.build_pipeline(args['bad_yaml'])
        pipe.run()
