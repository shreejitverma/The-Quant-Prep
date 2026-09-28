package codemore.pricerlib.pricing.model;

import codemore.pricerlib.pricing.matlib.Matlib;
import codemore.pricerlib.pricing.option.pathindependent.PathIndependentOption;
import codemore.pricerlib.pricing.option.pathindependent.equity.EuropeanCall;
import codemore.pricerlib.pricing.option.pathindependent.rates.EuropeanCaplet;

import static java.lang.Math.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class BlackScholes implements Model{
    private double sigma;
    private HashMap<String, Double> parameters;

    // Constructors
    public BlackScholes(){
        this.sigma = 0.25;
        this.parameters = new HashMap<>();
        this.parameters.put("sigma", sigma);
    }

    public BlackScholes(double sigma){
        this.sigma = sigma;
        this.parameters = new HashMap<>();
        this.parameters.put("sigma", sigma);
    };


    // Get parameters as a hashmap
    public HashMap<String, Double> getParameters(){
        return parameters;
    }

    @Override
    public double calibrationErrorFunction(ArrayList<Double> parameters) {
        return 0;
    }

    ;

    // Set model parameters obtained from an array of values
    public void setParameters(HashMap newParameters){
        // Ensure that all parameters are the same
        List<String> parameterNames = new ArrayList<String>(parameters.keySet());
        List<String> newParameterNames = new ArrayList<String>(newParameters.keySet());

        if (parameterNames.equals(newParameterNames)){
            parameters = newParameters;
        }else {
            System.out.println("Parameter sets are different");
        }
    };

    public double closedFormCallPricer(EuropeanCall call) {
        /********************************************
         Simple Black Scholes pricing formula for european call options

         Variables:
         St = Spot price
         K = Strike
         T = Time to maturity
         r = Interest rate

         Model parmeters:
         sigma = implied volatility
         ********************************************/
        //Get variables from Call option class
        double St = call.getSpot();
        double K = call.getStrike();
        double T = call.getExpiry();
        double r = call.getRate();

        // Calculate d1 and d2
        double sigma = parameters.get("sigma");
        double sigmaSqrtT = sigma * sqrt(T);
        double d1 = (log(St/K) + (r + (sigma*sigma)/2) * T)/(sigmaSqrtT);
        double d2 = d1 - (sigmaSqrtT);

        // Calculate Nd1 and Nd2
        double Nd1 = Matlib.normCDF(d1);
        double Nd2 = Matlib.normCDF(d2);

        // Return call price
        double callPrice = St*Nd1 - K * Nd2 * exp(-r * T);

        return callPrice;
    }

    public double closedFormCapletPricer(EuropeanCaplet caplet) {
        /********************************************
         Simple Black Scholes pricing formula for european call options

         Variables:
         St = Spot price
         K = Strike
         T = Time to maturity
         r = Interest rate

         Model parmeters:
         sigma = implied volatility
         ********************************************/
        //Get variables from Call option class
        double St = caplet.getSpot();
        double K = caplet.getStrike();
        double T = caplet.getExpiry();
        double r = caplet.getRate();

        // Calculate d1 and d2
        double sigma = parameters.get("sigma");
        double sigmaSqrtT = sigma * sqrt(T);
        double d1 = (log(St/K) + (r + (sigma*sigma)/2) * T)/(sigmaSqrtT);
        double d2 = d1 - (sigmaSqrtT);

        // Calculate Nd1 and Nd2
        double Nd1 = Matlib.normCDF(d1);
        double Nd2 = Matlib.normCDF(d2);

        // Return call price
        double callPrice = St*Nd1 - K * Nd2 * exp(-r * T);

        return callPrice;
    }
}
