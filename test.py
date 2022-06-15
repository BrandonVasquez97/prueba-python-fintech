from mainApp import principal
import pandas as pd 
import unittest

class TestDataFrame(unittest.TestCase):
    def test_1(self):
        df1 = principal(True)
        if type(df1) is str:
            self.assertEqual(df1, "No hay tabla final para mostrar")
        else:
            df1.drop("Time", axis=1, inplace=True)
            list1 = ["Americas", "Colombia", "2001ca082b2d2742765d8ac9182678bfe0374fbf"]
            list2 = ["Asia", "Turkey", "efaad145ca7774441dc7897b2ad3d402911cd5b5"]
            listaData = [list1, list2]
            respuesta_esperada = pd.DataFrame(listaData, columns=["Region", "City Name","Language"])
            
            pd.testing.assert_frame_equal(df1,respuesta_esperada,check_names=False)

if __name__ == '__main__':
    unittest.main()