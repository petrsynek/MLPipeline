import argparse

import yaml

from MLPipeline.pipeline_builder import Builder
from Tests.utils import create_dummy_pipeline_dict

if __name__ == '__main__':

    ap = argparse.ArgumentParser(
        usage="%(prog)s -d [int] -i [int] -o [int] -m [int]...",
        description="""
        App generates fake pipeline and execute it. Max. running time is 
        maximum runner time (5 secs by default) X depth X max_components_per_level.
        Should not be more than 3 min in default settings but could be much less due to the concurrency of the calls.
        """
    )
    ap.add_argument("-d",
                    "--depth",
                    default=12,
                    type=int
                    )
    ap.add_argument("-i",
                    "--no_inputs",
                    default=2,
                    type=int
                    )
    ap.add_argument("-o",
                    "--no_outputs",
                    default=2,
                    type=int
                    )
    ap.add_argument("-m",
                    "--max_components_per_level",
                    default=3,
                    type=int
                    )

    args = vars(ap.parse_args())
    print(args)

    pipeline = create_dummy_pipeline_dict(
        **{
            'depth': args['depth'],
            'no_inputs': args['no_inputs'],
            'no_outputs': args['no_outputs'],
            'max_components_per_level': args['max_components_per_level'],
        }
    )
    inputs = pipeline['pipeline']['inputs']

    site = Builder()
    site.parsed_yaml = pipeline
    print({j: f'S{i}' for i, j in enumerate(inputs)})
    print(yaml.dump(pipeline))
    site.pass_command_line_inputs({j: f'S{i}' for i, j in enumerate(inputs)})
    pipe = site.build_pipeline()
    fake_result = pipe.fake_run()
    if fake_result:
        if input("Write 'yes' to continue to execute live?: ") == 'yes':
            pipe = site.build_pipeline()
            pipe.run()
    else:
        print("Fake run failed!")
