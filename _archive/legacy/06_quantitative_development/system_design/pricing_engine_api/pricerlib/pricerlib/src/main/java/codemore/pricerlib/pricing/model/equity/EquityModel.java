package codemore.pricerlib.pricing.model.equity;

import codemore.pricerlib.pricing.model.Model;
import codemore.pricerlib.pricing.option.pathindependent.PathIndependentOption;
import codemore.pricerlib.pricing.option.pathindependent.equity.EuropeanCall;

import java.util.ArrayList;
import java.util.HashMap;


public interface EquityModel extends Model {
    // Pricing formula for a vanilla European call
    public double closedFormCallPricer(EuropeanCall europeanOption);
    public double calibrationErrorFunction(ArrayList<Double> parameters);
}
