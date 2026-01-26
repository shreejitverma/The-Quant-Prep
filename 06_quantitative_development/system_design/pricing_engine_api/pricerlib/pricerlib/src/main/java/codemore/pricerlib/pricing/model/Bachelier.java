package codemore.pricerlib.pricing.model;

import codemore.pricerlib.pricing.matlib.Matlib;
import codemore.pricerlib.pricing.option.pathindependent.PathIndependentOption;
import codemore.pricerlib.pricing.option.pathindependent.rates.EuropeanCaplet;

import java.util.ArrayList;
import java.util.HashMap;

public class Bachelier implements Model{
    private double sigma;
    private HashMap<String, Double> parameters;

    // Constructors
    public Bachelier(){
        this.sigma = 0.25;
        this.parameters = new HashMap<>();
        this.parameters.put("sigma", sigma);
    }

    public Bachelier(double sigma){
        this.sigma = sigma;
        this.parameters.put("sigma", sigma);
    };

    @Override
    public HashMap<String, Double> getParameters() {
        return null;
    }

    public double calibrationErrorFunction(ArrayList<Double> parameters) {
        return 0;
    }

    public double closedFormCapletPricer(EuropeanCaplet caplet) {
        /********************************************
         Simple Bachelier pricing formula for european caplets

         Model parmeters:
         sigma = implied volatility
         ********************************************/
        double F = caplet.getForward();
        double K = caplet.getStrike();
        double r = caplet.getRate();
        double T = caplet.getExpiry();

        double sigmaT = sigma * Math.sqrt(T);
        double D = (F - K)/(sigmaT);

        // Calculate the price of the caplet
        double price = Math.exp(-r * T) * sigmaT * (Matlib.normCDF(D) * D + Matlib.normPDF(D));
        
        return price;
    }

}
