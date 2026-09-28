package codemore.pricerlib.pricing.model;

import java.util.ArrayList;
import java.util.HashMap;

public interface Model {
    public HashMap<String, Double> getParameters();
    public double calibrationErrorFunction(ArrayList<Double> parameters);
}
