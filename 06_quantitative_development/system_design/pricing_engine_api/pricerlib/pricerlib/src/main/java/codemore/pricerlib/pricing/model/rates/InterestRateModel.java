package codemore.pricerlib.pricing.model.rates;

import codemore.pricerlib.pricing.model.Model;
import codemore.pricerlib.pricing.option.pathindependent.rates.EuropeanCaplet;

import java.util.ArrayList;
import java.util.HashMap;

public interface InterestRateModel extends Model {
    double closedFormCapletPricer(EuropeanCaplet caplet);
    public double calibrationErrorFunction(ArrayList<Double>parameters);
}
