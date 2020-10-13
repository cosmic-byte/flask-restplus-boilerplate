from app.main.core.DlLinerRegression import DlLinerRegression
from app.test.base import BaseTestCase


class DlLinearRegressionTest(BaseTestCase):

    def testDlLinearRegression(self):
        lr = DlLinerRegression(dataFileName="app/test/coretest/dllinearregressiontest/Folds5x2_pp.csv",
                               outputFileName="app/test/coretest/dllinearregressiontest/rs.txt")

        lr.readData()
        lr.run()
        lr.output()
        print("text")


if __name__ == '__main__':
    unittest.main()