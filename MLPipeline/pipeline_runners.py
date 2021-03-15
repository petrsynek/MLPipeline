from MLPipeline.pipeline_task import AbstractTask


class ImagePreprocessor(AbstractTask):
    """Task that adds I"""

    def execute(self, inputs):
        self.dummy_executor(inputs, 'I', (1, 2))


class OCRModel(AbstractTask):
    """Task that adds O"""

    def execute(self, inputs):
        self.dummy_executor(inputs, 'O', (1, 2))


class ExtractionModel(AbstractTask):

    def execute(self, inputs):
        self.dummy_executor(inputs, 'E', (1, 2))
