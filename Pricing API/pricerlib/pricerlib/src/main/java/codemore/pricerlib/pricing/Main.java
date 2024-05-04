package codemore.pricerlib.pricing;

import codemore.pricerlib.pricing.io.CSV;
import codemore.pricerlib.pricing.matlib.Complex;
import codemore.pricerlib.pricing.matlib.Matlib;
import codemore.pricerlib.pricing.model.*;
import codemore.pricerlib.pricing.model.equity.BlackScholesEquity;
import codemore.pricerlib.pricing.model.equity.EquityModel;
import codemore.pricerlib.pricing.model.equity.Heston;
import codemore.pricerlib.pricing.option.pathindependent.equity.EuropeanCall;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;

public class Main {

    public static void main(String[] args) throws FileNotFoundException {
        EuropeanCall call = new EuropeanCall();
        Heston heston = new Heston();
        BlackScholesEquity bsModel = new BlackScholesEquity();
        call.price(heston);

        // Show the heston parameters
        System.out.println(heston.getParameters());
        System.out.println(Matlib.normCDF(0));
        System.out.println(Matlib.normCDF(-1.96));

        double sigma = 0.2;
        // Create new parameter HashMap
        HashMap<String, Double> newParameter = new HashMap<>();
        newParameter.put("sigma", sigma);

        // Set the vol parameter
        bsModel.setParameters(newParameter);
        Double price = call.price(bsModel);
        double bsPrice= call.price(bsModel);
        System.out.println(bsPrice);

        Complex test = new Complex(1.0, 1.0);
        Complex test2= new Complex(2.0, 2.0);
        test = test.divide(test2);
        test.print();

        CSV csv = new CSV("./data/betasLMM.csv", ",");
        ArrayList<ArrayList<String>> file = csv.read();
        System.out.print(file.get(0).get(1));

    }
}
