
import unittest
from typing import Any

from jufo_pptx_script.templater.TemplateApplier import TemplateApplier
from jufo_pptx_script.templater.Template import Template

from functools import partial


class TestTexttemplate(unittest.TestCase):

    def setup_environment(self, data: dict[str, Any] = None):
        if data is None:
            data = {}

        env = Template()

        applier = TemplateApplier()

        parse: partial[str] = partial(applier.parse, env, data)

        def assert_array(results: [str], value: str):
            for res in results:
                self.assertEqual(res, value)

        return env, parse, assert_array

    def test_no_args(self):

        env, parse, assert_array = self.setup_environment()

        #region No-Args

        @env
        def no_args():
            return "no_args"

        assert_array([
            parse("I am {{ no_args() }}"),
            parse("I am {{ no_args(  ) }}"),
            parse("I am {{no_args()}}"),
            parse("I am {{no_args() }}"),
            parse("I am {{ no_args()}}"),
            parse("I am {{no_args(   )}}"),
            parse("I am {{ no_args  (  ) }}")
        ], "I am no_args")

    def test_one_arg_from_text(self):

        env, parse, assert_array = self.setup_environment()

        @env
        def one_arg_txt(arg):
            return f"one_arg_txt({arg})"

        assert_array([
            parse("I am {{ one_arg_txt(arg=A c) }}"),
            parse("I am {{ one_arg_txt( arg=A c ) }}"),
            parse("I am {{ one_arg_txt( arg=  A c ) }}"),
            parse("I am {{ one_arg_txt( arg  =  A c ) }}"),
            parse("I am {{ one_arg_txt( arg =  A c ) }}"),
            parse("I am {{ one_arg_txt(  arg=  A c ) }}"),
            parse("I am {{ one_arg_txt(    arg   =  A c   )   }}"),
        ],"I am one_arg_txt(A c)")

    def test_two_args_from_text(self):

        env, parse, assert_array = self.setup_environment()

        @env
        def two_args_text(a,b):
            return f"two_args_text({a},{b})"

        assert_array([
            parse("I am {{ two_args_text(a=A c,b=D f) }}"),
            parse("I am {{two_args_text(a=A c,b=D f)}}"),
            parse("I am {{two_args_text(a=A c,b=D f    )}}"),
            parse("I am {{two_args_text(a=A c,b=   D f    )}}"),
            parse("I am {{two_args_text(a=A c,b =   D f    )}}"),
            parse("I am {{two_args_text(a=A c, b =   D f    )}}"),
            parse("I am {{two_args_text(a=A c , b =   D f    )}}"),
            parse("I am {{two_args_text(a= A c , b =   D f    )}}"),
            parse("I am {{two_args_text( a = A c , b =   D f    )}}"),
            parse("I am {{two_args_text( a= A c , b =   D f    )}}"),
            parse("I am {{   two_args_text(   a    =   A c   ,    b    =     D f    )}}"),
            parse("I am {{ two_args_text( a = A c , b = D f ) }} "),
            parse("I am {{ two_args_text(b=D f,a=A c) }}"),
        ], "I am two_args_text(A c,D f)")


    def test_one_arg_from_script(self):

        env, parse, assert_array = self.setup_environment({
            'one_arg': "A c"
        })

        @env
        def f(one_arg: str):
            return f"f-call({one_arg})"

        assert_array([
            parse("I am {{ f() }}"),
            parse("I am {{ f( ) }}"),
            parse("I am {{ f(    ) }}"),
            parse("I am {{f()}}"),
        ], "I am f-call(A c)")

    def test_two_args_from_script(self):

        env, parse, assert_array = self.setup_environment({
            'f_arg': 'A c',
            's_arg': 'D f'
        })

        @env
        def f(f_arg: str, s_arg):
            return f"f-call({f_arg}, {s_arg})"

        assert_array([
            parse("I am {{ f() }}"),
            parse("I am {{ f(  ) }}"),
            parse("I am {{f()}}"),
        ],"I am f-call(A c, D f)")

    def test_two_args_one_from_text_one_from_script(self):
        env = Template()

        env, parse, assert_array = self.setup_environment({
            'script_arg': 'D f',
        })

        @env
        def f(txt_arg: str, script_arg):
            return f"f-call({txt_arg}, {script_arg})"

        assert_array([
            parse("I am {{ f(txt_arg=A c) }}"),
            parse("I am {{ f(txt_arg=A c  ) }}"),
            parse("I am {{ f(txt_arg= A c  ) }}"),
            parse("I am {{ f(txt_arg = A c  ) }}"),
            parse("I am {{ f( txt_arg = A c  ) }}"),
        ],"I am f-call(A c, D f)")

    def test_to_little_args(self):
        with self.assertRaises(ValueError) as context:
            env, parse, assert_array = self.setup_environment({
                'a': 'data'
            })

            @env
            def f(a,b):
                return f"f-call({a}, {b})"

            parse("I am {{ f() }}")

        self.assertEqual('''
Unknown error occurred. Please check your input: 'I am {{ f() }}' (Error trying to process rule "function_call":

Function 'f' requires the parameter(s) 'b', which are/were not given.)
        '''.strip(), str(context.exception).strip())

    def test_to_many_args(self):
        with self.assertRaises(ValueError) as context:

            env, parse, assert_array = self.setup_environment({
                'a': 'data',
                'b': "dataToo"
            })

            @env
            def f(a):
                return f"f-call({a})"

            parse('I am {{ f() }}')


        self.assertEqual('''
Unknown error occurred. Please check your input: 'I am {{ f() }}' (Error trying to process rule "function_call":

Function 'f' doesn't have/has the parameter(s) 'b', but they were passed anyway.)
        '''.strip(), str(context.exception).strip())