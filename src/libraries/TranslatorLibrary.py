import sys
from unittest.mock import Mock, MagicMock
from commands.translator import Translator
sys.path.append(sys.path[0] + "/..")

class TranslatorLibrary:
    def __init__(self):
        self.db_model = []
        self.inputs = []
        self.service_mock = MagicMock()
        self.io_mock = MagicMock()
        self.search_mock = MagicMock()


    def input_text(self, text):
        if text == "<EMPTY>":
            self.inputs.append("")
        else:
            self.inputs.append(text)
    
    def reset_input(self):
        self.inputs = []

    def add_inputs(self):
        self.service_mock.post()

    def get_all_refs(self):
        
        def post(self):
                for e in self.inputs:
                    self.db_model.append(e)

        self.io_mock.read.side_effect = self.inputs
        self.service_mock.post.side_effect = post
        
        translate = Translator(self.service_mock,
                               self.io_mock, self.search_mock)
        translate.run()

        
        self.service_mock.get_all.assert_called()
        

    def get_with_tag(self):

        def post(self):
                for e in self.inputs:
                    self.db_model.append(e)

        self.io_mock.read.side_effect = self.inputs
        self.service_mock.post.side_effect = post

        translate = Translator(self.service_mock,
                               self.io_mock,
                               self.search_mock)
        translate.run()

        self.service_mock.get_by_tag.assert_called_with("ttt")
